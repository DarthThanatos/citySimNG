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

def testTab(app, nrOfTopics, tabID, direction):
    app['']['TabBtn'+str(tabID*100)].Click().Click()
    app[""].Wait("enabled")
    for i in range(nrOfTopics):
        app[''][direction].Click().Click()
        app[""].Wait("enabled")    
        print ("Tab " + str(tabID) + " Topic " + str(i))
    app[''][direction].Click().Click()
    app[""].Wait("enabled")    
    print ("Tab " + str(tabID) + " Topic " + str(0))    
    app['']['contents'].Click().Click()
    app[""].Wait("enabled")


def toTutorialAndBack(app):
    #app in Tutorial
    #app.top_window().print_control_identifiers()

    #test tab1
    testTab(app, 8, 1, 'nextTopic')
    testTab(app, 8, 1, 'prevTopic')
    raw_input("Switch to second tab. Then press Enter to continue...")

    #test tab2 
    testTab(app, 16, 2, 'nextTopic')
    testTab(app, 16, 2, 'prevTopic')
    raw_input("Switch to third tab. Then press Enter to continue...")

    # #test tab3 
    testTab(app, 13, 3, 'nextTopic')
    testTab(app, 13, 3, 'prevTopic')
    raw_input("Switch to fourth tab. Then press Enter to continue...")

    # #test tab4
    testTab(app, 4, 4, 'nextTopic')
    testTab(app, 4, 4, 'prevTopic')

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

