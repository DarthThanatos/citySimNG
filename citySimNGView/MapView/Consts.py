from utils.RelativePaths import relative_textures_path, relative_fonts_path


# =================================================================================================================== #
# FONT CONSTS #
# =================================================================================================================== #
FONT_SIZE = 30
FONT = relative_fonts_path + "OldLondon.ttf"

# =================================================================================================================== #
# COLORS #
# =================================================================================================================== #
RED = (150, 0, 0)
GREEN = (0, 150, 0)
YELLOW = (200, 200, 0)
PURPLE = (200, 0, 200)
WHITE = (255, 255, 255)

# =================================================================================================================== #
# PYGAME CONSTS #
# =================================================================================================================== #
FPS = 100
LEFT = 1
RIGHT = 3

# =================================================================================================================== #
# RESOURCES PANEL CONSTS #
# =================================================================================================================== #
RESOURCES_PANEL_SIZE = 0.05
RESOURCES_PANEL_TEXTURE = relative_textures_path + 'BuildingsPanelTexture.jpg'

RESOURCES_PANEL_ARROW_Y = 0.5
RESOURCES_PANEL_RIGHT_ARROW_X = 0.7
RESOURCES_PANEL_LEFT_ARROW_X = 0.1


# =================================================================================================================== #
# BUILDINGS PANEL CONSTS #
# =================================================================================================================== #
BUILDINGS_PANEL_TEXTURE = relative_textures_path + 'BuildingsPanelTexture.jpg'
BUILDINGS_PANEL_SIZE = 0.12

BUILDINGS_PANEL_RIGHT_ARROW_X = 0.6
BUILDINGS_PANEL_LEFT_ARROW_X = 0.1
BUILDINGS_PANEL_ARROW_Y = 0.85

# =================================================================================================================== #
# INFO PANEL CONSTS #
# =================================================================================================================== #
INFO_PANEL_WIDTH = 0.5
INFO_PANEL_HEIGHT = 0.15

DELETE_BUILDING_WIDTH = 0.1
DELETE_BUILDING_HEIGHT = 0.3

# =================================================================================================================== #
# NAVIGATION PANEL CONSTS #
# =================================================================================================================== #
NAV_ARROW_WIDTH = 0.4
NAV_ARROW_HEIGHT = 0.4

NAVIGATION_PANEL_HEIGHT = 0.2
NAVIGATION_PANEL_WIDTH = 0.2

NAV_PANEL_TEX = relative_textures_path + 'BuildingsPanelTexture.jpg'

# =================================================================================================================== #
# TEXT PANEL CONSTS #
# =================================================================================================================== #
TEXT_PANEL_HEIGHT = 0.15
TEXT_PANEL_WIDTH = 1 - NAVIGATION_PANEL_WIDTH - INFO_PANEL_WIDTH - BUILDINGS_PANEL_SIZE 
TEXT_PANEL_FONT_SIZE = 10

# =================================================================================================================== #
# TEXTURES #
# =================================================================================================================== #
DEFAULT_TEXTURE = relative_textures_path + "DefaultBuilding.jpg"
DEFAULT_RESOURCE_TEXTURE = relative_textures_path + "DefaultBuilding.jpg"
GRASS_TEXTURE = relative_textures_path + "Grass.png"
MEADOW_TEXTURE = relative_textures_path + "Meadow.jpg"
GRASS2_TEXTURE = relative_textures_path + "Grass2.jpg"
NAV_ARROW_TEXTURE = relative_textures_path + 'LeftArrow.png'

# =================================================================================================================== #
# DWELLERS #
# =================================================================================================================== #
DWELLER_ICON_WIDTH = 0.03
DWELLER_ICON_HEIGHT = 0.9

# =================================================================================================================== #
# OTHERS #
# =================================================================================================================== #
RESOURCE_SIZE = 0.03

BUILDING_WIDTH = 0.4
BUILDING_HEIGHT = 0.2
BUILDING_SIZE = 0.1
# TODO:
RESOURCES_SPACE = 10

ARROW_BUTTON_WIDTH = 0.3
ARROW_BUTTON_HEIGHT = 0.1
SPACE = 20
MENU_BUTTON_WIDTH = 0.05
