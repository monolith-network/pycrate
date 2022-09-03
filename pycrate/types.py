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

   Object representing a V1 Node Sensor
"""
class NodeV1Sensor:
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
   def add_sensor(self, v1_sensor):
      for sensor in self.sensors:
         if sensor.id == v1_sensor.id:
            print("Can not have duplicate sensor ids")
            return False
      self.sensors.append(v1_sensor)
      return True

   """Documentation for a method.

      Encode node to json string
      returns encoded node
   """
   def encode(self):
      encoded = "{{\"id\":\"{0}\",\"description\":\"{1}\",\"sensors\":[".format(self.id, self.description)
      for sensor in self.sensors:
         encoded += "{{\"id\":\"{0}\",\"type\":\"{1}\",\"description\":\"{2}\"}},".format(sensor.id, sensor.type, sensor.description)
      if len(self.sensors) > 0:
         encoded = encoded[:-1]
      encoded += "]}"
      return encoded

   """Documentation for a method.

      Attempt to build a node from an encoded string
      returns true iff the node could be built from the string
   """
   def decode_from(self, encoded_node):
      decoded = json.loads(encoded_node)
      if decoded is None:
         print("Failed to parse data")
         return False

      self.id = decoded["id"]
      self.description = decoded["description"]
      for sensor in decoded["sensors"]:
         self.sensors.append(NodeV1Sensor(sensor["id"], sensor["type"], sensor["description"]))
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

      self.timestamp = id
      self.node_id = node_id
      self.sensor_id = sensor_id
      self.value = value

   """Documentation for a method.

      Encode node to json string
      returns encoded node
   """
   def encode(self):
      encoded = "{{\"id\":\"{0}\",\"description\":\"{1}\",\"sensors\":[".format(self.id, self.description)
      for sensor in self.sensors:
         encoded += "{{\"id\":\"{0}\",\"type\":\"{1}\",\"description\":\"{2}\"}},".format(sensor.id, sensor.type, sensor.description)
      if len(self.sensors) > 0:
         encoded = encoded[:-1]
      encoded += "]}"
      return encoded

   """Documentation for a method.

      Attempt to build a node from an encoded string
      returns true iff the node could be built from the string
   """
   def decode_from(self, encoded_node):
      decoded = json.loads(encoded_node)
      if decoded is None:
         print("Failed to parse data")
         return False

      self.id = decoded["id"]
      self.description = decoded["description"]
      for sensor in decoded["sensors"]:
         self.sensors.append(NodeV1Sensor(sensor["id"], sensor["type"], sensor["description"]))
      return True