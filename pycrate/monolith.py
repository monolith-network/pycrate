from time import time
from .types import *



class Monolith:
   def __init__(self, ipv4_address):
      if not isinstance(ipv4_address, IPV4Address):
         raise Exception("Given address must be an IPV4Address type")

   def get_timestamp(self):
      return int(time())