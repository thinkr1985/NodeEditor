"""Creating a ToolBar widget for Node Editor"""
from PyQt5 import QtWidgets, QtGui, QtCore
import os

import variables


class EditorToolBar(QtWidgets.QWidget):
    """Creating a EditorToolBar class by inheriting QtWidgets.QWidget."""
    def __init__(self, parent=None):
        """Initializing EditorToolBar class.
        Args:
            parent (QtWidgets.QWidget): Parent widget of this class.
        """
        super(EditorToolBar, self).__init__(parent=parent)
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setMaximumHeight(15)
        self.setMinimumHeight(15)

        # adding buttons
        self.gridButton = ToolBarButton()
        self.gridButton.setToolTip("Grid On/Off")
        self.gridIcon = os.path.join(variables.ICON_PATH, "gridIcon.png")
        self.gridButton.setIcon(QtGui.QIcon(self.gridIcon))

        self.notesButton = ToolBarButton()
        self.notesButton.setToolTip("Notes On/Off")
        self.notesIcon = os.path.join(variables.ICON_PATH, "noteIcon.png")
        self.notesButton.setIcon(QtGui.QIcon(self.notesIcon))

        self.frameButton = ToolBarButton()
        self.frameButton.setToolTip("Frame All Node")
        self.frameIcon = os.path.join(variables.ICON_PATH, "frameIcon.png")
        self.frameButton.setIcon(QtGui.QIcon(self.frameIcon))

        # adding buttons to layout
        self.layout.addWidget(self.gridButton, QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.notesButton)
        self.layout.addWidget(self.frameButton)

        # adding spacer item to keep button on left side.
        self.spacerItem = QtWidgets.QSpacerItem(
            500, 10, QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.Expanding)
        self.layout.addItem(self.spacerItem)

        # setting a widget stylesheet
        self.setStyleSheet("""
                            EditorToolBar{
                                background-color: gray;
                                border-color: gray;
                            }
                            """.replace("gray", variables.SC_GRID_DARK_COLOR))


class ToolBarButton(QtWidgets.QPushButton):
    """Creating TooolBarButton class by inheriting QtWidgets.QPushButton."""
    def __init__(self, parent=None):
        """Initializing ToolBarButton class.
        Args:
            parent (QtWidgets.QWidget): Parent widget of this class.
        """
        super(ToolBarButton, self).__init__(parent=parent)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setMaximumWidth(20)
        self.setStyleSheet("""
                            ToolBarButton{
                                background-color: gray;
                                color: white;
                                border-width: 5px;
                                border-radius: 3px;
                                border-color : black;
                            }
                            ToolBarButton:hover{
                                                background-color: white;
                                                border-width: 10px;
                                                }
                            """)

    def setOnColor(self):
        """This method sets stylesheet of the widget if turned on.
        Returns:
            (None): Returns None.
        """
        self.setStyleSheet("""
                            ToolBarButton{
                                background-color: gray;
                                color: white;
                                border-width: 5px;
                                border-radius: 3px;
                                border-color : black;
                            }
                            ToolBarButton:hover{
                                                background-color: darkgray;
                                                border-width: 10px;
                                                }
                            """)

    def setOffColor(self):
        """This method sets stylesheet of the widget if turned off.
        Returns:
            (None): Returns None.
        """
        self.setStyleSheet("""
                            ToolBarButton{
                                background-color: darkgray;
                                color: white;
                                border-width: 5px;
                                border-radius: 3px;
                                border-color : black;
                            }
                            ToolBarButton:hover{
                                                background-color: gray;
                                                }
                            """)
