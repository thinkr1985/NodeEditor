"""Declaring global variables to use in Node Editor classes"""
from PyQt5 import QtGui, QtWidgets
import os


ICON_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "icons")

WALLPAPER = os.path.join(ICON_PATH, "wallpaper.jpg")

SC_DISPLAY_BG_IMAGE = False

SC_BG_COLOR = "#393939"  # darkest gray

SC_GRID_SQUARE_SIZE = 5  # Grid squares required to make dark grid.

SC_GRID_LIGHT_COLOR = "#2f2f2f"  # light gray

SC_GRID_DARK_COLOR = "#292929"  # dark gray

SC_GRID_LIGHT_LINE_WIDTH = 1  # Grid light line width

SC_GRID_DARK_LINE_WIDTH = 1  # Grid dark line width

SC_GRID_SIZE = 20  # size of one square

VIEW_HIGH_ANTI_ALIASING = (
        QtGui.QPainter.Antialiasing |
        QtGui.QPainter.HighQualityAntialiasing |
        QtGui.QPainter.TextAntialiasing |
        QtGui.QPainter.SmoothPixmapTransform
)  # Node editor viewport anti-aliasing (default with High Anti-aliasing)

VIEW_UPDATE_MODE = QtWidgets.QGraphicsView.FullViewportUpdate

VIEW_ZOOM_FACTOR = 1.25

VIEW_ZOOM = 10.0

VIEW_ZOOM_STEP = 0.1

VIEW_ZOOM_RANGE = [0, 10]

VIEW_ZOOM_CLAMP = False

NODE_WIDTH = 150.0

NODE_HEIGHT = 100.0

NODE_LABEL_FONT = QtGui.QFont("Verdana", 10)

NODE_LABEL_FORECOLOR = "#B2B2B2"  # Node Label foreground color

NODE_LABEL_BACKCOLOR = "#505050"  # Node Label foreground color

NODE_OUTLINE_SELECT_COLOR = "#DBDBDB"  # Node outline color when selected

NODE_OUTLINE_DESELECT_COLOR = "#5D5D5D"  # Node outline color when unselected

NODE_BODY_COLOR = "#7B7B7B"  # Node body color

PARAM_LABEL_COLOR = "#FFFFFF"

PARAM_LABEL_FONT = QtGui.QFont("Verdana", 9)

PARAM_BACK_COLOR = "#FF111111"

PARAM_FORE_COLOR = "#FF0000"

PARAM_ACTIVE_OUTLINE_COLOR = "#03AD00"

PARAM_INACTIVE_OUTLINE_COLOR = "#DBDBDB"

PARAM_RADIUS = 4.0

PARAM_OUTLINE_WIDTH = 4

PARAM_POS_OFFSET = 20

CON_INACTIVE_COLOR = "#FF000000"

CON_ACTIVE_COLOR = "#03AD00"

CON_ACTIVE_LINE_WIDTH = 3

CON_INACTIVE_LINE_WIDTH = 2

