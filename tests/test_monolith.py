'''
   This test is to check the functionality of the 
   pycrate monolith object, but it also happens to be 
   a great way to test the monolith itsself to a degree
'''

from sys import exit
from time import sleep
from pycrate import *

address = IPV4Connection("0.0.0.0", 8080)

server = Monolith(address)

if not server.is_connected():
   print("Not able to contact a monolith with given config: " + 
            address.address + 
            ":" + 
            str(address.port))
   exit(1)

'''
   Node / Metrics used in multiple tests
'''
metric_node = NodeV1("pycrate-metric-node", 
                     "A node used to submit metrics in pycrate test")

assert(metric_node.add_sensor(NodeV1SensorEntry("pycrate-0", "[empty]", "[empty]")))
assert(metric_node.add_sensor(NodeV1SensorEntry("pycrate-1", "[empty]", "[empty]")))

'''
   For the sake of tests these entries should
   stay ordered oldest to newest. 
'''
metric_readings = [
   ReadingV1(924204842, "pycrate-metric-node", "pycrate-0", 42.0),
   ReadingV1(924204853, "pycrate-metric-node", "pycrate-0", 97.0),
   ReadingV1(1634238000, "pycrate-metric-node", "pycrate-1", 0.0),
   ReadingV1(1634238001, "pycrate-metric-node", "pycrate-1", 9029.0),
]

'''
   Test the registrar endpoints
'''
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

'''
   Test the stream related endpoints
'''
def test_streams():

   assert(server.metric_stream_add(IPV4Connection("0.0.0.0", 9087)))

   # Sleep as this is a queued request
   sleep(5.0)

   assert(server.metric_stream_delete(IPV4Connection("0.0.0.0", 9087)))

   # Sleep as this is a queued request
   sleep(5.0)

'''
   Test metric submission
'''
def test_metric_submission():
   # Submit the metrics
   for reading in metric_readings:
      assert(server.metric_submit_reading(reading))

   # Sleep as this is a queued request
   sleep(5.0)

   assert(server.metric_submit_heartbeat(HeartbeatV1(metric_node.id)))

'''
   Test metric fetching
'''
def test_metric_fetch():

   retrieval_error_message = '''
Retrieved metrics are not the same in count as we've submitted. 
This could be because a faild test has left old metrics in the monolith 
metric database. Purge the database of test data and try again
'''

   # Range fetch
   result = server.metric_fetch_range(metric_node.id, metric_readings[0].timestamp, metric_readings[-1].timestamp)
   assert(result is not None)
   assert(result is not False)

   decoded = []
   for entry in result:
      decoded.append( 
         ReadingV1(entry["timestamp"], entry["node_id"], entry["sensor_id"], entry["value"])
      )

   if len(decoded) != len(metric_readings)-2:
      print(retrieval_error_message)
      exit(1)

   # Fetch all after a given time
   decoded.clear()
   
   result = server.metric_fetch_after(metric_node.id, metric_readings[0].timestamp)
   assert(result is not None)
   assert(result is not False)

   decoded = []
   for entry in result:
      decoded.append( 
         ReadingV1(entry["timestamp"], entry["node_id"], entry["sensor_id"], entry["value"])
      )

   if len(decoded) != len(metric_readings)-1:
      print(retrieval_error_message)
      exit(1)

   # Fetch all before a given time
   decoded.clear()
   
   result = server.metric_fetch_before(metric_node.id, metric_readings[-1].timestamp)
   assert(result is not None)
   assert(result is not False)

   decoded = []
   for entry in result:
      decoded.append( 
         ReadingV1(entry["timestamp"], entry["node_id"], entry["sensor_id"], entry["value"])
      )

   if len(decoded) != len(metric_readings)-1:
      print(retrieval_error_message)
      exit(1)

'''
   Test node /sensor fetching
'''
def test_node_sensor_fetch():

   retrieval_error_message = '''
Retrieved nodes or sensors are not the same in count as we've submitted. 
This could be because a faild test has left old data in the monolith 
database. Purge the database of test data and try again
'''

   result = server.metric_fetch_nodes()
   assert(result is not None)
   assert(result is not False)

   if len(result) != 1:
      print(retrieval_error_message)
      exit(1)

   assert(result[0] == metric_node.id)

   result = server.metric_fetch_sensors(metric_node.id)
   assert(result is not None)
   assert(result is not False)

   for sensor in metric_node.sensors:
      assert(sensor.id in result)


def test_version():
   result = server.get_version()
   assert(result is not None)
   assert(result is not False)
   assert(result.name == "Monolith")
   print(result.name + " | version: " + result.major + "." + result.minor + "." + result.patch + " | build hash: " + result.hash)

# ---------------------------------------------------------------------------------

print("Test endpoint: Version")
test_version()
print("[PASS]")

print("Test endpoint: Registrar")
test_registrar()
print("[PASS]")

# Register the node used in the next tests
assert(server.registrar_add_node(metric_node))

print("Test endpoint: Metric submission")
test_metric_submission()
print("[PASS]")

print("Test endpoint: Node / Sensor fetch")
test_node_sensor_fetch()
print("[PASS]")

print("Test endpoint: Metric fetch")
test_metric_fetch()
print("[PASS]")

print("Test endpoint: Metric Streams")
test_streams()
print("[PASS]")

# Remove the node
assert(server.registrar_delete_node(metric_node.id))
