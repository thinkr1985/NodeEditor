from PyQt5 import QtGui, QtCore, QtWidgets
import math

import variables
import logger


class Connection(QtWidgets.QGraphicsPathItem):
    """Creating Connection class by inheriting QGraphicsItem"""
    def __init__(self, parent=None, sourceParam=None, targetParam=None):
        """Initializing Connection class.
        Args:
            parent (QtWidgets.QGraphicsItem): Parent widget of this class.
            sourceParam (parameter.Parameter): Source Parameter of this connection.
            targetParam (parameter.Parameter): Target Parameter of this connection.
        """
        super(Connection, self).__init__(parent=parent)
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsSelectable |
                      QtWidgets.QGraphicsPathItem.ItemIsSelectable)
        self.sourceParam = sourceParam
        self.targetParam = targetParam
        self.sourceNode = self.sourceParam.node
        self.targetNode = self.targetParam.node
        self.activePen = QtGui.QPen(QtGui.QColor(variables.CON_ACTIVE_COLOR))
        self.activePen.setWidth(variables.CON_ACTIVE_LINE_WIDTH)
        self.deActivePen = QtGui.QPen(QtGui.QColor(variables.CON_INACTIVE_COLOR))
        self.deActivePen.setWidth(variables.CON_INACTIVE_LINE_WIDTH)
        self.arrow = self.arrow()

    def boundingRect(self):
        """Creating Bounding Rectangle for Connection widget.
        Returns (QtCore.QRectF): Returnsb Bounding RectF item.

        """
        return QtCore.QRectF(-10, (
                    variables.NODE_HEIGHT / 5 * self.targetParam.paramIndex + 10),
                             12, 12).normalized()

    def arrow(self):
        """"Creating instance of ConnectionArrow to draw Arrow shape.
        returns (ConnectionArrow): Returns the instance of ConnectionArrow Class.
        """
        arrowItem = ConnectionArrow(parameter=self.targetParam)
        arrowItem.setPen(QtCore.Qt.darkYellow)
        arrowItem.setBrush(QtCore.Qt.darkYellow)
        arrowItem.setZValue(10000)
        self.targetParam.node.scene.addItem(arrowItem)
        return arrowItem

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """Defining the Paint event for the Connection class.
        Args:
            painter (QtGui.QPainter): Painter object to paint this widget.
            QStyleOptionGraphicsItem (QtWidgets.QStyleGraphicsItem): pass
            widget (QtWidgets.QGraphicsItem): widget for which you want to paint.
        Returns:
            (None): Returns None.
        """
        painter.setBrush(QtCore.Qt.NoBrush)
        if self.isSelected():
            painter.setPen(self.activePen)
        else:
            painter.setPen(self.deActivePen)
        start_point = self.sourceParam.position
        end_point = self.targetParam.position
        path = QtGui.QPainterPath(QtCore.QPointF(start_point[0], start_point[1]))
        path.lineTo(QtCore.QPointF(end_point[0], end_point[1]))
        self.setPath(path)
        painter.drawPath(self.path())

        painter.setBrush(QtCore.Qt.yellow)
        painter.setPen(QtCore.Qt.yellow)

        poly_point_1 = QtCore.QPointF(self.targetParam.position[0], self.targetParam.position[1])
        poly_point_2 = QtCore.QPointF(self.targetParam.position[0], self.targetParam.position[1] - 12)
        poly_point_3 = QtCore.QPointF(self.targetParam.position[0] - 12, self.targetParam.position[1])
        points = [poly_point_1, poly_point_2, poly_point_3]
        polygon = QtGui.QPolygonF(points)
        self.arrow.setPolygon(polygon)

        rotDeg = 0
        xlength = start_point[0] - end_point[0]
        ylength = start_point[1] - end_point[1]
        d = math.sqrt(math.pow(xlength, 2) + math.pow(ylength, 2))
        beta = math.acos(xlength / d)
        rotDeg = math.degrees(beta)

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


class ConnectionArrow(QtWidgets.QGraphicsPolygonItem):
    """Creating a ConnectionArrow class by inheriting
     QtWidgets.QGraphicsPolygonItem"""
    def __init__(self, parent=None, parameter=None):
        """Initializing ConnectionArrow class.
        Args:
            parent (QtWidgets.QGraphicsItem): Parent widget of this class.
            parameter (parameter.Parameter): Target parameter of the arrow.
        """
        super(ConnectionArrow, self).__init__(parent=parent)
        self.parameter = parameter
        self.parameterIndex = self.parameter.paramIndex

    def boundingRect(self):
        """"Creating a bounding box for this class.
        Returns:
            (QtCore.QRectF): Returns QtCore.QRectF item.
        """
        return QtCore.QRectF(-10, (
                    variables.NODE_HEIGHT / 5 * self.parameterIndex + 10),
                             12, 12).normalized()

