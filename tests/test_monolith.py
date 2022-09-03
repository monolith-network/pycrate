'''
   This test is to check the functionality of the 
   pycrate monolith object, but it also happens to be 
   a great way to test the monolith itsself to a degree
'''

from sys import exit
from pycrate import *

address = IPV4Address("0.0.0.0", 8080)

server = Monolith(address)

if not server.is_connected():
   print("Not able to contact a monolith with given config: " + 
            address.url + 
            ":" + 
            str(address.port))
   exit(1)

def test_registrar():
   test_node_id = "test_node_0"
   node = NodeV1(test_node_id, "A test node from pycrate")
   node.add_sensor(NodeV1SensorEntry("0", "pycrate-temp", "a test sensor"))
   node.add_sensor(NodeV1SensorEntry("1", "pycrate-flame", "a test sensor"))
   node.add_sensor(NodeV1SensorEntry("2", "pycrate-motion", "a test sensor"))

   bunk_node = NodeV1("I wont exist", "But do any of us really?")

   # Register the node
   assert(server.registrar_add_node(node))
   
   # Probe for the node
   assert(server.registrar_probe(node))

   # Check for non-added node
   assert(not server.registrar_probe(bunk_node))

   # Fetch the node
   fetched_node = server.registrar_fetch_node(test_node_id)

   assert(fetched_node is not None)

   # Compare the nodes and ensure no data loss
   assert(fetched_node.id == node.id)
   assert(fetched_node.description == node.description)
   assert(len(fetched_node.sensors) == len(node.sensors))
   for x in range(0, len(fetched_node.sensors)):
      assert(fetched_node.sensors[x].id == node.sensors[x].id)
      assert(fetched_node.sensors[x].description == node.sensors[x].description)
      assert(fetched_node.sensors[x].type == node.sensors[x].type)

   # Delete item from registry
   assert(server.registrar_delete_node(test_node_id))

   # Ensure its gone
   assert(server.registrar_fetch_node(test_node_id) is None)


print("Test endpoint: Registrar")
test_registrar()