"""Creating a Graph Editor"""
import sys
from PyQt5 import QtWidgets

import view
import toolbar
import variables
import node


class GraphEditor(QtWidgets.QWidget):
    """Creating a GraphEditor class by inheriting QWidget"""
    def __init__(self, parent=None):
        """Initializing GraphEditor class.
        Args:
            parent (QtWidgets.QWidget): Parent widget for this class.
        """
        super(GraphEditor, self).__init__(parent)
        self.setWindowTitle("Node Editor")
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
        """This method connected all widgets to their functions.
        Returns:
            (None): Returns None.
        """
        self.toolBar.gridButton.clicked.connect(self.toggleGrid)
        self.toolBar.notesButton.clicked.connect(self.toggleNote)

    def toggleGrid(self):
        """This method toggles the grid visibility for scene.
        Returns:
            (None): Returns None.
        """
        if self.graphicsView.scene.drawGrid:
            self.graphicsView.scene.drawGrid = False
            self.toolBar.gridButton.setOffColor()
        else:
            self.graphicsView.scene.drawGrid = True
            self.toolBar.gridButton.setOnColor()
        self.graphicsView.scene.update()

    def toggleNote(self):
        """This methos toggles the notes display in scene.
        Returns:
            (None): Returns None.
        """
        all_items = (self.graphicsView.scene.items())
        if not all_items:
            return
        for item in all_items:
            if isinstance(item, node.Node):
                if item.note:
                    display = item.note.displayNote
                    if display:
                        item.note.displayNote = False
                    else:
                        item.note.displayNote = True
        self.graphicsView.scene.update()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = GraphEditor()
    win.show()
    app.exec_()
