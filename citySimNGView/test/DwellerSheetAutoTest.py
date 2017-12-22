import json
from time import sleep

from pywinauto import application



def clickOnButton(app, btn_title, n = None):
    try:
        while True:
            app[""][btn_title].Click()
            if n is not None and n == 0:
                break
            else: n-=1
    except Exception:
        pass


def preTest():
    app = application.Application().connect(path="Mediator.exe")
    # clickOnButton(app, "Creator",2)
    app.top_window()["Creator"].DoubleClick(button="left")
    app.top_window().Wait("enabled")
    print "creator ready"
    app[""].dump_tree()
    app.top_window()["add to Resources"].DoubleClick()
    app.top_window().Wait("ready")
    print "resources sheet ready"
    # here we assume that view is switched to ResourceSheet panel
    app[""]["Description of Resourcefor Tutorial moduleEdit1"].TypeKeys("Description")
    sleep(1)
    app[""]["StartIncome: Edit"].set_text("1")
    sleep(1)
    # clickOnButton(app, "Submit0")
    app.top_window()["Submit"].DoubleClick()
    sleep(1)
    print "submitted resource"

    app[""].dump_tree()
    app.top_window()["add to Dwellers"].DoubleClick()
    sleep(1)
    return app
    # it is important to have the app already running in ResourceSheeto panel at this point

def parseJSON(path):
    with open(path, "r") as f:
        content = f.read()
        js = json.loads(content)
        return js

def compareJSONOutputWithExpected():
    got = parseJSON("tmp.dep")
    expected = parseJSON("expected_dweller_content.json")
    print "Checking if expected json agrees with the result...",
    if got == expected: print "passed"
    else: print "failed"

def testInput(app):

    # here we assume that view is switched to ResourceSheet panel
    app[""]["Description of Dwellerfor Tutorial moduleEdit1"].TypeKeys("Description")
    sleep(1)
    app.top_window()['Resource'].click()
    sleep(1)
    app.top_window()['Consumed in quantity:Edit'].set_text("15")
    # clickOnButton(app, "Submit0")
    app.top_window()["Submit"].DoubleClick()
    sleep(1)
    print "submitted dweller"
    app.top_window().Wait("ready")
    while not app.Window_(title = "Choose a file to save").Exists():
        app.top_window()["Save these dependencies to file"].Click()
    print "window ", "Choose a file to save", "Exists"
    app.Window_(title="Choose a file to save").Wait("enabled", timeout=30)
    app.Window_(title="Choose a file to save")["Edit3"].TypeKeys("..\\..\\..\\citySimNG\\citySimNGView\\test\\tmp.dep")
    try:
        app.Window_(title="Choose a file to save")["Zapisz"].DoubleClick()
        app.Window_(title="Choose a file to save").WaitNot("Enabled")
    except Exception:
        pass
    print "saved file"

def postTest(app):
    clickOnButton(app, "Menu")
    app[""].Wait("enabled")

app = preTest()
testInput(app)
compareJSONOutputWithExpected()
postTest(app)
#if at this point no exception has been thrown, we assume transitions to various panels work correctly in MainMenu panel
