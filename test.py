import os
import socket


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("192.168.101.1", 80))
ipAddr = s.getsockname()[0]
s.close()

host = list(os.uname())
print("HOSTNAME: %s" % host[1])
print("IP Address: %s" % ipAddr)