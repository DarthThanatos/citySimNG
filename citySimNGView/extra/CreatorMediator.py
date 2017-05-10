import socket
import sys
import json

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 12345))

try:

    # Receive response
    print >>sys.stderr, 'waiting to receive'
    data, server = sock.recvfrom(1234)
    print >>sys.stderr, 'received "%s"' % data
    sock.sendto("Got msg", ("127.0.0.1", 1234))
    msg = json.loads(data)
    print msg["pageInfo"]
finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
