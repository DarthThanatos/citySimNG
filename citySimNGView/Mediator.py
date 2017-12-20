import socket
import sys
import json
import threading
import traceback

import wx
from py4j.clientserver import ClientServer, JavaParameters, PythonParameters
from py4j.java_gateway import JavaGateway, GatewayParameters
import logging

from LoadingScreen import LoadingScreen
from ViewSetter import MyFrame
from viewmodel.ViewModel import ViewModel

def receiver_func(viewSetter):
    global sock
    while True:
        # Receive response from model
        try:
            data, server = sock.recvfrom(1000000)
        except Exception:
            traceback.print_exc()
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

def wait_for_controller(loading_screen):
    print "waiting for logic to connect..."
    global sender, sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sender = Sender(sock)
    sock.bind(('', 12345))
    TCP_IP = '127.0.0.1'
    TCP_PORT = 2468
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    conn, addr = s.accept()
    conn.close()
    wx.CallAfter(loading_screen.closeWindow)

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

class EngineApp(wx.App):
    def __init__(self):
        wx.App.__init__(self, redirect=False)

    def OnInit(self):  #called by wx.Python

        print "on init"
        # turn on debug mode
        if '--d' in sys.argv or '--debug' in sys.argv:
            turn_on_debug()

        loading_screen = LoadingScreen("resources\\sysFiles\\images\\loading.gif")
        loading_screen.Show()
        print "loading screen shown"

        t = InitializingThread(loading_screen)
        t.start()  #calls t.run()
        return True


class InitializingThread(threading.Thread):
    def __init__(self, loading_screen):
        threading.Thread.__init__(self)
        self.loading_screen = loading_screen

    def run(self):
        global javagateway, sender
        javagateway = JavaGateway(gateway_parameters=GatewayParameters(port=25335))
        wx.CallAfter(self.init_frame, None, javagateway)

    def init_frame(self, sender, javagateway):
        global gateway
        screenDims = wx.GetDisplaySize()
        frame = MyFrame(None, wx.ID_ANY, "Engine Frame", screenDims, sender, javagateway)
        gateway = startViewModelListener(frame)
        threading._start_new_thread(wait_for_controller,(self.loading_screen,))

def customAppMain():
    print "initializing app"
    app = EngineApp()

    try:
        app.MainLoop()
    finally:
        global gateway, javagateway, sock
        print "closing sockets"
        sock.close()
        javagateway.close()
        gateway.close()
        sys.exit()


def main():
    sender = Sender(sock)

    # turn on debug mode
    if '--d' in sys.argv or '--debug' in sys.argv:
        turn_on_debug()

    javagateway = JavaGateway(gateway_parameters=GatewayParameters(port=25335))

    # app = wx.PySimpleApp()
    app = wx.App(False)
    screenDims = wx.GetDisplaySize()

    loading_screen = LoadingScreen("resources\\sysFiles\\images\\loading.gif")
    frame = MyFrame(None, wx.ID_ANY, "SDL Frame", screenDims, sender, javagateway)

    # thread.start_new_thread(receiver_func, (frame,))
    gateway = startViewModelListener(frame)

    # frame.Show()
    wait_for_controller()
    try:
        app.MainLoop()
    finally:
        logging.info("closing sockets")
        sock.close()
        gateway.close()
        javagateway.close()
        sys.exit()


# main()
customAppMain()
