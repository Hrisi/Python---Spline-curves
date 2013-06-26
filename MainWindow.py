from PyQt4 import QtCore, QtGui, QtOpenGL
import sys
import Workspace
import Bezier_curves
import Vec3D
import SplinesC2
import SplinesC1
import SplinesC0
import MainDialog


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.environment()
        self.window_properties()

        self.main_dialog = MainDialog.MainDialog()
        self.main_dialog.hide()
        #value, accepted = QtGui.QInputDialog.getInt(None, "foo", "bar")

        #test
        curve = Bezier_curves.BezierCurve()
        splineC2 = SplinesC2.SplineC2(3, [[1, 2], [2, 7]])
        splineC1 = SplinesC1.SplineC1(3, [[1, 2], [2, 7]])
        splineC0 = SplinesC0.SplineC0(3, [[1, 2], [2, 7], [7, 10]])

        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(0, 1, 0),
                  Vec3D.Vec3D(2, 1, 0),
                  Vec3D.Vec3D(3, 0, 0),
                  Vec3D.Vec3D(4, -1, 0),
                  Vec3D.Vec3D(4, -1, 0),
                  Vec3D.Vec3D(4, -1, 4),
                  Vec3D.Vec3D(4, -1, 3),
                  Vec3D.Vec3D(4, -1, -3),
                  Vec3D.Vec3D(4, -1, 2)]
        for index in range(0, 6):
            curve.append_point(points[index])
            splineC1.append_deBoor_point(points[index])

        for index in range(0, 5):
            splineC2.append_deBoor_point(points[index])
        for index in range(0, 10):
            splineC0.append_point(points[index])

        self.workspace.add_Bezier_curve_object(curve)
        self.workspace.change_curve_visibility(curve)
        self.workspace.change_subdivision_visibility(curve, 0.3)
        self.workspace.change_degree_elevation_visibility(curve)
        #self.workspace.change_derivative_visibility(curve, 2)
        #self.workspace.change_derivative_visibility(curve, 1)
        #self.workspace.change_curve_subdivision_visibility(curve, 0.5)
        #self.workspace.change_control_polygon_visibility(curve)

        #self.workspace.add_splineC2_object(splineC2)
        #self.workspace.change_curve_visibility(splineC2)
        #self.workspace.change_Bezier_control_polygon_visibility(splineC2)
        #self.workspace.change_deBoor_control_polygon_visibility(splineC2)
        #self.workspace.add_splineC1_object(splineC1)
        #self.workspace.change_curve_visibility(splineC1)
        #self.workspace.add_splineC0_object(splineC0)
        #self.workspace.change_curve_visibility(splineC0)
        #self.workspace.change_control_polygon_visibility(splineC0)

        #self.workspace.updateGL()
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
            self.create_object_dialog, curve)

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

    def create_object_dialog(self):
        #if isinstance(object_, Bezier_curves.BezierCurve):
            #self.workspace.add_Bezier_curve_object(object_)
            #self.add_points_dialog(object_)

        self.main_dialog.show()

    def add_points_dialog(self, object_):
        dialog = QtGui.QDialog()


def main():
    app = QtGui.QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
