from time import sleep

from pywinauto import application

def clickOnButton(app, btn_title):
    try:
        app[""][btn_title].Click().Click()
    except Exception:
        pass


def preTest():
    app = application.Application().connect(path="Mediator.exe")
    clickOnButton(app, "Creator")
    app[""].Wait("enabled")
    clickOnButton(app, "add to Resources")
    app[""].Wait("enabled")
    return app
    # it is important to have the app already running in ResourceSheeto panel at this point

def testInput(app):
    # here we assume that view is switched to ResourceSheet panel
    sleep(1)
    app[""]["Description of Resourcefor Tutorial moduleEdit1"].TypeKeys("Description")
    # print [method_name for method_name in dir(app[""]["StartIncome"]) if callable(getattr(app[""]["StartIncome"], method_name))]
    app[""]["StartIncome: Edit"].set_text("1")
    clickOnButton(app, "Submit")
    sleep(2)
    # clickOnButton(app, "Save these dependencies to file")

    app.top_window()["Save these dependencies to file"].Click()
    app[""]["Save these dependencies to file"].Click()
    app.Window_(title="Choose a file to save").Wait("enabled", timeout=30)
    # app.Window_(title="Choose a file to save").dump_tree()
    app.Window_(title="Choose a file to save")["Edit3"].TypeKeys("tmp")
    app.Window_(title="Choose a file to save")["Zapisz"].Click()

def postTest(app):
    clickOnButton(app, "Cancel")
    clickOnButton(app, "Menu")
    app[""].Wait("enabled")

app = preTest()
testInput(app)
# postTest(app)
#if at this point no exception has been thrown, we assume transitions to various panels work correctly in MainMenu panel
