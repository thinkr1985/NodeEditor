"""Creating Node"""
from PyQt5 import QtGui, QtWidgets, QtCore
import os

import variables
import parameter
import logger
import note


class Node(QtWidgets.QGraphicsItem, object):
    """Creating Node Class by inheriting QtWidgets.QGraphicsItem"""
    def __init__(self, scene=None, label=None, nodeType=None, parent=None,
                 thumbnail=None, toolTip=None):
        """Initializing Node Class.
        Args:
            scene (QtWidgets.QGraphicsScene): Graphics Scene item to add this
                widget.
            label (str): Label of this in string format.
            nodeType (str): Node type of this Node.
            parent (QtWidgets.QGraphicsItem): Parent widget of this class.
            thumbnail (str): Thumbnail image path of this Node. (jpg, png)
            toolTip (str): Tool tip for node in string format.
        """
        super(Node, self).__init__(parent=parent)
        self.scene = scene
        self.label = label
        self.nodeType = nodeType
        self.thumbnail = thumbnail
        self.parameters = []
        self.outConnections = []
        self.inConnections = []
        self.upStreamDependencies = []
        self.downStreamDependencies = []
        self.note = None
        self.toolTip = toolTip
        self.setToolTip(self.toolTip)

        # setting up Pens and brushes
        self.outlineSelectedPen = QtGui.QPen(
            QtGui.QColor(variables.NODE_OUTLINE_SELECT_COLOR))
        self.outlineDeSelectedPen = QtGui.QPen(
            QtGui.QColor(variables.NODE_OUTLINE_DESELECT_COLOR)
        )
        self.labelForeBrush = QtGui.QBrush(
            QtGui.QColor(variables.NODE_LABEL_FORECOLOR))
        self.bodyBrush = QtGui.QBrush(QtGui.QColor(variables.NODE_BODY_COLOR))
        self.labelForeColor = QtGui.QColor(variables.NODE_LABEL_FORECOLOR)
        self.labelBackColor = QtGui.QColor(variables.NODE_LABEL_BACKCOLOR)
        self.labelBrush = QtGui.QBrush(self.labelBackColor)
        self.labelFont = QtGui.QFont("Verdana", 10)

        self.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable |
                      QtWidgets.QGraphicsItem.ItemIsSelectable)

        # adding node label
        self.setupLabel()
        # setting out parameter
        outParameter = parameter.Parameter(parent=self, node=self,
                                           paramName="out", paramValue=None,
                                           paramIndex=1, paramType="output")
        self.parameters.append(outParameter)

    def boundingRect(self):
        """"Creating a bounding box for this class.
        Returns:
            (QtCore.QRectF): Bounding box of this widget.
        """
        return QtCore.QRectF(
            -variables.NODE_SIZE,
            -variables.NODE_SIZE,
            variables.NODE_SIZE * 2,
            variables.NODE_SIZE * 2
        ).normalized()

    def setupLabel(self):
        """Setting up Title of the Node using QGraphicsTextItem"""
        self.label_item = QtWidgets.QGraphicsTextItem(self)
        self.label_item.setPlainText(self.label)
        self.label_item.setDefaultTextColor(QtCore.Qt.white)
        self.label_item.setFont(self.labelFont)
        self.label_item.setPos(-variables.NODE_SIZE, -variables.NODE_SIZE - 2)
        self.label_item.setTextWidth(variables.NODE_SIZE)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """This events paints the Node on screen.
        Args:
            painter (QtGui.QPainter): Painter object to paint the widget.
            QStyleOptionGraphicsItem (QtWidgets.QStyleOptionGraphicsItem):pass
            widget: pass

        Returns:
            (None): Returns None.
        """
        self.outlineSelectedPen.setWidth(3)
        # create body rectangle
        body = QtGui.QPainterPath()
        body.setFillRule(QtCore.Qt.WindingFill)

        # create outline polygon
        outline = QtGui.QPolygon()
        outline.setPoints(- variables.NODE_SIZE,
                          - variables.NODE_SIZE,
                          - variables.NODE_SIZE,
                          variables.NODE_SIZE,
                          variables.NODE_SIZE,
                          variables.NODE_SIZE,
                          variables.NODE_SIZE,
                          -variables.NODE_SIZE)
        if self.isSelected():
            painter.setPen(self.outlineSelectedPen)
        else:
            painter.setPen(self.outlineDeSelectedPen)
        painter.setBrush(self.bodyBrush)
        painter.drawPolygon(outline)
        # create label polygon
        label_outline = QtGui.QPolygon()
        label_outline.setPoints(- variables.NODE_SIZE + 1,
                                - variables.NODE_SIZE + 1,
                                -variables.NODE_SIZE + 1,
                                - variables.NODE_SIZE + 19,
                                variables.NODE_SIZE - 1,
                                - variables.NODE_SIZE + 19,
                                variables.NODE_SIZE - 1,
                                - variables.NODE_SIZE+1)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self.labelBrush)
        painter.drawPolygon(label_outline)

        if self.thumbnail:
            if os.path.exists(self.thumbnail):
                pixmap = QtGui.QPixmap(self.thumbnail)
                painter.drawPixmap(-variables.NODE_SIZE + 15, -variables.NODE_SIZE + 25, variables.NODE_SIZE + 30,
                                   variables.NODE_SIZE + 30, pixmap)

    def addParameter(self, paramName=None, paramValue=None):
        """This method Adds parameter to Node with given name and value.
        Args:
            paramName (str): Name of Parameter to add in string.
            paramValue (): Value of the parameter.
        Returns:
            (parameter.Parameter): Returns the Parameter object.
        """
        if self.parameters:
            for param in self.parameters:
                if param.paramName == paramName:
                    logger.log(typ="ERROR",
                               msg="Parameter {} already exists on node {}!".
                               format(paramName, param.node.label))
                    return
        logger.log(msg="Adding parameter {} to node {}".format(paramName,
                                                               self.label))
        parameter_ = parameter.Parameter(parent=self,
                                         node=self,
                                         paramName=paramName,
                                         paramValue=paramValue,
                                         paramIndex=(len(self.parameters)),
                                         paramType="input")
        logger.log(msg=parameter_)
        self.parameters.append(parameter_)
        return parameter_

    def removeParameter(self, paramName=None):
        """This method removes the parameter from itself of provided name.
        Args:
            paramName (str): Name of the parameter to remove in string.

        Returns:
            (None): Returns None.
        """
        parameters = {}
        [parameters.update({x.paramIndex: x}) for x in self.parameters
         if self.parameters]
        if parameters:
            for index, param_node in parameters.items():
                if param_node.paramName == paramName:
                    self.scene.removeItem(param_node)

    def addConnection(self, sourceParam=None, targetParam=None):
        """This method adds connection to the scene.
        Args:
            targetParam (parameter.Parameter): target parameter of another node.
            sourceParam (parameter.Parameter): source parameter.
        Returns:
            (connection.Connection): Returns the connection object.
        """

        return sourceParam.addConnection(targetParam=targetParam)

    def removeConnection(self, sourcePar, targetPar):
        """This method removes connection from the scene.
        Args:
            sourcePar (parameter.Parameter): source parameter of this node.
            targetPar (parameter.Parameter): target parameter of another node.
        Returns:
            (None)
        """
        if self.outConnections:
            for connect in self.outConnections:
                if connect.sourceParam == sourcePar and \
                        connect.targetParam == targetPar:
                    connect.remove()
                else:
                    logger.log(
                        typ="ERROR",
                        msg="No connection found to remove from {}.{} to {}.{}".
                        format(self.label, sourcePar.paramName,
                               targetPar.node.label,
                               targetPar.paramName))
        else:
            logger.log(typ="ERROR",
                       msg="There are no connections in the node {}".format(
                           self.label))

    def getDownStreamDependencies(self, node_=None):
        """This method gets all the down stream dependencies of given node.
        Args:
            node_ (Node): Node Object.
        Returns:
            (list): Returns List containing Node objects.
        """
        if not node_:
            node_ = self
        dependencies = []
        for node_object in node_.downStreamDependencies:
            dependencies.append(node_object)
            if node_object.downStreamDependencies:
                dep = self.getDownStreamDependencies(node_=node_object)
                if dep:
                    dependencies.extend(dep)
        return dependencies

    def getUpStreamDependencies(self, node_=None):
        """This method gets all the up stream dependencies of given node.
        Args:
            node_ (Node): Node Object.
        Returns:
            (list): Returns List containing Node objects.
        """
        if not node_:
            node_ = self
        dependencies = []
        for node_object in node_.upStreamDependencies:
            dependencies.append(node_object)
            if node_object.upStreamDependencies:
                dep = self.getUpStreamDependencies(node_=node_object)
                if dep:
                    dependencies.extend(dep)
        return dependencies

    def remove(self):
        """" This method removes node from scene.
            order is important here.
            first we need to remove note, connections then parameters and then
            we can remove node.
        """
        # removing note
        if self.note:
            self.note.remove()
        # removing out connections
        if self.outConnections:
            for connect in self.outConnections:
                connect.remove()
        # removing in connections
        if self.inConnections:
            for connect in self.inConnections:
                connect.remove()
        # removing parameters
        if self.parameters:
            for parameter_ in self.parameters:
                parameter_.remove()

        logger.log(msg="Removing node {}".format(self.label))
        # removing node itself.
        self.scene.removeItem(self)

    def addNote(self, note_=None):
        """This method adds note to the note.
            message exceeds 180 characters will get truncated.
        Args:
            note_ (str): Note in string format.
        Returns:
            (note.Note): Returns Note object.
        """
        if self.note:
            self.note.remove()
        self.note = note.Note(self, node=self, message=note_)
        return self.note

    def removeNote(self):
        """This method removes note from the node.
        Returns:
            (None): Returns None.
        """
        if self.note:
            self.note.remove()
            self.note = None
        else:
            logger.log(
                typ="SKIPPED",
                msg="No Note found to remove in node {}".format(self.label))

    def getNote(self, asString=False):
        """"This method gets notes from current node
        Returns:
            (str/note.Note): Returns Note object if asString is False or return
                            message of the note in string format.
        """
        if self.note:
            if asString:
                return self.note.message
            else:
                return self.note
        else:
            logger.log(
                typ="ERROR",
                msg="No Note found to query in node {}".format(self.label))






