""" Note Graphics item class"""
from PyQt5 import QtWidgets, QtGui, QtCore

import variables
import logger


class Note(QtWidgets.QGraphicsItem):
    """Creating a Note class by inheriting QtWidgets.QGraphicsItem.
    """
    def __init__(self, parent=None, node=None, message=None):
        """Initializing Note class
        Args:
            parent (QtWidgets.QGraphicsItem): Parent class.
            node (node.Node): Node to to which you want to add node.
            message (str): Message string to display in Note.
        """
        super(Note, self).__init__(parent=parent)
        self.node = node
        self.message = message
        self.displayNote = True
        self.pen = QtGui.QPen(QtGui.QColor(1, 1, 1))
        self.brush = QtGui.QBrush(QtGui.QColor(255, 255, 51, 75))
        self.pen.setWidth(2)
        self.setZValue(1)
        self.setPosition()

    def setPosition(self):
        """This method sets Note position to top right corner of its Node.
        Returns:
            (None): Returns None.
        """
        pos_X = self.node.parameters[0].scenePos().x() + variables.NODE_SIZE
        pos_Y = self.node.parameters[0].scenePos().y() - variables.NODE_SIZE *2
        self.setPos(pos_X, pos_Y)

    def boundingRect(self):
        """This method creates a bounding rectangle for this class.
        Returns:
            (QtCore.QRectF): rectF object.
        """
        return QtCore.QRectF(self.node.parameters[0].scenePos().y(),
                             self.node.parameters[0].scenePos().y(),
                             100, 100)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """This method paints the widget on screen.
        Args:
            painter (QtGui.QPainter): Painter object to paint this widget.
            QStyleOptionGraphicsItem (None): None.
            widget (None): None.

        Returns:
            (None): Returns None.
        """
        if self.displayNote and self.message:
            # drawing outline polygon
            painter.setBrush(self.brush)
            painter.setPen(self.pen)
            outline = QtGui.QPolygon()
            outline.setPoints(0, 100,
                              -12, 50,
                              -75, 50,
                              -75, -50,
                              75, -50,
                              75, 50,
                              12, 50)
            painter.drawPolygon(outline)
            # drawing text message
            text = QtGui.QStaticText()
            if len(self.message) > 180:
                message = "{}...".format(self.message[:180])
            else:
                message = self.message
            text.setText(message)
            text.setTextWidth(140)
            painter.drawStaticText(-70, -40, text)

    def remove(self):
        """This method removes itself from the scene.
        Returns:
            (None): Returns None.
        """
        logger.log(msg="Removing note from node {}".format(self.node.label))
        self.node.scene.removeItem(self)
