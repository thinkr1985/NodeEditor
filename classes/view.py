"""Creating Graphics view class for Node editor"""
from PyQt5 import QtWidgets, QtCore, QtGui

import scene
import variables
import parameter
import connection
import node
import logger


class GraphView(QtWidgets.QGraphicsView):
    """Creating a GraphView class by inheriting QGraphicsView"""
    def __init__(self, parent=None):
        """Initializing GraphView class
        Args:
            parent (QtWidgets.QWidget): Parent widget of this class.
        """
        super(GraphView, self).__init__(parent)
        self.setMouseTracking(True)
        self.graphicsPixmapItem = None
        self.scene = scene.GraphScene(parent=self)
        self.setScene(self.scene)
        self.setRenderHints(variables.VIEW_HIGH_ANTI_ALIASING)
        self.setViewportUpdateMode(variables.VIEW_UPDATE_MODE)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self.draggedParameter = None
        self.draggedPosition = None
        self.isDragging = False
        self.dragLine = []

    def mousePressEvent(self, event):
        """Overriding mouse press event to middle mouse press.
        Args:
            event (QtCore.QEvents): Event.

        Returns:
            (None)
        """
        if event.button() == QtCore.Qt.MiddleButton:
            self.middle_mouse_press(event)
        elif event.button() == QtCore.Qt.LeftButton:
            self.left_mouse_press(event)
        elif event.button() == QtCore.Qt.RightButton:
            self.right_mouse_press(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Overriding mouse release event to on middle mouse release.
        Args:
            event (QtCore.QEvent): Event.

        Returns:
            (None)
        """
        if event.button() == QtCore.Qt.MiddleButton:
            self.middle_mouse_release(event)
        if event.button() == QtCore.Qt.LeftButton:
            self.left_mouse_release(event)
        if event.button() == QtCore.Qt.RightButton:
            self.right_mouse_release(event)
        else:
            super().mouseReleaseEvent(event)

    def middle_mouse_press(self, event):
        """This method gives sets start panning viewport with middle mouse.
        Args:
            event (QtCore.QEvent): Event.

        Returns:
            (None)
        """
        release_event = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonRelease,
                                          event.localPos(),
                                          event.screenPos(),
                                          QtCore.Qt.LeftButton,
                                          QtCore.Qt.NoButton,
                                          event.modifiers())
        super().mouseReleaseEvent(release_event)

        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

        fake_event = QtGui.QMouseEvent(event.type(),
                                       event.localPos(),
                                       event.screenPos(),
                                       QtCore.Qt.LeftButton,
                                       event.buttons() |
                                       QtCore.Qt.LeftButton,
                                       event.modifiers())
        super().mousePressEvent(fake_event)

    def middle_mouse_release(self, event):
        """This method sets end to panning viewport with middle mouse.
        Args:
            event (QtCore.QEvent): Event.

        Returns:
            (None)
        """
        release_event = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonRelease,
                                          event.localPos(),
                                          event.screenPos(),
                                          QtCore.Qt.LeftButton,
                                          QtCore.Qt.NoButton,
                                          event.modifiers())
        super().mouseReleaseEvent(release_event)
        self.setDragMode(QtWidgets.QGraphicsView.NoDrag)

    def left_mouse_press(self, event):
        """Making Mouse Press Event Super on left mouse button press.
        Args:
            event (QtCore.QEvent): Event.

        Returns:
            None
        """
        item = self.itemAt(event.pos())
        if item:
            if type(item) == parameter.Parameter:
                self.isDragging = True
                self.draggedParameter = item
                self.draggedPosition = self.mapToScene(event.pos())
            else:
                self.isDragging = False
                self.draggedParameter = None
        else:
            self.isDragging = False
            self.draggedParameter = None
        super().mousePressEvent(event)

    def right_mouse_press(self, event):
        """making mouse press event super on right mouse button press.
        Args:
            event (QtCore.QEvent): Event.

        Returns:
            None
        """
        super().mousePressEvent(event)

    def left_mouse_release(self, event):
        """Making mouse release super on left mouse button press.
        Args:
            event (QtCore.QEvent): Event.

        Returns:
            None
        """
        if self.dragLine:
            self.scene.removeItem(self.dragLine)
            self.dragLine = None
        item = self.itemAt(event.pos())
        if item:
            if type(item) == parameter.Parameter:
                if self.draggedParameter:
                    logger.log(msg="Adding connection from {}.{} to {}.{}".
                               format(self.draggedParameter.node.label,
                                      self.draggedParameter.paramName,
                                      item.node.label, item.paramName))
                    con = self.draggedParameter.node.addConnection(
                        sourceParam=self.draggedParameter, targetParam=item)
                    if con:
                        self.draggedParameter = None
                    self.isDragging = False
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.dragLine:
            self.scene.removeItem(self.dragLine)
            self.dragLine = None
        if self.isDragging:
            if self.draggedParameter:
                self.dragLine = QtWidgets.QGraphicsLineItem(
                    self.draggedPosition.x(),
                    self.draggedPosition.y(),
                    self.mapToScene(event.pos()).x(),
                    self.mapToScene(event.pos()).y()
                )

                pen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.DotLine)
                self.dragLine.setPen(pen)
                self.scene.addItem(self.dragLine)
        super().mouseMoveEvent(event)

    def right_mouse_release(self, event):
        """making mouse release super on right mouse button press.
        Args:
            event (QtCore.QEvent): Event.

        Returns:
            None
        """
        super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        """Overriding the wheel event to make zoom the viewport.
        Args:
            event (QtCore.QEvent): Event.

        Returns:
            (None)
        """
        # calculating zoom factor
        zoom_out_factor = 1 / variables.VIEW_ZOOM_FACTOR

        # calculate the zoom
        if event.angleDelta().y() > 0:
            zoom_factor = variables.VIEW_ZOOM_FACTOR
            variables.VIEW_ZOOM_FACTOR += variables.VIEW_ZOOM_STEP
        else:
            zoom_factor = zoom_out_factor
            variables.VIEW_ZOOM_FACTOR -= variables.VIEW_ZOOM_STEP

        # setting up clamping
        variables.VIEW_ZOOM_CLAMP = False
        if variables.VIEW_ZOOM < variables.VIEW_ZOOM_RANGE[0]:
            variables.VIEW_ZOOM = variables.VIEW_ZOOM_RANGE[0]
            variables.VIEW_ZOOM_CLAMP = True
        elif variables.VIEW_ZOOM > variables.VIEW_ZOOM_RANGE[1]:
            variables.VIEW_ZOOM = variables.VIEW_ZOOM_RANGE[1]
            variables.VIEW_ZOOM_CLAMP = True

        # scaling the scene
        if not variables.VIEW_ZOOM_CLAMP:
            self.scale(zoom_factor, zoom_factor)

    def keyPressEvent(self, event):
        """Overriding keyPressEvent to add delete functionality"""
        if event.key() == QtCore.Qt.Key_Delete:
            self.deleteSelected()
        else:
            super().keyPressEvent(event)

    def deleteSelected(self):
        """This method deletes selected Node/parameter/Connection"""
        # order is important here.
        # First we need to remove all connections and then nodes.

        # removing connections
        selected_items = self.scene.selectedItems()
        for item in self.scene.selectedItems():
            if isinstance(item, connection.Connection):
                item.remove()
        # removing nodes
        for item in self.scene.selectedItems():
            if isinstance(item, node.Node):
                item.remove()
        print(self.scene.selectedItems())