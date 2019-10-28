from PyQt5 import QtGui, QtCore, QtWidgets
import math

import variables
import logger


class Connection(QtWidgets.QGraphicsPathItem):
    """Creating Connection class by inheriting QGraphicsItem"""
    def __init__(self, parent=None, sourceParam=None, targetParam=None,
                 toolTip=None):
        """Initializing Connection class.
        Args:
            parent (QtWidgets.QGraphicsItem): Parent widget of this class.
            sourceParam (parameter.Parameter): Source Parameter of this connection.
            targetParam (parameter.Parameter): Target Parameter of this connection.
            toolTip (str): Tool tip for connection in string format.
        """
        super(Connection, self).__init__(parent=parent)
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsSelectable |
                      QtWidgets.QGraphicsPathItem.ItemIsSelectable)
        self.sourceParam = sourceParam
        self.targetParam = targetParam
        self.toolTip = toolTip
        self.setToolTip(self.toolTip)
        self.sourceNode = self.sourceParam.node
        self.targetNode = self.targetParam.node
        self.activePen = QtGui.QPen(QtCore.Qt.green)
        self.activePen.setWidth(2)
        self.deActivePen = QtGui.QPen(QtCore.Qt.black)
        self.deActivePen.setWidth(2)

    def boundingRect(self):
        """Creating Bounding Rectangle for Connection widget.
        Returns (QtCore.QRectF): Returnsb Bounding RectF item.

        """
        return QtCore.QRectF(variables.NODE_SIZE, (
                    variables.NODE_SIZE / 5 * self.targetParam.paramIndex + 10),
                             12, 12).normalized()

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """Defining the Paint event for the Connection class.
        Args:
            painter (QtGui.QPainter): Painter object to paint this widget.
            QStyleOptionGraphicsItem (QtWidgets.QStyleGraphicsItem): pass
            widget (QtWidgets.QGraphicsItem): widget for which you want to paint.
        Returns:
            (None): Returns None.
        """
        painter.setBrush(QtCore.Qt.black)
        if self.isSelected():
            painter.setPen(self.activePen)
        else:
            painter.setPen(self.deActivePen)

        start_point = [self.sourceParam.scenePos().x() + (variables.NODE_SIZE /self.sourceParam.paramIndex + 2),
                       self.sourceParam.scenePos().y() - (variables.NODE_SIZE /(self.sourceParam.paramIndex + 2))]

        end_point = [self.targetParam.scenePos().x() - (variables.NODE_SIZE /self.targetParam.paramIndex + 10),
                     self.targetParam.scenePos().y() - variables.NODE_SIZE/self.targetParam.paramIndex + 25]

        path = QtGui.QPainterPath(QtCore.QPointF(start_point[0], start_point[1]))
        path.lineTo(QtCore.QPointF(end_point[0], end_point[1]))
        self.setPath(path)
        painter.drawPath(self.path())

    def remove(self):
        """This method removes the connection of self.
        Returns:
            (None): Returns None.
        """
        logger.log(msg="Removing connection of parameter {} from node {} from"
                       " parameter {} from node {}".format(
                        self.targetParam.paramName,
                        self.targetParam.node.label,
                        self.sourceParam.paramName,
                        self.sourceParam.node.label,
            ))
        self.sourceParam.node.outConnections.remove(self)
        self.sourceParam.outConnections.remove(self)
        if self.sourceParam.node in self.sourceParam.node.downStreamDependencies:
            self.sourceParam.node.downStreamDependencies.remove(self.sourceParam.node)

        self.targetParam.node.inConnections.remove(self)
        if self.targetParam.node in self.targetParam.node.upStreamDependencies:
            self.targetParam.node.upStreamDependencies.remove(self.targetParam.node)
        self.targetParam.inConnections.remove(self)

        self.sourceParam.node.scene.removeItem(self)