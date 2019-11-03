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
        self.arrowShape = ArrowHead(self)
        self.targetParam.node.scene.addItem(self.arrowShape)

    def boundingRect(self):
        """Creating Bounding Rectangle for Connection widget.
        Returns (QtCore.QRectF): Returnsb Bounding RectF item.

        """
        return QtCore.QRectF(self.sourceParam.scenePos().x() +
                       variables.NODE_SIZE + 10,
                       (self.sourceParam.scenePos().y() -
                        variables.NODE_SIZE / 2) + 5,
                             self.targetParam.scenePos().x()
                             - variables.NODE_SIZE - 10,
                             (self.targetParam.scenePos().y() -
                              variables.NODE_SIZE + 27) +
                             (20 * self.targetParam.paramIndex) - 18
                             ).normalized()

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

        start_point = [self.sourceParam.scenePos().x() +
                       variables.NODE_SIZE + 10,
                       (self.sourceParam.scenePos().y() -
                        variables.NODE_SIZE / 2) + 5]

        end_point = [self.targetParam.scenePos().x()
                     - variables.NODE_SIZE - 10,
                     (self.targetParam.scenePos().y() -
                      variables.NODE_SIZE + (variables.NODE_SIZE/2)) +
                     ((variables.NODE_SIZE/3) * self.targetParam.paramIndex) - (variables.NODE_SIZE/3)]

        path = QtGui.QPainterPath(QtCore.QPointF(start_point[0], start_point[1]))
        path.lineTo(QtCore.QPointF(end_point[0], end_point[1]))
        self.setPath(path)
        painter.drawPath(self.path())

        # setting arrow head position
        rotDeg = 0
        xlength = start_point[0] - end_point[0]
        ylength = start_point[1] - end_point[1]
        d = math.sqrt(math.pow(xlength, 2) + math.pow(ylength, 2))
        if d > 0:
            beta = math.acos(xlength / d)
            rotDeg = math.degrees(beta)
            if start_point[1] > end_point[1]:
                self.arrowShape.setRotation(rotDeg + 180)
            else:
                self.arrowShape.setRotation(-rotDeg + 180)

        self.arrowShape.setPos(end_point[0], end_point[1])

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
        self.targetParam.node.scene.removeItem(self.arrowShape)
        self.sourceParam.node.outConnections.remove(self)
        self.sourceParam.outConnections.remove(self)
        if self.sourceParam.node in self.sourceParam.node.downStreamDependencies:
            self.sourceParam.node.downStreamDependencies.remove(self.sourceParam.node)

        self.targetParam.node.inConnections.remove(self)
        if self.targetParam.node in self.targetParam.node.upStreamDependencies:
            self.targetParam.node.upStreamDependencies.remove(self.targetParam.node)
        self.targetParam.inConnections.remove(self)

        self.sourceParam.node.scene.removeItem(self)


class ArrowHead(QtWidgets.QGraphicsPolygonItem):
    def __init__(self, parent=None):
        super(ArrowHead, self).__init__(parent=parent)
        self.pen = QtGui.QPen(QtCore.Qt.NoPen)
        self.brush = QtGui.QBrush(QtCore.Qt.black)
        self.setFillRule(QtCore.Qt.WindingFill)
        self.setZValue(-1)

    def boundingRect(self):
        return QtCore.QRectF(0, 0, 10, 10)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        point_1_pos = QtCore.QPointF(0, 0)
        point_2_pos = QtCore.QPointF(-20, -5)
        point_3_pos = QtCore.QPointF(-20, 5)
        polygon = QtGui.QPolygonF([point_1_pos, point_2_pos, point_3_pos])
        self.setPolygon(polygon)
        painter.drawPolygon(polygon)
