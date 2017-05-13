import socket
import sys
import json
import thread
import wx

# Create a UDP socket
from ViewSetter import MyFrame

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 12345))



def receiver_func(viewSetter):
    while True:
        # Receive response
        #print >> sys.stderr, 'waiting to receive'
        try:
            data, server = sock.recvfrom(10000)
        except Exception:
            print "Hold on, Jesus, not so fast"
        #print >> sys.stderr, 'View receiver: received sth:',data
        viewSetter.passMsgToCurrentView(data)
        try:
            jsonObj = json.loads(data)
            uuid = jsonObj["UUID"]
            #print "Got UUID:", uuid, "from:",jsonObj["From"]
            msg = {}
            msg["UUID"] = uuid
            msg["To"] = jsonObj["From"]
            sock.sendto(json.dumps(msg),("localhost", 2468))
        except:
            # no uuid, sender does not want confirmation, skipping gracefully
            pass 


class Sender:
    def __init__(self, sock):
        self.sock = sock

    def send(self, msg):
        self.sock.sendto(msg, ("127.0.0.1", 1234))
        print "Sender: sent",msg

def wait_for_controller():
    TCP_IP = '127.0.0.1'
    TCP_PORT = 2468
    BUFFER_SIZE = 20  # Normally 1024, but we want fast response

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    conn, addr = s.accept()
    print 'Connection address:', addr
    conn.close()

def main():
    sender = Sender(sock)

    app = wx.PySimpleApp()
    screenDims = wx.GetDisplaySize()

    frame = MyFrame(None, wx.ID_ANY, "SDL Frame", screenDims, sender)
    frame.Show()

    thread.start_new_thread(receiver_func, (frame,))
    wait_for_controller()
    try:
        app.MainLoop()
    finally:
        print >>sys.stderr, 'closing socket'
        sock.close()

main()