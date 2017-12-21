from time import sleep

from pywinauto import application

def preTest():
    return application.Application().connect(path="Mediator.exe")
    # it is important to have the app already running in MainMenu panel at this point

def toLoaderAndBack(app):
    app['']['Load and mount New Game'].Click().Click()
    app[""].Wait("enabled")
    app[""]["Main Menu"].Click().Click()

def toCreatorAndBack(app):
    # Now we should be in the Creator Main Panel
    app[""].Wait("enabled")
    app[""]["Creator"].Click().Click()
    app.top_window().print_control_identifiers()

    # Now we are in Creator
    app[""].Wait("enabled")
    app[""]["Menu"].Click().Click()

def testExit(app):
    # Now we should be back in the Main Menu panel
    app[""].Wait("enabled")
    app[""]["Exit"].Click().Click()
    sleep(5)
    print app.is_process_running()

app = preTest()
toLoaderAndBack(app)
toCreatorAndBack(app)
#if at this point no exception has been thrown, we assume transitions to various panels work correctly in MainMenu panel
testExit(app)