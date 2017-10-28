WELCOME_MSG = \
    "Welcome to the Creator Module! Today we will focus on creating dependencies. Now, let's start with something simple.\n"+\
    "On the left you have three panels, from which dependency creation is controlled.\n" +\
    "Dependencies may be added, edited or deleted. Each operation is performed by pressing respective buttons on the right of each panel.\n" +\
    "If you want to add new dependencies' set element, just press add button.\n" +\
    "To edit or delete already existing dependencies' set element, pick the one and click edit or delete button, respectively.\n" +\
    "When you are ready, just click create button on the bottom of the screen. Note, that each field must be filled before the operation succeeds.\n" +\
    "If everything was in order, a logical representation of dependencies will be created and sent to the loader module.\n" +\
    "At any point, you may just stop your work and save it by pressing save button.\nChanges will be saved to a .dep file\n" +\
    "You can then load dependencies created at some point in the past by pressing \"Load dependencies from file\" button.\n" +\
    "To return to menu, click the menu button on the bottom of the screen."

CHECKER_PANEL_ERROR_MSG = "-> Pick at least one element in the section \"{}\". If there is nothing to choose there, consider creating some elements in other panels\n"

LOADER_BTN_HINT = "Go to loader panel. Here you can load previously created dependencies and mount them into a game itself, selecting set from sets list and clicking appropriate button. " \
                  "\nHint: you can view dependencies graph by double clicking on a set name"

CREATOR_BTN_HINT = "Go to the Creator panel.\n It kind of serves the role of the admin panel of this system. \nThere you can create dependencies sets later injected in the games itself; save and load " \
                   "dependencies from .dep files; editing, adding and deleting strategic games' build-blocks: entities named resources, buildings and dwellers. You can also choose " \
                   "your own appropriate textures of the map's background to add more fitting atmosphere to a currently created game. Each set should have a unique set name or it will overwrite " \
                   "previously created set! Also, after creating dependencies, you can view them in the bottom panel of the Creator panel in the form of a visualised dependencies graph. \nHint: you can edit an already created entity by " \
                   "double clicking on its name."

EXIT_BTN_HINT = "Exit this system. Please wait until the black console window that appeared after running run.bat script closes itself; then you can be certain this system cleaned " \
                "up and exited properly"

MENU_BTN_HINT = "Return to the panel you have come from"
LOAD_DEPS_BTN_HINT = "Load dependencies from file. Caution: new dependencies will override any work you have performed up to this moment"
SAVE_DEPS_BTN_HINT = "Save dependencies to file. Caution: the previous contents of a chosen file will be overwritten"
CREATE_DEPS_BTN_HINT = "Create dependencies and send them to the selection list in the loader module. Before clicking this button, if you do not want to overwrite any previously created sets, please " \
                       "give your set a unique name"

CLEAN_DEPS_BTN_HINT = "Cleans admin panel. Caution: if you do not want to lose your work, first you should save it to a file by clicking Save button"
BACKGROUND_TEXTURE_SELECTION_BTN_HINT = "Choose another texture from a png or jpg file in the selected directory. Chosen textures will be used when moving to adjacent map tiles, so pick textures having " \
                                        "similar rhythm"

SHOW_GRAPH_BTN_HINT = "Shows a graph of dependencies under a dependencies set name selected above.\n" \
                      "You can know that a wanted set name has been selected, when its background color is blue.\n" \
                      "Hint: you can show a graph just double-clicking on a chosen set name in the above list."

MOUNT_GAME_BTN_HINT = "Mounts selected dependencies set into a game itself and goes into this game's menu panel.\n " \
                      "You can know that a wanted set name has been selected, when its background color is blue."

GAME_BTN_HINT = "Starts a game when none has been started yet, or resumes one if the started game was paused, respectively"

TUTORIAL_BTN_HINT = "Shows the Tutorial panel with all its information, including the clues to this game mechanics, the chosen set characteristics and the game's entities descriptions."

EXCHANGE_BTN_HINT = "Goes into the Exchange panel. This panel is a place where you can try boost your domain development by selling, buying or playing for additional resources." \
                    " All changes will have an effect to your stock pile (its state can be checked in a game's map top-most panel)"

DEPENDENCIES_SENT_MSG = "Dependencies sent to further processing to creator controller"

GRAPH_DETAILS_BTN_HINT = "Click here to see a detailed graph description. Nodes representing entities will be organized with attached names (if appropriate); by clicking on a node, you will be able to see" \
                         " important information in a panel to the right"