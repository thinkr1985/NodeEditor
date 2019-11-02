"""Creating a Graph Editor"""
import sys
from PyQt5 import QtWidgets

import view
import toolbar
import variables


class GraphEditor(QtWidgets.QWidget):
    """Creating a GraphEditor class by inheriting QWidget"""
    def __init__(self, parent=None):
        """Initializing GraphEditor class.
        Args:
            parent (QtWidgets.QWidget): Parent widget for this class.
        """
        super(GraphEditor, self).__init__(parent)
        self.setWindowTitle("Test Window")
        self.setGeometry(300, 300, 600, 300)
        self.setContentsMargins(5, 5, 5, 5)
        # adding base layout to node editor
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # adding toolbar
        self.toolBarLayout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.toolBarLayout)
        self.toolBar = toolbar.EditorToolBar()
        self.toolBarLayout.addWidget(self.toolBar)

        self.viewLayout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.viewLayout)

        # adding a graphics view to node editor
        self.graphicsView = view.GraphView(parent=self)
        self.viewLayout.addWidget(self.graphicsView)

        self.connect_()
        self.setStyleSheet("""
                            GraphEditor{
                                background-color: gray;
                                border-color: gray;
                            }
                            """.replace("gray", variables.SC_GRID_DARK_COLOR))

    def connect_(self):
        self.toolBar.gridButton.clicked.connect(self.toggleGrid)

    def toggleGrid(self):
        if self.graphicsView.scene.drawGrid:
            self.graphicsView.scene.drawGrid = False
            self.graphicsView.scene.update()
            self.toolBar.gridButton.setOffColor()
        else:
            self.graphicsView.scene.drawGrid = True
            self.graphicsView.scene.update()
            self.toolBar.gridButton.setOnColor()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = GraphEditor()
    win.show()
    app.exec_()
