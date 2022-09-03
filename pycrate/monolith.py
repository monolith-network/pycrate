from time import time
import urllib.request, urllib.parse
import json
from .types import *


"""Documentation for a class.

   Object to interact with a monolith
"""
class Monolith:
   def __init__(self, ipv4_address):
      if not isinstance(ipv4_address, IPV4Address):
         raise Exception("Given address must be an IPV4Address type")
      self.host = "http://" + ipv4_address.url + ":" + str(ipv4_address.port)

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

      Probe the registrar for a node
      Returns None iff the command fails,
              True if the item was found
              and False if the item was not found
   """
   def registrar_probe(self, node):
      if not isinstance(node, NodeV1):
         raise Exception("NODE must be of type NodeV1")

      response = self.fetch_endpoint("/registrar/probe/" + node.id)

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

      Delete a node. 
      Returns None iff the command fails,
      True if the command worked, False otherwise

      Note: The deletion endpoint returns success unless there was
             an internal error - This means that if you attempt to
             delete something that didn't exist, it will still return
             success as long as no internal errors occurred.
   """
   def registrar_delete_node(self, id):
      if not isinstance(id, str):
         raise Exception("ID must be of type string")
      
      response = self.fetch_endpoint("/registrar/delete/" + id)

      if response is None:
         return None

      decoded_response = json.loads(response)

      if decoded_response["status"] == 200 and decoded_response["data"] == "success":
         return True
      return False