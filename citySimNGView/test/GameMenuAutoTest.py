from pywinauto import application

def preTest():
    # it is important to have the app already running in MainMenu panel at this point
    app = application.Application().connect(path="Mediator.exe")
    app['']['Load and mount New Game'].Click().Click()
    app[""].Wait("enabled")
    app['']['Game Menu'].Click().Click()
    app[""].Wait("enabled")
    return app #should return a hold to an app in the GameMenu panel

def toGameAndBack(app):
    app['']['Game'].Click().Click()
    app[""].Wait("enabled",timeout=30)
    app[""]["Menu"].Click()
    app[""].Wait("enabled")

def toTutorialAndBack(app):
    # Now we should be in the Creator Main Panel
    app['']['Tutorial'].Click().Click()
    app[""].Wait("enabled")
    app[""]["Menu"].Click().Click()
    app[""].Wait("enabled")
    # app[""].print_control_identifiers()
    # app[""]["Exchange"].Click().Click()
    # app[""].print_control_identifiers()

def postTest(app):
    # it is important to have an app in GameMenu panel at this point
    app['']['Back to Loader'].Click().Click()
    app[""].Wait("enabled")
    app['']['Main Menu'].Click().Click()
    app[""].Wait("enabled")

app = preTest()
toTutorialAndBack(app)
toGameAndBack(app)
#if at this point no exception has been thrown, we assume transitions to various panels work correctly in GameMenu panel
postTest(app)
