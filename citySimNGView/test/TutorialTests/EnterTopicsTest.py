from time import sleep
from pywinauto import application

def preTest():
    #app in MainMenu
    app = application.Application().connect(path="Mediator.exe")
    app['']['Load and mount New Game'].Click().Click()
    app[""].Wait("enabled")
    app['']['Game Menu'].Click().Click()
    app[""].Wait("enabled")
    app['']['Tutorial'].Click().Click()
    app[""].Wait("enabled")
    return app 

def testTab(app, nrOfTopics, tabID):
    for i in range(nrOfTopics):
        app['']['TabBtn'+str(tabID*100 + i)].Click().Click()
        app[""].Wait("enabled")
        app['']['contents'].Click().Click()
        app[""].Wait("enabled")
        print ("Tab " + str(tabID) + " Button " + str(i))


def toTutorialAndBack(app):
    #app in Tutorial
    #app.top_window().print_control_identifiers()

    #test tab1
    testTab(app, 8, 1)
    raw_input("Switch to second tab. Then press Enter to continue...")

    #test tab2 
    testTab(app, 16, 2)
    raw_input("Switch to third tab. Then press Enter to continue...")

    # #test tab3
    testTab(app, 13, 3)
    raw_input("Switch to fourth tab. Then press Enter to continue...")

    # #test tab4
    testTab(app, 4, 4)    

def postTest(app):
    #app in Tutorial
    app[""]["Menu"].Click().Click()
    app[""].Wait("enabled")
    app['']['Back to Loader'].Click().Click()
    app[""].Wait("enabled")
    app['']['Main Menu'].Click().Click()
    app[""].Wait("enabled")

app = preTest()
toTutorialAndBack(app)
postTest(app)

