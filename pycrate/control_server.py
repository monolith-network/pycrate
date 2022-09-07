from sqlite3 import connect
from .types import IPV4Connection
import socket
import threading
from sys import exit
from .types import ActionV1

server_thread = None
start_thread = None
continue_serving = True

def new_conn(socket, callback_fn):
   global continue_serving
   while continue_serving:
      sock, address = socket.accept()
      actual_data = None
      try:
         data_len = int.from_bytes(sock.recv(4), "little")
         actual_data = sock.recv(data_len)
      except:
         continue
      
      if actual_data is not None:
         action = ActionV1(0,"","",0.0)
         if action.decode_from(actual_data.decode("utf-8")):
            callback_fn(action)

def start(connection, callback_fn):
   if not isinstance(connection, IPV4Connection):
      raise Exception("Connection must be an IPV4Connection")

   global server_thread
   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   sock.bind((connection.address, connection.port))
   sock.listen(5)
   server_thread = threading.Thread(target=new_conn, args=(sock, callback_fn))
   server_thread.start()

def control_server_start(connection, callback_fn):
   global start_thread
   start_thread = threading.Thread(target=start, args=(connection, callback_fn))
   start_thread.start()
   
def control_server_stop():
   global continue_serving
   continue_serving = False
   try:
      server_thread.join()
      start_thread.join()
   except:
      exit(0)
