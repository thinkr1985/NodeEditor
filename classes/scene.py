"""Creating a graph SC class"""
from PyQt5 import QtGui, QtCore, QtWidgets
import math

import variables
import node
import connection
import logger


class GraphScene(QtWidgets.QGraphicsScene):
    """Creating GraphSC class by inheriting QGraphicsScene"""
    def __init__(self, parent=None, backgroundImage=None):
        """Initializing GraphScene class.
        Args:
            parent (QtWidgets.QGraphicsView): Parent widget for this class.
        """
        super(GraphScene, self).__init__(parent)
        self.backGroundImage = QtGui.QPixmap(variables.WALLPAPER)
        self.drawBackgroundImage()
        # color settings
        self.backGroundColor = QtGui.QColor(variables.SC_BG_COLOR)
        self.setBackgroundBrush(self.backGroundColor)
        self.gridLightPen = QtGui.QPen(
            QtGui.QColor(variables.SC_GRID_LIGHT_COLOR))
        self.gridLightPen.setWidth(variables.SC_GRID_LIGHT_LINE_WIDTH)
        self.gridDarkPen = QtGui.QPen(
            QtGui.QColor(variables.SC_GRID_DARK_COLOR))
        self.gridDarkPen.setWidth(variables.SC_GRID_DARK_LINE_WIDTH)

        # setting SC height and width
        self.SceneWidth, self.SceneHeight = 32000, 32000
        self.setSceneRect(-self.SceneWidth/2, -self.SceneHeight/2,
                          self.SceneWidth, self.SceneHeight)

        self.nodes = []
        # node_1 = self.addNode(label="read", nodeType="read", thumbnail="D:\\car_image.png")
        # node_2 = self.addNode(label="write", nodeType="write")
        # node_3 = self.addNode(label="image", nodeType="image")
        # node_3.addParameter(paramName="source", paramValue=0)
        # node_1.addParameter(paramName="color", paramValue=0)
        # node_1.addParameter(paramName="alpha", paramValue=0)
        # node_2.addParameter(paramName="filepath", paramValue=0)
        for num in range(10):

            node_1 = self.addNode(label="read", nodeType="read")
            node_1.addParameter(paramName="blend", paramValue=0)
            node_1.addParameter(paramName="alpha", paramValue=0)

    # node_2.addParameter(paramName="blend", paramValue=0)

    def drawBackgroundImage(self):
        # drawing a background image
        if variables.SC_DISPLAY_BG_IMAGE:
            item = self.backGroundImage = QtWidgets.QGraphicsPixmapItem(self.backGroundImage)
            self.addItem(item)

    def drawBackground(self, painter, rect):
        """This method draws background on QGraphicsScene
        Args:
            painter (QtGui.QPainter): QtGui painter object to paint rectangle.
            rect (QtCore.QRect): QtCore QRect object to draw rectangle.

        Returns:
            None
        """
        super().drawBackground(painter, rect)  # overriding the default class.

        # creating a grid
        # we need to convert values to int because rect.(..) returns floats.
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))
        first_left = left - (left % variables.SC_GRID_SIZE)
        first_top = top - (top % variables.SC_GRID_SIZE)

        # getting lines to be drawn on grid
        light_grid_lines, dark_grid_lines = [], []

        # drawing vertical lines
        for x in range(first_left, right, variables.SC_GRID_SIZE):
            if x % (variables.SC_GRID_SIZE * variables.SC_GRID_SQUARE_SIZE) != 0:
                light_grid_lines.append(QtCore.QLineF(x, top, x, bottom))
            else:
                dark_grid_lines.append(QtCore.QLineF(x, top, x, bottom))
        # drawing horizontal lines
        for y in range(first_top, bottom, variables.SC_GRID_SIZE):
            if y % (variables.SC_GRID_SIZE * variables.SC_GRID_SQUARE_SIZE) != 0:
                light_grid_lines.append(QtCore.QLineF(left, y, right, y))
            else:
                dark_grid_lines.append(QtCore.QLineF(left, y, right, y))

        # drawing the grid
        painter.setPen(self.gridLightPen)
        painter.drawLines(light_grid_lines)
        painter.setPen(self.gridDarkPen)
        painter.drawLines(dark_grid_lines)

    def addNode(self, label=None, nodeType=None, thumbnail=None):
        """This method adds node to the scene
        Args:
            label (str) : Label of the node.
            nodeType (str): Type of the node.
            thumbnail (str): thumbnail path. (jpg, png, giff)
        Returns:
            (node.Node): Returns the newly created node.
        """
        if not label or not nodeType:
            return
        for node_ in self.nodes:
            if node_.label == label:
                label = "{}_{}".format(label, len(self.nodes))
        logger.log(msg="Creating node with label {}".format(label))
        new_node = node.Node(self, label=label, nodeType=nodeType, thumbnail=thumbnail)
        self.addItem(new_node)
        self.nodes.append(new_node)
        return new_node

    def removeNode(self, node):
        """This method removes node from the scene.
        Args:
            node (node.Node):

        Returns:
            (None)
        """
        logger.log(msg="Removing node {}".format(node.label))
        self.nodes.remove(node)
        self.removeItem(node)


