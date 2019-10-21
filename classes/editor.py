"""Creating a Graph Editor"""
import sys
from PyQt5 import QtWidgets

import view


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

        # adding base layout to node editor
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # adding a graphics view to node editor
        self.graphicsView = view.GraphView(parent=self)
        self.layout.addWidget(self.graphicsView)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = GraphEditor()
    win.show()
    app.exec_()
