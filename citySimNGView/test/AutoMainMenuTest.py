from time import sleep

from pywinauto import application

app = application.Application().connect(path="Mediator.exe")
# app[''].dump_tree()
app['']['Load and mount New Game'].print_control_identifiers()

app['']['Load and mount New Game'].Click().Click()
app[""].Wait("enabled")
app[""]["Main Menu"].Click().Click()

app[""].Wait("enabled")
app[""]["Creator"].Click().Click()
app.top_window().print_control_identifiers()

app[""].Wait("enabled")
app[""]["Menu"].Click().Click()

app[""].Wait("enabled")
app[""]["Exit"].Click().Click()
sleep(5)
print app.is_process_running()

# n_app = application.Application().start("notepad.exe")
# n_app.top_window().dump_tree()