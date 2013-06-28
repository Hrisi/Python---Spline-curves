from PyQt4 import QtCore, QtGui, QtOpenGL
import sys
import Workspace
import Bezier_curves
import Vec3D
import SplinesC2
import SplinesC1
import SplinesC0
import MainDialog


class InputException(Exception):
    pass


class MainWindow(QtGui.QMainWindow):
    MISSING_COORDINATES_MESSAGE = "You haven't entered one coordinate or more."

    def __init__(self):
        super(MainWindow, self).__init__()

        self.environment()
        self.window_properties()
        self.dialog = None

        self.show()

    def open_file(self):
        file_name = QtGui.QFileDialog.getOpenFileName(self, 'Open File',
                                                      '.')
        file_ = open(file_name)
        data = file_.read()
        #read from file and put the points in the right place
        fname.close()

    def save_file(self):
        file_name = QtGui.QFileDialog.getSaveFileName(self, 'Save File',
                                                      '.')
        file_ = open(file_name, 'w')
        #write inserted points into file
        fname.close()

    def window_properties(self):
        self.setGeometry(1000, 640, 300, 300)
        self.setWindowTitle('3D Spline visualisation')

        menu_bar = self.menuBar()
        file_ = menu_bar.addMenu('&File')
        file_.addSeparator()
        #file_new = file_.addMenu('&New')
        #file_new.addSeparator()

        #self.create_menu_item('Bezier curve', None, 'Ctrl+B', 'New workspace',
                              #self.create_Bezier_curve_object, file_new)

        #spline = file_new.addMenu('&Spline')
        #spline.addSeparator()

        #self.create_menu_item('C0', None, 'Ctrl+0', 'New C0 spline',
                              #self.splineC1_dialog, spline)
        #self.create_menu_item('C1', None, 'Ctrl+1', 'New C1 spline',
                              #self.splineC1_dialog, spline)
        #self.create_menu_item('C2', None, 'Ctrl+2', 'New C2 spline',
                              #self.splineC2_dialog, spline)

        self.create_menu_item('Open', None, 'Ctrl+O', 'Open file',
                              self.open_file, file_)
        self.create_menu_item('Save', None, 'Ctrl+S', 'Save file',
                              self.save_file, file_)
        self.create_menu_item('Exit', None, 'Ctrl+Q', 'Exit application',
                              QtCore.SLOT('close()'), file_)

        curve = menu_bar.addMenu('&Bezier curve')

        self.create_menu_item(
            'New', None, 'Ctrl+B', 'New Bezier_curve',
            self.show_Bezier_curve_dialog, curve)

        view = menu_bar.addMenu('&View')
        view.addSeparator()
        self.create_menu_item('Zoom In', None, 'Ctrl++', 'Zoom in workspace',
                              self.workspace.zoom_in, view)
        self.create_menu_item('Zoom Out', None, 'Ctrl+-', 'Zoom out workspace',
                              self.workspace.zoom_out, view)

        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Ready')

    def environment(self):
        self.workspace = Workspace.Workspace()
        self.workspace.setMinimumSize(800, 640)

        self.frame = QtGui.QFrame(self)

        self.setCentralWidget(self.frame)

        self.left_frame = QtGui.QFrame(self)
        self.left_frame.setFixedSize(200, 640)
        self.left_frame_layout = QtGui.QVBoxLayout()
        self.frame
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

    def get_control_points_from_dialog(self):
        add_points_line_edit = []

        for index in range(0, len(self.dialog.add_points_line_edit) - 1):
            add_points_line_edit.append(
                self.dialog.add_points_line_edit[index])

        for coordinates in add_points_line_edit:
            for index in range(0, 3):
                if coordinates[index] == "":
                    print(":))")
                    message_box = QtGui.QMessageBox()
                    message_box.setText(self.MISSING_COORDINATES_MESSAGE)
                    message_box.show()
                    raise InputException(self.MISSING_COORDINATES_MESSAGE)

        self.workspace.inserted_control_points = [
            Vec3D.Vec3D(int(coordinates[0].text()),
                        int(coordinates[1].text()),
                        int(coordinates[2].text()))
            for coordinates in add_points_line_edit]

        self.create_Bezier_curve()

    def show_Bezier_curve_dialog(self):
        self.dialog = MainDialog.MainDialog('New Bezier curve')
        self.dialog.show()

        self.dialog.draw_button.clicked.connect(
            self.get_control_points_from_dialog)

    def create_Bezier_curve(self):
        curve = Bezier_curves.BezierCurve()

        for point in self.workspace.inserted_control_points:
            curve.append_point(point)

        print(curve.control_points)

        self.workspace.change_curve_visibility(curve)
        self.workspace.add_Bezier_curve_object(curve)

        self.dialog.hide()
        self.dialog = None

    def add_points_dialog(self, object_):
        dialog = QtGui.QDialog('Bezier Curves')


def main():
    app = QtGui.QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
