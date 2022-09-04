from time import time
import threading
import urllib.request, urllib.parse
import json
from .types import *

"""Documentation for a class.

   Object to interact with a monolith
"""
class Monolith:
   def __init__(self, ipv4_address):
      if not isinstance(ipv4_address, IPV4Connection):
         raise Exception("Given address must be an IPV4Connection type")
      self.host = "http://" + ipv4_address.address + ":" + str(ipv4_address.port)
      self.server_thread = None

   """Documentation for a method.

      Retrieve a timestamp that conforms to the monolith standard
   """
   def get_timestamp(self):
      return int(time())

   """Documentation for a method.

      Fetch a particular endpoing from monolith.
      If a problem occurs, None will be returned
   """
   def fetch_endpoint(self, endpoint):
      target_url = self.host +  urllib.parse.quote(endpoint)
      try: return urllib.request.urlopen(target_url).read()
      except:
         return None

   """Documentation for a method.

      Check if we are connected to a monolith
      Returns None if there was a problem
   """
   def is_connected(self):
      if self.fetch_endpoint("/") is None:
         return False
      return True

   """Documentation for a method.

      Attempt to retrieve the version info of the endpoint
      Returns None iff the command fails,
      True if the command worked, False otherwise
   """
   def get_version(self):

      s_time = str(time)
      response = self.fetch_endpoint("/version")
      if response is None:
         return None

      decoded_response = json.loads(response)

      if decoded_response["status"] == 200:
         data = decoded_response["data"]
         return VersionV1(data["name"], 
                           data["hash"],
                           data["version_major"],
                           data["version_minor"],
                           data["version_patch"])
      return False

   """Documentation for a method.

      Register a node with Monolith
      Returns None iff the command fails,
              True if the item was added,
              and False otherwise
   """
   def registrar_add_node(self, node):
      if not isinstance(node, NodeV1):
         raise Exception("NODE must be of type NodeV1")

      encoded = node.encode()

      response = self.fetch_endpoint("/registrar/add/" + node.id + "/" + encoded)

      if response is None:
         return None

      decoded_response = json.loads(response)

      if decoded_response["status"] == 200 and decoded_response["data"] == "success":
         return True
      return False

   """Documentation for a method.

      Register a controller with Monolith
      Returns None iff the command fails,
              True if the item was added,
              and False otherwise
   """
   def registrar_add_controller(self, controller):
      if not isinstance(controller, ControllerV1):
         raise Exception("NODE must be of type controller")

      encoded = controller.encode()

      response = self.fetch_endpoint("/registrar/add/" + controller.id + "/" + encoded)

      if response is None:
         return None

      decoded_response = json.loads(response)

      if decoded_response["status"] == 200 and decoded_response["data"] == "success":
         return True
      return False

   """Documentation for a method.

      Probe the registrar for a node
      Returns None iff the command fails,
              True if the item was found
              and False if the item was not found
   """
   def registrar_probe(self, id):
      if not isinstance(id, str):
         raise Exception("ID must be of type str")

      response = self.fetch_endpoint("/registrar/probe/" + id)

      if response is None:
         return None

      decoded_response = json.loads(response)

      if decoded_response["status"] == 200 and decoded_response["data"] == "found":
         return True
      return False

   """Documentation for a method.

      Attempt to retrieve a node from the registrar
      Returns None if the command fails, or if the returned 
      data from the server was insufficient to construct a node.
      If everything works, a NodeV1 object will be returned
   """
   def registrar_fetch_node(self, id):
      if not isinstance(id, str):
         raise Exception("ID must be of type string")
      
      response = self.fetch_endpoint("/registrar/fetch/" + id)

      if response is None:
         return None

      decoded_response = json.loads(response)

      # A status indicates that the query worked but there was no node
      if "status" in decoded_response:
         return None

      # Attempt to convert the reponse into a node
      node = NodeV1("","")
      if not node.decode_from(response):
         raise Exception("Data from server did not match a V1 Node (is something on fire?)")

      return node

   """Documentation for a method.

      Attempt to retrieve a controller from the registrar
      Returns None if the command fails, or if the returned 
      data from the server was insufficient to construct a controller.
      If everything works, a ControllerV1 object will be returned
   """
   def registrar_fetch_controller(self, id):
      if not isinstance(id, str):
         raise Exception("ID must be of type string")
      
      response = self.fetch_endpoint("/registrar/fetch/" + id)

      if response is None:
         return None

      decoded_response = json.loads(response)

      # A status indicates that the query worked but there was no node
      if "status" in decoded_response:
         return None

      # Attempt to convert the reponse into a controller
      controller = ControllerV1("","",IPV4Connection("", 0))
      if not controller.decode_from(response):
         raise Exception("Data from server did not match a V1 Controller (is something on fire?)")

      return controller

   """Documentation for a method.

      Delete a node. 
      Returns None iff the command fails,
      True if the command worked, False otherwise

      Note: The deletion endpoint returns success unless there was
             an internal error - This means that if you attempt to
             delete something that didn't exist, it will still return
             success as long as no internal errors occurred.
   """
   def registrar_delete(self, id):
      if not isinstance(id, str):
         raise Exception("ID must be of type string")
      
      response = self.fetch_endpoint("/registrar/delete/" + id)

      if response is None:
         return None

      decoded_response = json.loads(response)

      if decoded_response["status"] == 200 and decoded_response["data"] == "success":
         return True
      return False

   """Documentation for a method.

      Register a metric stream receiver
      Returns None iff the command fails,
      True if the command worked, False otherwise
   """
   def metric_stream_add(self, destination):
      if not isinstance(destination, IPV4Connection):
         raise Exception("DESTINATION must be of type IPV4Connection")
      
      response = self.fetch_endpoint("/metric/stream/add/" + 
                                       destination.address +
                                       "/" +
                                       str(destination.port))
      if response is None:
         return None

      decoded_response = json.loads(response)

      if decoded_response["status"] == 200 and decoded_response["data"] == "success":
         return True
      return False

   """Documentation for a method.

      Delete a metric stream receiver
      Returns None iff the command fails,
      True if the command worked, False otherwise
   """
   def metric_stream_delete(self, destination):
      if not isinstance(destination, IPV4Connection):
         raise Exception("DESTINATION must be of type IPV4Connection")
      
      response = self.fetch_endpoint("/metric/stream/delete/" + 
                                       destination.address +
                                       "/" +
                                       str(destination.port))
      if response is None:
         return None

      decoded_response = json.loads(response)

      if decoded_response["status"] == 200 and decoded_response["data"] == "success":
         return True
      return False

   """Documentation for a method.

      Submit a reading 
      Returns None iff the command fails,
      True if the command worked, False otherwise
   """
   def metric_submit_reading(self, reading):
      if not isinstance(reading, ReadingV1):
         raise Exception("READING must be of type ReadingV1")

      encoded_reading = reading.encode()

      response = self.fetch_endpoint("/metric/submit/" + encoded_reading)
      if response is None:
         return None

      decoded_response = json.loads(response)

      if decoded_response["status"] == 200 and decoded_response["data"] == "success":
         return True
      return False

   """Documentation for a method.

      Submit a heartbeat for a node 
      Returns None iff the command fails,
      True if the command worked, False otherwise
   """
   def metric_submit_heartbeat(self, heartbeat):
      if not isinstance(heartbeat, HeartbeatV1):
         raise Exception("HEARTBEAT must be of type HeartbeatV1")
         
      encoded_heartbeat = heartbeat.encode()

      response = self.fetch_endpoint("/metric/heartbeat/" + encoded_heartbeat)
      if response is None:
         return None

      decoded_response = json.loads(response)

      if decoded_response["status"] == 200 and decoded_response["data"] == "success":
         return True
      return False

   """Documentation for a method.

      Attempt to retrieve a list of registered node ids
      Returns None iff the command fails,
      True if the command worked, False otherwise
   """
   def metric_fetch_nodes(self):

      s_time = str(time)
      response = self.fetch_endpoint("/metric/fetch/nodes")
      if response is None:
         return None

      decoded_response = json.loads(response)

      if decoded_response["status"] == 200:
         return decoded_response["data"]
      return False

   """Documentation for a method.

      Attempt to retrieve a list of sensor ids for the given node
      Returns None iff the command fails,
      True if the command worked, False otherwise
   """
   def metric_fetch_sensors(self, node_id):
      if not isinstance(node_id, str):
         raise Exception("NODE ID must be of type string")

      s_time = str(time)
      response = self.fetch_endpoint("/metric/fetch/" + 
                                     node_id +
                                     "/sensors")
      if response is None:
         return None

      decoded_response = json.loads(response)

      if decoded_response["status"] == 200:
         return decoded_response["data"]
      return False

   """Documentation for a method.

      Fetch a metrics from a specified range of time
      Returns None iff the command fails,
      True if the command worked, False otherwise
   """
   def metric_fetch_range(self, node_id, start, end):
      if not isinstance(node_id, str):
         raise Exception("NODE ID must be of type string")
      if not isinstance(start, int):
         raise Exception("START must be of type int")
      if not isinstance(end, int):
         raise Exception("END must be of type int")
      if start > end:
         raise Exception("Start must not be after end")
      if start == end:
         raise Exception("Start and end can not be the same")

      s_start = str(start)
      s_end = str(end)
      response = self.fetch_endpoint("/metric/fetch/" + 
                                     node_id +
                                     "/range/" + 
                                     s_start +
                                     "/" +
                                     s_end)
      if response is None:
         return None

      decoded_response = json.loads(response)

      if decoded_response["status"] == 200:
         return decoded_response["data"]
      return False

   """Documentation for a method.

      Fetch a metrics after a specified time
      Returns None iff the command fails,
      True if the command worked, False otherwise
   """
   def metric_fetch_after(self, node_id, time):
      if not isinstance(node_id, str):
         raise Exception("NODE ID must be of type string")
      if not isinstance(time, int):
         raise Exception("TIME must be of type int")
      if time > self.get_timestamp():
         raise Exception("Given time exceeds current time (The future) ")

      s_time = str(time)
      response = self.fetch_endpoint("/metric/fetch/" + 
                                     node_id +
                                     "/after/" + 
                                     s_time)
      if response is None:
         return None

      decoded_response = json.loads(response)

      if decoded_response["status"] == 200:
         return decoded_response["data"]
      return False

   """Documentation for a method.

      Fetch a metrics after a specified time
      Returns None iff the command fails,
      True if the command worked, False otherwise
   """
   def metric_fetch_before(self, node_id, time):
      if not isinstance(node_id, str):
         raise Exception("NODE ID must be of type string")
      if not isinstance(time, int):
         raise Exception("TIME must be of type int")
      if time > self.get_timestamp():
         raise Exception("Given time exceeds current time (The future) ")

      s_time = str(time)
      response = self.fetch_endpoint("/metric/fetch/" + 
                                     node_id +
                                     "/before/" + 
                                     s_time)
      if response is None:
         return None

      decoded_response = json.loads(response)

      if decoded_response["status"] == 200:
         return decoded_response["data"]
      return False
