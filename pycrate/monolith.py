from sys import exit
from .types import *


class Monolith:
   def __init__(self, ipv4_address):
      if not isinstance(ipv4_address, IPV4Address):
         print("Given address must be an IPV4Address type")
         exit(1)