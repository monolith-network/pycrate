import json

"""Documentation for a class.

   Object representing an ipv4 address and port
"""
class IPV4Address:
   def __init__(self, url, port):
      if not isinstance(url, str):
         raise Exception("URL Must be a string")
      if not isinstance(port, int):
         raise Exception("PORT Must be an int")
      self.url = url
      self.port = port

"""Documentation for a class.

   Object representing a V1 Node Sensor entry
"""
class NodeV1SensorEntry:
   def __init__(self, id, type, description):
      if not isinstance(id, str):
         raise Exception("ID be a string")
      if not isinstance(type, str):
         raise Exception("TYPE be a string")
      if not isinstance(description, str):
         raise Exception("DESCRIPTION Must be a string")
      self.id = id
      self.type = type
      self.description = description
      
   """Documentation for a method.

      Encode action to json string
      returns encoded entry
   """
   def encode(self):
      encoded = "{{\"id\":\"{0}\",\"type\":\"{1}\",\"description\":\"{2}\"}}".format(
         self.id, 
         self.type, 
         self.description
      )
      return encoded

   """Documentation for a method.

      Attempt to build an entry from an encoded string
      returns true iff the action could be built from the string
   """
   def decode_from(self, encoded):
      decoded = json.loads(encoded)
      if decoded is None:
         print("Failed to parse data")
         return False

      self.id = decoded["id"]
      self.type = decoded["type"]
      self.description = decoded["description"]
      return True

"""Documentation for a class.

   Object representing a V1 Node
"""
class NodeV1:
   def __init__(self, id, description):
      if not isinstance(id, str):
         raise Exception("ID be a string")
      if not isinstance(description, str):
         raise Exception("DESCRIPTION Must be a string")
      self.id = id
      self.description = description
      self.sensors = []

   """Documentation for a method.

      Add a sensor to the sensor list and ensure that its unique
      returns true iff the item could be added
   """
   def add_sensor(self, sensor):
      if not isinstance(sensor, NodeV1SensorEntry):
         print("SENSOR must be a NodeV1SensorEntry object")
         return False

      encoded = sensor.encode()
      if not sensor.decode_from(encoded):
         print("Invalid sensor")
         return False

      self.sensors.append(sensor)
      return True

   """Documentation for a method.

      Encode node to json string
      returns encoded node
   """
   def encode(self):
      encoded = "{{\"id\":\"{0}\",\"description\":\"{1}\",\"sensors\":[".format(self.id, self.description)
      for sensor in self.sensors:
         encoded += sensor.encode() + ","
      if len(self.sensors) > 0:
         encoded = encoded[:-1]
      encoded += "]}"
      return encoded

   """Documentation for a method.

      Attempt to build a node from an encoded string
      returns true iff the node could be built from the string
   """
   def decode_from(self, encoded_node):
      self.sensors = []
      decoded = json.loads(encoded_node)
      if decoded is None:
         print("Failed to parse data")
         return False

      self.id = decoded["id"]
      self.description = decoded["description"]
      for sensor in decoded["sensors"]:
         self.sensors.append(NodeV1SensorEntry(sensor["id"], sensor["type"], sensor["description"]))
      return True

"""Documentation for a class.

   Object representing a V1 Node
"""
class ReadingV1:
   def __init__(self, timestamp, node_id, sensor_id, value):
      if not isinstance(timestamp, int):
         raise Exception("TIMESTAMP Must be an int")
      if not isinstance(node_id, str):
         raise Exception("NODE ID Must be a string")
      if not isinstance(sensor_id, str):
         raise Exception("SENSOR ID Must be a string")
      if not isinstance(value, float):
         raise Exception("VALUE must be a float")

      self.timestamp = timestamp
      self.node_id = node_id
      self.sensor_id = sensor_id
      self.value = value

   """Documentation for a method.

      Encode reading to json string
      returns encoded node
   """
   def encode(self):
      encoded = "{{\"timestamp\":{0},\"node_id\":\"{1}\",\"sensor_id\":\"{2}\",\"value\":{3}}}".format(
         self.timestamp, self.node_id, self.sensor_id, self.value
      )

      return encoded

   """Documentation for a method.

      Attempt to build a node from an encoded string
      returns true iff the reading could be built from the string
   """
   def decode_from(self, encoded_node):
      decoded = json.loads(encoded_node)
      if decoded is None:
         print("Failed to parse data")
         return False

      self.timestamp = decoded["timestamp"]
      self.node_id = decoded["node_id"]
      self.sensor_id = decoded["sensor_id"]
      self.value = decoded["value"]
      return True
      
"""Documentation for a class.

   Object representing a V1 Stream
"""
class StreamV1:
   def __init__(self, timestamp, sequence):
      if not isinstance(timestamp, int):
         raise Exception("TIMESTAMP Must be an int")
      if not isinstance(sequence, int):
         raise Exception("SEQUENCE Must be an int")

      self.timestamp = timestamp
      self.sequence = sequence
      self.readings = []

   """Documentation for a method.

      Add a metric reading to the stream
   """
   def add_reading(self, reading):
      if not isinstance(reading, ReadingV1):
         print("READING must be a ReadingV1 object")
         return False

      encoded_reading = reading.encode()
      if not reading.decode_from(encoded_reading):
         print("Invalid reading")
         return False

      self.readings.append(reading)
      return True

   """Documentation for a method.

      Encode to json string
      returns encoded stream
   """
   def encode(self):
      encoded = "{{\"timestamp\":{0},\"sequence\":{1},\"data\":[".format(self.timestamp, self.sequence)
      for reading in self.readings:
         encoded += reading.encode() + ","
      if len(self.readings) > 0:
         encoded = encoded[:-1]
      encoded += "]}"
      return encoded

   """Documentation for a method.

      Attempt to build a stream from an encoded string
      returns true iff the stream could be built from the string
   """
   def decode_from(self, encoded_stream):
      self.readings = []
      decoded = json.loads(encoded_stream)
      if decoded is None:
         print("Failed to parse data")
         return False

      self.timestamp = decoded["timestamp"]
      self.sequence = decoded["sequence"]
      for reading in decoded["data"]:
         self.readings.append(ReadingV1(reading["timestamp"], reading["node_id"], reading["sensor_id"], reading["value"]))
      return True

"""Documentation for a class.

   Object representing a V1 Action
"""
class ActionV1:
   def __init__(self, timestamp, controller_id, action_id, value):
      if not isinstance(timestamp, int):
         raise Exception("TIMESTAMP Must be an int")
      if not isinstance(controller_id, str):
         raise Exception("CONTROLLER ID Must be a string")
      if not isinstance(action_id, str):
         raise Exception("ACTION ID Must be a string")
      if not isinstance(value, float):
         raise Exception("VALUE must be a float")

      self.timestamp = timestamp
      self.controller_id = controller_id
      self.action_id = action_id
      self.value = value

   """Documentation for a method.

      Encode action to json string
      returns encoded node
   """
   def encode(self):
      encoded = "{{\"timestamp\":{0},\"controller_id\":\"{1}\",\"action_id\":\"{2}\",\"value\":{3}}}".format(
         self.timestamp, self.controller_id, self.action_id, self.value
      )

      return encoded

   """Documentation for a method.

      Attempt to build a action from an encoded string
      returns true iff the node could be built from the string
   """
   def decode_from(self, encoded_node):
      decoded = json.loads(encoded_node)
      if decoded is None:
         print("Failed to parse data")
         return False

      self.timestamp = decoded["timestamp"]
      self.controller_id = decoded["controller_id"]
      self.action_id = decoded["action_id"]
      self.value = decoded["value"]
      return True

      

"""Documentation for a class.

   Object representing a V1 Controller's action entry
"""
class ControllerV1ActionEntry:
   def __init__(self, id, description):
      if not isinstance(id, str):
         raise Exception("ID be a string")
      if not isinstance(description, str):
         raise Exception("DESCRIPTION Must be a string")
      self.id = id
      self.description = description

   """Documentation for a method.

      Encode action to json string
      returns encoded entry
   """
   def encode(self):
      encoded = "{{\"id\":\"{0}\",\"description\":\"{1}\"}}".format(
         self.id, self.description
      )

      return encoded

   """Documentation for a method.

      Attempt to build a entry from an encoded string
      returns true iff the action could be built from the string
   """
   def decode_from(self, encoded):
      decoded = json.loads(encoded)
      if decoded is None:
         print("Failed to parse data")
         return False

      self.id = decoded["id"]
      self.description = decoded["description"]
      return True

"""Documentation for a class.

   Object representing a V1 Controller
"""
class ControllerV1:
   def __init__(self, id, description):
      if not isinstance(id, str):
         raise Exception("ID Must be an string")
      if not isinstance(description, str):
         raise Exception("DESCRIPTION Must be a string")

      self.id = id
      self.description = description
      self.actions = []

   """Documentation for a method.

      Add an action reading to the controller
   """
   def add_action(self, action):
      if not isinstance(action, ControllerV1ActionEntry):
         print("ACTION must be a ControllerV1ActionEntry object")
         return False

      encoded = action.encode()
      if not action.decode_from(encoded):
         print("Invalid action")
         return False

      self.actions.append(action)
      return True

   """Documentation for a method.

      Encode to json string
      returns encoded controller
   """
   def encode(self):
      encoded = "{{\"id\":\"{0}\",\"description\":\"{1}\",\"actions\":[".format(self.id, self.description)
      for action in self.actions:
         encoded += action.encode() + ","
      if len(self.actions) > 0:
         encoded = encoded[:-1]
      encoded += "]}"
      return encoded

   """Documentation for a method.

      Attempt to build a controller from an encoded string
      returns true iff the controller could be built from the string
   """
   def decode_from(self, encoded):
      self.actions = []
      decoded = json.loads(encoded)
      if decoded is None:
         print("Failed to parse data")
         return False

      self.id = decoded["id"]
      self.description = decoded["description"]
      for action in decoded["actions"]:
         self.actions.append(ControllerV1ActionEntry(action["id"], action["description"]))
      return True