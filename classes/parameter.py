"""Creating a parameter class"""
from PyQt5 import QtGui, QtCore, QtWidgets

import variables
import connection
import logger


class Parameter(QtWidgets.QGraphicsItem):
    """Creating a Parameter class by inheriting QtWidgets.QGraphicsItem"""
    def __init__(self,  parent=None, node=None, paramName=None, paramValue=None,
                 paramIndex=1, paramType="input", toolTip=None):
        """Initializing Parameter class.
        Args:
            parent (QtWidgets.QGraphicsItem): Parent Item of this class.
            node (node.Node): Node object.
            paramName (str): Name of the Parameter.
            paramValue (): Value of the Parameter.
            paramIndex (int): Index of the Parameter.
            paramType (str): Type of the Parameter.
            toolTip (str): Tool tip of Parameter in string format.
        """
        super(Parameter, self).__init__(parent=parent)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setCursor(QtCore.Qt.CrossCursor)
        self.paramType = paramType
        self.node = node
        self.scene = self.node.scene
        self.paramName = paramName
        self.paramValue = paramValue
        self.toolTip = toolTip
        self.setToolTip(self.toolTip)
        self.outConnections = []
        self.inConnections = []
        self.paramIndex = paramIndex
        self.label_item = QtWidgets.QGraphicsTextItem(self)
        self.labelColor = QtGui.QColor(QtCore.Qt.white)
        self.labelFont = QtGui.QFont(variables.PARAM_LABEL_FONT)
        self.penActive = QtGui.QPen(QtCore.Qt.green)
        self.penInActive = QtGui.QPen(QtCore.Qt.white)
        self.activeBrush = QtGui.QBrush(QtCore.Qt.red)
        self.inActiveBrush = QtGui.QBrush(QtCore.Qt.black)
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
            return QtCore.QRectF(-variables.NODE_SIZE - variables.PARAM_RADIUS,
                                 (variables.NODE_SIZE / 3 * self.paramIndex + 3)
                                 - variables.NODE_SIZE + 3,
                                 12, 12).normalized()
        elif self.paramType == "output":
            return QtCore.QRectF(variables.NODE_SIZE,
                                 -variables.NODE_SIZE / 2,
                                 12, 12).normalized()

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
                -variables.NODE_SIZE,
                (variables.NODE_SIZE / 3 * self.paramIndex + 2)
                - variables.NODE_SIZE - 3
            )
        elif self.paramType == "output":
            self.label_item.setPos(variables.NODE_SIZE, -variables.NODE_SIZE)
        self.label_item.setTextWidth(
            variables.NODE_SIZE - 2
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
            painter.drawEllipse(-variables.NODE_SIZE - variables.PARAM_RADIUS,
                                (variables.NODE_SIZE / 3 * self.paramIndex + 3)
                                - variables.NODE_SIZE + 3,
                                variables.PARAM_RADIUS, variables.PARAM_RADIUS)

        elif self.paramType == "output":
            painter.drawEllipse(variables.NODE_SIZE, -variables.NODE_SIZE / 2,
                                variables.PARAM_RADIUS, variables.PARAM_RADIUS)

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


