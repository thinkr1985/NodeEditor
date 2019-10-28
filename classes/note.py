""" Note Graphics item class"""
from PyQt5 import QtWidgets, QtGui, QtCore

import variables


class Note(QtWidgets.QGraphicsItem):
    def __init__(self, parent=None, node=None, message=None):
        super(Note, self).__init__(parent=parent)
        self.node = node
        self.message = message
        self.pen = QtGui.QPen(QtGui.QColor(1, 1, 1))
        self.brush = QtGui.QBrush(QtGui.QColor(255, 255, 51, 75))
        self.pen.setWidth(2)
        self.node.scene.addItem(self)
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable |
                      QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)
        self.write_note()

    def write_note(self):
        if not self.message:
            return
        self.text_item = QtWidgets.QGraphicsTextItem(self)
        self.text_item.setPlainText("This is test note his is test note his is test note his is test note his is test note")
        self.text_item.setDefaultTextColor(QtCore.Qt.white)
        self.text_item.setFont(QtGui.QFont("Verdana", 8))
        self.text_item.setPos(-100, 0)
        self.text_item.setTextWidth(
            variables.NODE_WIDTH - 2 * 5
        )

    def boundingRect(self):
        return QtCore.QRectF(0, 100, 100, 100)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        outline = QtGui.QPolygon()
        outline.setPoints(0, 200, -25, 100, -150, 100, -150, -100, 150, -100, 150, 100, 25, 100)
        painter.drawPolygon(outline)
