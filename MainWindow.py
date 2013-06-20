from PyQt4 import QtCore, QtGui, QtOpenGL
import sys
import Workspace


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.environment()
        self.window_properties()

        self.show()

    def window_properties(self):
        self.setGeometry(1000, 640, 300, 300)
        self.setWindowTitle('3D Spline visualisation')

        menu_bar = self.menuBar()
        file = menu_bar.addMenu('&File')
        file.addSeparator()
        self.create_menu_item('New', None, 'Ctrl+N', 'New workspace',
                              self.workspace.reset, file)
        self.create_menu_item('Exit', None, 'Ctrl+Q', 'Exit application',
                              QtCore.SLOT('close()'), file)
        # to add more menu items

        #self.status_bar = QtGui.statusBar()
        #self.status_bar.showMessage('Ready')

    def environment(self):
        self.workspace = Workspace.Workspace()
        self.workspace.setMinimumSize(800, 640)

        self.frame = QtGui.QFrame(self)

        self.setCentralWidget(self.frame)

        self.left_frame = QtGui.QFrame(self)
        self.left_frame.setFixedSize(200, 640)
        self.left_frame_layout = QtGui.QVBoxLayout()
        self.left_frame_layout.addWidget(QtGui.QLineEdit())
        self.left_frame_layout.addWidget(QtGui.QLineEdit())
        self.left_frame.setLayout(self.left_frame_layout)

        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.workspace)
        self.layout.addWidget(self.left_frame)
        self.frame.setLayout(self.layout)

    def create_menu_item(self, menu_item_label, icon_location,
                         shortcut, status_tip, action, menu_item):
        menu_item_action = QtGui.QAction(QtGui.QIcon(icon_location),
                                         menu_item_label, self)
        menu_item_action.setShortcut(shortcut)
        menu_item_action.setStatusTip(status_tip)
        self.connect(menu_item_action, QtCore.SIGNAL('triggered()'), action)

        menu_item.addAction(menu_item_action)


def main():
    app = QtGui.QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
