import socket
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
a = {"To":"MenuModule", "UUID":"uuid"}
a_str = json.dumps(a)
print a_str
#sock.sendto(a_str, ("127.0.0.1", 2468))

msg = {}
msg["To"] = "MapNode"
msg["Operation"] = "PlaceBuilding"
msg["Args"] = {}
msg["Args"]["BuildingName"] = "name"
msg["Args"]["BuildingId"] = 1
stream = json.dumps(msg)
print stream