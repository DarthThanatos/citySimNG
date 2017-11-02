import socket
import sys
import json
import thread
import traceback

import wx
from py4j.clientserver import ClientServer, JavaParameters, PythonParameters
from py4j.java_gateway import JavaGateway, GatewayParameters
import logging

from ViewSetter import MyFrame
from viewmodel.ViewModel import ViewModel

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 12345))

def receiver_func(viewSetter):
    while True:
        # Receive response from model
        try:
            data, server = sock.recvfrom(1000000)
        except Exception:
            traceback.print_exc()
            print "Hold on, Jesus, not so fast"
        wx.CallAfter(viewSetter.passMsgToCurrentView, data)
        try:
            jsonObj = json.loads(data)
            uuid = jsonObj["UUID"]
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
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    conn, addr = s.accept()
    conn.close()

def startViewModelListener(viewSetter):
    viewModel = ViewModel(viewSetter)
    return ClientServer(
        java_parameters=JavaParameters(),
        python_parameters=PythonParameters(),
        python_server_entry_point=viewModel)

def turn_on_debug():
    logger = logging.getLogger("py4j")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

def main():
    sender = Sender(sock)

    # turn on debug mode
    if '--d' in sys.argv or '--debug' in sys.argv:
        turn_on_debug()

    # app = wx.PySimpleApp()
    app = wx.App(False)
    screenDims = wx.GetDisplaySize()

    javagateway = JavaGateway(gateway_parameters=GatewayParameters(port=25335))
    frame = MyFrame(None, wx.ID_ANY, "SDL Frame", screenDims, sender, javagateway)
    # thread.start_new_thread(receiver_func, (frame,))
    gateway = startViewModelListener(frame)

    # frame.Show()
    wait_for_controller()
    try:
        app.MainLoop()
    finally:
        print >>sys.stderr, 'closing sockets'
        sock.close()
        gateway.close()
        javagateway.close()
        sys.exit()

main()