from time import sleep

from pywinauto import application

def preTest():
    # it is important to have the app already running in MainMenu panel at this point
    app = application.Application().connect(path="Mediator.exe")
    app['']['Load and mount New Game'].Click().Click()
    app[""].Wait("enabled")
    return app #should return a hold to an app in the Loader panel


def testShowDetailsBeforeShown(app):
    # at this point nothing should be displayed on "graph details" panel
    show_details_btns = app[""].children(title = "Show Details")
    for button_title in ["Show details1", "Show Details2", "Show Details3"]:
        print "checking if ", button_title, "is not enabled...",
        if not app[""][button_title].IsEnabled(): print "PASSED"
        else: print "FAILED"


def testListBox(app):
    #check if default names are in list
    app[""].ListBox.select("Moon")
    app[""]["Show graphs"].Click()
    sleep(1)
    app[""].ListBox.select("Stronghold")
    app[""]["Show graphs"].Click()
    sleep(1)

def testShowDetailsAfterShown(app):
    # at this point, sth should be displayed on graph details panel
    details_map = {"Show details1" : "Details of Resources", "Show Details2" : "Details of Dwellers", "Show Details3": "Details of Buildings"}
    for button_title in details_map.keys():
        print "checking if ", button_title, "is not enabled after dialog shows...",
        try:
            app[""][button_title].Click().Click().Click()
        except Exception:
            pass
        app.Window_(title = details_map[button_title]).Wait("enabled", timeout = 30)
        if not app[""][button_title].IsEnabled():
            print "PASSED"
        else:
            print "FAILED"
        sleep(1)
        app.Window_(title=details_map[button_title]).Exit.Click()

def postTest(app):
    # it is important to have an app in Loader panel at this point
    app['']['Main Menu'].Click().Click()
    app[""].Wait("enabled")

app = preTest()
testShowDetailsBeforeShown(app)
testListBox(app)
testShowDetailsAfterShown(app)

#if at this point no exception has been thrown, we assume transitions to various panels work correctly in GameMenu panel
postTest(app)
