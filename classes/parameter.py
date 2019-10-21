"""Creating a parameter class"""
from PyQt5 import QtGui, QtCore, QtWidgets

import variables
import connection
import logger


class Parameter(QtWidgets.QGraphicsItem):
    """Creating a Parameter class by inheriting QtWidgets.QGraphicsItem"""
    def __init__(self,  parent=None, node=None, paramName=None, paramValue=None,
                 paramIndex=1, paramType="input"):
        """Initializing Parameter class.
        Args:
            parent (QtWidgets.QGraphicsItem): Parent Item of this class.
            node (node.Node): Node object.
            paramName (str): Name of the Parameter.
            paramValue (): Value of the Parameter.
            paramIndex (int): Index of the Parameter.
            paramType (str): Type of the Parameter.
        """
        super(Parameter, self).__init__(parent=parent)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setCursor(QtCore.Qt.CrossCursor)
        self.paramType = paramType
        self.node = node
        self.scene = self.node.scene
        self.paramName = paramName
        self.paramValue = paramValue
        self.outConnections = []
        self.inConnections = []
        self.paramIndex = paramIndex
        self.label_item = QtWidgets.QGraphicsTextItem(self)
        self.parPos = variables.PARAM_POS_OFFSET * paramIndex
        self.position = [self.scenePos().x(), self.scenePos().y()]
        self.labelColor = QtGui.QColor(variables.PARAM_LABEL_COLOR)
        self.labelFont = QtGui.QFont(variables.PARAM_LABEL_FONT)
        self.penActive = QtGui.QPen(
            QtGui.QColor(variables.PARAM_ACTIVE_OUTLINE_COLOR))
        self.penInActive = QtGui.QPen(
            QtGui.QColor(variables.PARAM_INACTIVE_OUTLINE_COLOR))
        self.activeBrush = QtGui.QBrush(QtGui.QColor(variables.PARAM_FORE_COLOR))
        self.inActiveBrush = QtGui.QBrush(
            QtGui.QColor(variables.PARAM_BACK_COLOR))
        self.outputInactiveBrush = QtGui.QBrush(QtCore.Qt.black)
        self.outputInactivePen = QtGui.QPen(QtCore.Qt.black)
        if self.paramType == "input":
            self.setupLabel()

    def boundingRect(self):
        """Creating Bounding box for parameter
        Returns:
            (QtCore.QRectF): Returns the QRectF item.
        """
        if self.paramType == "input":
            return QtCore.QRectF(-10, (variables.NODE_HEIGHT / 5 * self.paramIndex + 10),
                12, 12).normalized()
        elif self.paramType == "output":
            return QtCore.QRectF(variables.NODE_WIDTH, 30, 12, 12).normalized()

    def setupLabel(self):
        """Setting up Parameter label
        Returns:
            (None): Returns None.
        """
        self.label_item.setPlainText(self.paramName)
        self.label_item.setDefaultTextColor(self.labelColor)
        self.label_item.setFont(self.labelFont)
        if self.paramType == "input":
            self.label_item.setPos(
                2, (variables.NODE_HEIGHT / 5 * self.paramIndex + 2)
            )
        elif self.paramType == "output":
            self.label_item.setPos(variables.NODE_WIDTH - 40, 20)
        self.label_item.setTextWidth(
            variables.NODE_WIDTH - 2
        )

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """This events paints the widget on screen.
        Args:
            painter (QtGui.QPainter): Painter item to paint.
            QStyleOptionGraphicsItem (): pass
            widget ():

        Returns:
            (None): Returns None.
        """
        if self.paramType == "input":
            self.position = [self.node.scenePos().x() - 10,
                             (variables.NODE_HEIGHT / 5 * self.paramIndex + 15) + self.node.scenePos().y()]
        elif self.paramType == "output":
            self.position = [self.node.scenePos().x() + variables.NODE_WIDTH + 10,
                             35 + self.node.scenePos().y()]

        self.penInActive.setWidth(1)
        self.penActive.setWidth(1)
        if self.isSelected():
            painter.setBrush(self.activeBrush)
            painter.setPen(self.penActive)
        else:
            if self.paramType == "input":
                painter.setBrush(self.inActiveBrush)
                painter.setPen(self.penInActive)
            else:
                if self.paramType == "output":
                    painter.setBrush(self.outputInactiveBrush)
                    painter.setPen(self.outputInactivePen)
        if self.paramType == "input":
            painter.drawEllipse(
                -10, (variables.NODE_HEIGHT / 5 * self.paramIndex + 10), 12, 12)
        elif self.paramType == "output":
            painter.drawEllipse(variables.NODE_WIDTH, 30, 12, 12)

    def addConnection(self, targetParam=None):
        """This method adds connection to the scene.
        Args:
            targetParam (Parameter): target parameter of another node.
        Returns:
            (connection.Connection): Returns the connection object.
        """
        if targetParam.paramType == "output":
            logger.log(typ="ERROR", msg="Target parameter cannot be a output")
            return
        if targetParam in self.node.parameters:
            logger.log(typ="ERROR",
                       msg="Connection cannot be created with self parameters")
            return
        if self.paramType == targetParam.paramType:
            logger.log(typ="ERROR",
                       msg="Connection cannot be made inbetween same parameter"
                           " type (! {}.{} --> {}.{})".format(
                            self.node.label,
                            self.paramName,
                            targetParam.node.label,
                            targetParam.paramName))
            return
        if targetParam.node in self.node.getUpStreamDependencies(node_=self.node):
            logger.log(typ="ERROR",
                       msg="Connection cannot be made as node {} is in up"
                           " stream dependencies of node {}".format(
                           targetParam.node.label, self.node.label))
            return

        if not self.outConnections:
            logger.log(
                msg="Connecting parameter {} from node {} to parameter {}"
                    " of node {}".format(self.paramName, self.node.label,
                                         targetParam.paramName,
                                         targetParam.node.label))
            return self.connect(targetParam)

        for connec in self.outConnections:
            if connec.targetParam.paramName == targetParam.paramName\
                    and connec.targetParam.node in self.node.downStreamDependencies\
                    and connec.targetParam.node.label == targetParam.node.label:

                logger.log(
                    typ="ERROR",
                    msg="Connection inbetween {}.{} to {}.{} already exists"
                        .format(self.node.label, self.paramName,
                                targetParam.node.label,
                                targetParam.paramName))
                return
        logger.log(msg="Connecting parameter {} from node {} to parameter {}"
                       " of node {}".format(self.paramName, self.node.label,
                                            targetParam.paramName,
                                            targetParam.node.label))
        return self.connect(targetParam)

    def connect(self, targetParam):
        """This method connects parameter with given target parameter.
        Args:
            targetParam (Parameter): Target Parameter object.
        Returns:
            (connection.Connection): Returns connection object.
        """
        # removing connection if has one already
        if targetParam.inConnections:
            for connect_ in targetParam.inConnections:
                connect_.remove()
        # adding new connection
        con = connection.Connection(sourceParam=self,
                                    targetParam=targetParam)
        self.outConnections.append(con)
        self.node.outConnections.append(con)
        targetParam.inConnections.append(con)
        targetParam.node.inConnections.append(con)
        self.node.downStreamDependencies.append(targetParam.node)
        targetParam.node.upStreamDependencies.append(self.node)
        self.scene.addItem(con)
        con.setZValue(-1)
        logger.log(msg=con)
        return con

    def remove(self):
        """This method removes self from its node.
        Returns:
            (None): Returns None.
        """
        # removing all connections of this parameter.
        if self.outConnections:
            for connect in self.outConnections:
                connect.remove()

        logger.log(msg="Removing parameter {} from node {}".format(
            self.paramName, self.node.label))
        # removing parameter itself.
        self.node.scene.removeItem(self)


