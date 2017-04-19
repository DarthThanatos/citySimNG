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
        print >> sys.stderr, 'waiting to receive'
        try:
            data, server = sock.recvfrom(1234)
        except Exception:
            print "Hold on, Jesus, not so fast"
        print >> sys.stderr, 'receiver: received sth:',data
        #msg = json.loads(data)
        viewSetter.passMsgToCurrentView(data)


class Sender:
    def __init__(self, sock):
        self.sock = sock

    def send(self, msg):
        self.sock.sendto(msg, ("127.0.0.1", 1234))
        print "Sender: sent",msg



def main():
    sender = Sender(sock)

    app = wx.PySimpleApp()
    screenDims = wx.GetDisplaySize()

    frame = MyFrame(None, wx.ID_ANY, "SDL Frame", screenDims, sender)
    frame.Show()

    thread.start_new_thread(receiver_func, (frame,))
    try:
        app.MainLoop()
    finally:
        print >>sys.stderr, 'closing socket'
        sock.close()

main()