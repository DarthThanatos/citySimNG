"""
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

"""
# main()