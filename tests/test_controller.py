from pycrate import *
from time import sleep 
address = IPV4Connection("0.0.0.0", 8080)

server = Monolith(address)

if not server.is_connected():
   print("Not able to contact a monolith with given config: " + 
            address.address + 
            ":" + 
            str(address.port))
   exit(1)

# Controller

controller_address = IPV4Connection("0.0.0.0", 6969)
controller_id = "test_controller"
controller = ControllerV1(controller_id, "A test controller", controller_address)
controller.add_action(ControllerV1ActionEntry("test", "a test action"))

assert(server.registrar_add_controller(controller))
assert(server.registrar_probe(controller.id))

# Node

node = NodeV1("node", "a node")
assert(node.add_sensor(NodeV1SensorEntry("node_sensor", "[empty]", "[empty]")))
assert(server.registrar_add_node(node))

def callback_fn(requested_action):
   print("Controller ID: " + requested_action.controller_id + ", Action ID: " + requested_action.action_id)
   return

print("Starting server")
control_server_start(controller_address, callback_fn)

print("Sending Data")
try:
   while True:
      sleep(1)
      server.metric_submit_reading(ReadingV1(924204842, "node", "node_sensor", 42.0))

except KeyboardInterrupt:
   pass
finally:
   control_server_stop()
   assert(server.registrar_delete(controller_id))