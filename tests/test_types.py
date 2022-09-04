from pycrate import *

monolith = Monolith(IPV4Connection("0.0.0.0", 8080))

def test_node_v1():
   listed_sensors = [
      NodeV1SensorEntry("0", "test", "test node"),
      NodeV1SensorEntry("1", "test", "test node"),
      NodeV1SensorEntry("2", "test", "test node"),
      NodeV1SensorEntry("3", "test", "test node"),
      NodeV1SensorEntry("4", "test", "test node"),
   ]

   node = NodeV1("0000-0000-0000-0000", "A test node")

   for sensor in listed_sensors:
      assert(node.add_sensor(sensor))

   new_node = NodeV1("","")

   assert(new_node.decode_from(node.encode()))
   assert(new_node.id == node.id)
   assert(new_node.description == node.description)
   assert(len(new_node.sensors) == len(node.sensors))

   for x in range(0, len(new_node.sensors)):
      assert(new_node.sensors[x].id == node.sensors[x].id)
      assert(new_node.sensors[x].description == node.sensors[x].description)
      assert(new_node.sensors[x].type == node.sensors[x].type)

def test_reading_v1():
   reading = ReadingV1(monolith.get_timestamp(), "node_0", "0000-0000-0000-0000", 42.5)
   decoded_reading = ReadingV1(0,"","",0.0)
   assert(decoded_reading.decode_from(reading.encode()))
   assert(decoded_reading.timestamp == reading.timestamp)
   assert(decoded_reading.node_id == reading.node_id)
   assert(decoded_reading.sensor_id == reading.sensor_id)
   assert(decoded_reading.value == reading.value)

def test_streams_v1():

   listed_readings = [
      ReadingV1(monolith.get_timestamp(), "node", "sensor", 42.5),
      ReadingV1(monolith.get_timestamp(), "node", "sensor", 42.6),
      ReadingV1(monolith.get_timestamp(), "node", "sensor", 42.7),
      ReadingV1(monolith.get_timestamp(), "node", "sensor", 42.8),
      ReadingV1(monolith.get_timestamp(), "node", "sensor", 42.9),
      ReadingV1(monolith.get_timestamp(), "node", "sensor", 42.0),
   ]
   
   stream = StreamV1(monolith.get_timestamp(), 42)

   for reading in listed_readings:
      assert(stream.add_reading(reading))

   decoded_stream = StreamV1(monolith.get_timestamp() - 10, 99)
   decoded_stream.decode_from(stream.encode())

   assert(stream.timestamp == decoded_stream.timestamp)
   assert(stream.sequence == decoded_stream.sequence)
   assert(len(stream.readings) == len(decoded_stream.readings))

   for x in range(0, len(decoded_stream.readings)):
      assert(decoded_stream.readings[x].timestamp == stream.readings[x].timestamp)
      assert(decoded_stream.readings[x].node_id == stream.readings[x].node_id)
      assert(decoded_stream.readings[x].sensor_id == stream.readings[x].sensor_id)
      assert(decoded_stream.readings[x].value == stream.readings[x].value)


def test_action_v1():
   reading = ActionV1(monolith.get_timestamp(), "controller_0", "0000-0000-0000-0000", 42.5)
   decoded = ActionV1(0,"","",0.0)
   assert(decoded.decode_from(reading.encode()))
   assert(decoded.timestamp == reading.timestamp)
   assert(decoded.controller_id == reading.controller_id)
   assert(decoded.action_id == reading.action_id)
   assert(decoded.value == reading.value)

def test_controller_v1():
   listed_actions = [
      ControllerV1ActionEntry("0", "test action"),
      ControllerV1ActionEntry("1", "test action"),
      ControllerV1ActionEntry("2", "test action"),
      ControllerV1ActionEntry("3", "test action"),
      ControllerV1ActionEntry("4", "test action"),
   ]

   controller = ControllerV1("0000-0000-0000-0000", "A test controller", IPV4Connection("0.0.0.0", 6969))

   for action in listed_actions:
      assert(controller.add_action(action))

   new_controller = ControllerV1("","", IPV4Connection("bunk", 0))

   assert(new_controller.decode_from(controller.encode()))
   assert(new_controller.id == controller.id)
   assert(new_controller.description == controller.description)
   assert(len(new_controller.actions) == len(controller.actions))

   for x in range(0, len(controller.actions)):
      assert(new_controller.actions[x].id == controller.actions[x].id)
      assert(new_controller.actions[x].description == controller.actions[x].description)

def test_heartbeat_v1():
   heartbeat = HeartbeatV1("0000-0000-0000-0000")
   decoded = HeartbeatV1("")
   assert(decoded.decode_from(heartbeat.encode()))
   assert(decoded.id == heartbeat.id)

def test_version_v1():
   v = VersionV1("test_app", "91030123", "1", "2", "500")
   decoded = VersionV1("", "", "", "", "")
   assert(decoded.decode_from(v.encode()))
   assert(v.name == decoded.name)
   assert(v.hash == decoded.hash)
   assert(v.major == decoded.major)
   assert(v.minor == decoded.minor)
   assert(v.patch == decoded.patch)

print("Test NodeV1 type")
test_node_v1()

print("Test ReadingV1 type")
test_reading_v1()

print("Test StreamV1 type")
test_streams_v1()

print("Test ActionV1 type")
test_action_v1()

print("Test ControllerV1 type")
test_controller_v1()

print("Test HeartbeatV1 type")
test_heartbeat_v1()

print("Test VersionV1 type")
test_version_v1()