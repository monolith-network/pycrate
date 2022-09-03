from pycrate import *

listed_sensors = [
   NodeV1Sensor("0", "test", "test node"),
   NodeV1Sensor("1", "test", "test node"),
   NodeV1Sensor("2", "test", "test node"),
   NodeV1Sensor("3", "test", "test node"),
   NodeV1Sensor("4", "test", "test node"),
]

node = NodeV1("0000-0000-0000-0000", "A test node")

for sensor in listed_sensors:
   assert(node.add_sensor(sensor))

encoded = node.encode()

print(encoded)

new_node = NodeV1("","")

assert(new_node.decode_from(encoded))

assert(new_node.id == node.id)
assert(new_node.description == node.description)

for sensor in new_node.sensors:
   assert(sensor.id == sensor.id)
   assert(sensor.description == sensor.description)
   assert(sensor.type == sensor.type)