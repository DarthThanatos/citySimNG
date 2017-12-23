from pywinauto import application

def preTest():
    app = application.Application().connect(path="Mediator.exe")
    app.top_window()["Creator"].DoubleClick(button="left")
    app.top_window().Wait("enabled")
    return app

def testShowDetailsBeforeCreated(app):
    # at this point nothing should be displayed on "graph details" panel
    show_details_btns = app[""].children(title = "Show Details")
    for button_title in ["Show details1", "Show Details2", "Show Details3"]:
        print "checking if ", button_title, "is not enabled...",
        if not app[""][button_title].IsEnabled(): print "PASSED"
        else: print "FAILED"


def testShowDetailsAfterCreated(app):
    # at this point, sth should be displayed on graph details panel
    details_map = {"Show details1" : "Details of Resources", "Show Details2" : "Details of Dwellers", "Show Details3": "Details of Buildings"}
    for button_title in details_map.keys():
        print "checking if ", button_title, "is enabled after pressing create button...",
        if app[""][button_title].IsEnabled():
            print "PASSED"
        else:
            print "FAILED"

def loadAndCreateDeps(path):
    while not app.Window_(title = "Choose a file").Exists():
        app[""]["Load dependencies from a file"].Click()
    app.Window_(title="Choose a file").Wait("enabled", timeout=30)
    app.Window_(title="Choose a file")["Edit3"].TypeKeys(path)
    try:
        app.Window_(title="Choose a file")["Otworz"].DoubleClick()
        app.Window_(title="Choose a file").WaitNot("Enabled")
    except Exception:
        pass
    app.top_window().Create.DoubleClick()


def moveToLoaderFromCreator():
    app['']['Menu'].DoubleClick()
    app[""].Wait("enabled")
    app['']['Load and mount New Game'].Click().Click()
    app[""].Wait("enabled")

def moveToCreatorFromLoader():
    app['']['Main Menu'].DoubleClick()
    app[""].Wait("enabled")
    app['']['Creator'].DoubleClick()
    app[""].Wait("enabled")


def testCreatedCorrectly(app):
    print "Test if graph details buttons are not enabled before the create button was pressed..."
    testShowDetailsBeforeCreated(app)
    loadAndCreateDeps("..\\..\\..\\citySimNG\\citySimNGView\\test\\test_dep.dep")
    print "Test if graph details buttons are enabled after the create button was pressed..."
    testShowDetailsAfterCreated(app)
    print "Test if created deps are available in Loader panel ...",
    moveToLoaderFromCreator()
    try:
        app[""].ListBox.select("Default Set") # if everything is correct, default set is selectable - no exception is thrown
        print "PASSED"
    except Exception:
        print "FAILED"
    finally:
        moveToCreatorFromLoader()


def testDeletablesResource(app):
    loadAndCreateDeps("..\\..\\..\\citySimNG\\citySimNGView\\test\\resources_del.dep")
    app.top_window().ResourcesListBox.select("Resource")
    app.top_window()["delete selected from Resources"].Click()
    # ^ since there is a predecessor relation (R, Pred, R1), it system should refuse to delete Resource and its name should still be selectable (no exception should be raised)
    print "test if Resource was not deleted...",
    try:
        app.top_window().ResourcesListBox.select("Resource")
        print "PASSED"
    except:
        print "FAILED"
    print "test if Resource1 was deleted...",
    app.top_window().ResourcesListBox.select("Resource1")
    app.top_window()["delete selected from Reources"].Click()
    try:
        app.top_window().DwellersListBox.select("Resource1")
        print "FAILED"
    except:
        print "PASSED"
    # now if the previous test passed, Resource should be removable...
    print "test if Resource was deleted...",
    app.top_window().ResourcesListBox.select("Resource")
    app.top_window()["delete selected from Reources"].Click()
    try:
        app.top_window().DwellersListBox.select("Resource")
        print "FAILED"
    except:
        print "PASSED"

def testDeletablesDweller(app):
    loadAndCreateDeps("..\\..\\..\\citySimNG\\citySimNGView\\test\\dwellers_del.dep")
    app.top_window().DwellerListBox.select("Dweller")
    app.top_window()["delete selected from Dwellers"].Click()
    # ^ since there is a predecessor relation (D, Pred, D1), it system should refuse to delete Dweller and its name should still be selectable (no exception should be raised)
    print "test if Dweller was not deleted...",
    try:
        app.top_window().BuildingsListBox.select("Dweller")
        print "PASSED"
    except:
        print "FAILED"
    print "test if Dweller1 was deleted...",
    app.top_window().DwellersListBox.select("Dweller1")
    app.top_window()["delete selected from Dwellers"].Click()
    try:
        app.top_window().DwellersListBox.select("Dweller1")
        print "FAILED"
    except:
        print "PASSED"
    # now if the previous test passed, Dweller should be removable...
    print "test if Dweller was deleted...",
    app.top_window().DwellersListBox.select("Dweller")
    app.top_window()["delete selected from Dwellers"].Click()
    try:
        app.top_window().DwellersListBox.select("Dweller")
        print "FAILED"
    except:
        print "PASSED"

def testDeletablesBuilding(app):
    loadAndCreateDeps("..\\..\\..\\citySimNG\\citySimNGView\\test\\buildings_del.dep")
    app.top_window().BuildingsListBox.select("Building")
    app.top_window()["delete selected from Buildings"].Click()
    # ^ since there is a predecessor relation (B, Pred, B1), it system should refuse to delete Building and its name should still be selectable (no exception should be raised)
    print "test if Building was not deleted...",
    try:
        app.top_window().BuildingsListBox.select("Building")
        print "PASSED"
    except:
        print "FAILED"
    print "test if Building1 was deleted...",
    app.top_window().BuildingsListBox.select("Building1")
    app.top_window()["delete selected from Buildings"].Click()
    try:
        app.top_window().BuildingsListBox.select("Building1")
        print "FAILED"
    except:
        print "PASSED"
    # now if the previous test passed, Building should be removable...
    print "test if Building was deleted...",
    app.top_window().BuildingsListBox.select("Building")
    app.top_window()["delete selected from Buildings"].Click()
    try:
        app.top_window().BuildingsListBox.select("Building")
        print "FAILED"
    except:
        print "PASSED"


def testCrossDeletables(app):
    loadAndCreateDeps("..\\..\\..\\citySimNG\\citySimNGView\\test\\test_dep.dep")
    app.top_window().ResourcesListBox.select("Resource")
    app.top_window()["delete selected from Resources"].Click()
    # ^ since there exist relations (D, Consumes, R) and (B, Consumes, R), system should refuse to delete Resource and its name should still be selectable (no exception should be raised)
    print "test if Resource was not deleted...",
    try:
        app.top_window().ResourcesListBox.select("Resource")
        print "PASSED"
    except:
        print "FAILED"

    app.top_window().DwellerListBox.select("Dweller")
    app.top_window()["delete selected from Dwellers"].Click()
    # ^ since there is a relation (B, Hosts, D) system should refuse to delete Dweller and its name should still be selectable (no exception should be raised)
    print "test if Dweller was not deleted...",
    try:
        app.top_window().BuildingsListBox.select("Dweller")
        print "PASSED"
    except:
        print "FAILED"

    app.top_window().BuildingsListBox.select("Building")
    app.top_window()["delete selected from Buildings"].Click() # delete Building to remove "Hosts" relationship between Building and Dweller
    app.top_window().ResourcesListBox.select("Resource")
    app.top_window()["delete selected from Resources"].Click()
    # ^ since there still exists relationship (B, Consumes, R), system should refuse to delete Resource and its name should still be selectable (no exception should be raised)
    print "test if Resource was not deleted...",
    try:
        app.top_window().ResourcesListBox.select("Resource")
        print "PASSED"
    except:
        print "FAILED"


    app.top_window().DwellerListBox.select("Dweller")
    app.top_window()["delete selected from Dwellers"].Click()
    # ^ since the relation (B, Hosts, D) no longer exists system should refuse to delete Dweller and its name should still be selectable (no exception should be raised)
    print "test if Dweller was not deleted...",
    try:
        app.top_window().BuildingsListBox.select("Dweller")
        print "PASSED"
    except:
        print "FAILED"

    # now if the previous test passed, Resource should be removable (no relationships binding it exist any more)...
    print "test if Resource was deleted...",
    app.top_window().ResourcesListBox.select("Resource")
    app.top_window()["delete selected from Reources"].Click()
    try:
        app.top_window().DwellersListBox.select("Resource")
        print "FAILED"
    except:
        print "PASSED"


def postTest(app):
    app['']['Menu'].DoubleClick()
    app[""].Wait("enabled")

app = preTest()
testCreatedCorrectly(app)
testDeletablesResource(app)
testDeletablesDweller(app)
testDeletablesBuilding(app)
testCrossDeletables(app)
postTest(app)
#if at this point no exception has been thrown, we assume transitions to various panels work correctly in MainMenu panel
