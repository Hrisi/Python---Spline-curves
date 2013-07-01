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
    NEGATIVE_DEGREE_MESSAGE = "You have inserted negative number. Try again!"
    EMPTY_INTERVAL = "One or more interval lengths empty!"

    def __init__(self):
        super(MainWindow, self).__init__()

        self.environment()
        self.window_properties()
        self.dialog = None

        self.show()

    def open_file(self):
        file_name = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.')
        file_ = open(file_name)
        data = file_.read()
        #read from file and put the points in the right place
        fname.close()

    def save_file(self):
        file_name = QtGui.QFileDialog.getSaveFileName(self, 'Save File', '.')
        file_ = open(file_name, 'w')
        #write inserted points into file
        fname.close()

    def window_properties(self):
        self.setGeometry(1000, 640, 300, 300)
        self.setWindowTitle('3D Spline visualisation')

        menu_bar = self.menuBar()
        file_ = menu_bar.addMenu('&File')
        file_.addSeparator()

        self.create_menu_item('Open', None, 'Open file',
                              self.open_file, file_, 'Ctrl+O')
        self.create_menu_item('Save', None, 'Save file',
                              self.save_file, file_, 'Ctrl+S')
        self.create_menu_item('Exit', None, 'Exit application',
                              QtCore.SLOT('close()'), file_, 'Ctrl+Q')

        curve = menu_bar.addMenu('&Bezier curve')
        file_.addSeparator()

        self.create_menu_item(
            'New', None, 'New Bezier_curve',
            self.show_Bezier_curve_dialog, curve, 'Ctrl+B')
        self.create_menu_item(
            'Add more points', None, 'Adds more points to the curve.',
            self.show_add_more_Bezier_points_dialog, curve)
        self.create_menu_item(
            'Delete last point', None, 'Deletes last point from the curve.',
            self.workspace.delete_last_point_from_Bezier_curve, curve)
        self.create_menu_item(
            'Show control_polygon', None, 'Shows control polygon',
            self.workspace.show_control_polygon, curve)
        self.create_menu_item(
            'Hide control_polygon', None, 'Hides control polygon',
            self.workspace.hide_control_polygon, curve)
        self.create_menu_item(
            'Calculate derivative', None, 'Calculates derivative.',
            self.show_derivative_dialog, curve)
        self.create_menu_item(
            'Show subdivision', None, 'Subdivides curve.',
            self.show_subdivision_dialog, curve)
        self.create_menu_item(
            'Hide subdivision', None, 'Hides subdivision of curve.',
            self.workspace.hide_subdivision, curve)
        self.create_menu_item(
            'Show degree elevation', None, 'Shows curve elevation.',
            self.workspace.show_degree_elevation, curve)
        self.create_menu_item(
            'Hide degree elevation', None, 'Hides curve elevation.',
            self.workspace.hide_degree_elevation, curve)

        spline = menu_bar.addMenu('&Spline')
        spline.addSeparator()
        new_spline = spline.addMenu('&New')

        self.create_menu_item(
            'New', None, 'New Spline C0',
            self.show_splineC0_dialog, new_spline, 'Ctrl+0')
        self.create_menu_item(
            'New', None, 'New Spline C1',
            self.show_splineC1_dialog, new_spline, 'Ctrl+1')
        self.create_menu_item(
            'New', None, 'New Spline C2',
            self.show_splineC2_dialog, new_spline, 'Ctrl+2')

        self.create_menu_item(
            'Show Bezier control_polygon', None, 'Shows Bezier polygon',
            self.workspace.show_Bezier_control_polygon, spline)
        self.create_menu_item(
            'Hide Bezier control_polygon', None, 'Hides Bezier polygon',
            self.workspace.hide_Bezier_control_polygon, spline)
        self.create_menu_item(
            'Show deBoor control_polygon', None, 'Shows deBoor polygon',
            self.workspace.show_deBoor_control_polygon, spline)
        self.create_menu_item(
            'Hide deBoor control_polygon', None, 'Hides deBoor polygon',
            self.workspace.hide_deBoor_control_polygon, spline)

        view = menu_bar.addMenu('&View')
        view.addSeparator()
        self.create_menu_item('Zoom In', None, 'Zoom in workspace',
                              self.workspace.zoom_in, view, 'Ctrl++')
        self.create_menu_item('Zoom Out', None, 'Zoom out workspace',
                              self.workspace.zoom_out, view, 'Ctrl+-')

        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Ready')

    def environment(self):
        self.workspace = Workspace.Workspace()
        self.workspace.setMinimumSize(800, 640)

        self.frame = QtGui.QFrame(self)

        self.setCentralWidget(self.frame)

        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.workspace)
        self.frame.setLayout(self.layout)

    def create_menu_item(self, menu_item_label, icon_location, status_tip,
                         action, menu_item, shortcut=None):
        menu_item_action = QtGui.QAction(QtGui.QIcon(icon_location),
                                         menu_item_label, self)

        if shortcut is not None:
            menu_item_action.setShortcut(shortcut)

        menu_item_action.setStatusTip(status_tip)
        self.connect(menu_item_action, QtCore.SIGNAL('triggered()'), action)

        menu_item.addAction(menu_item_action)

    def show_dialog(self, title, splineC0=None, splineC1=None, splineC2=None):
        self.dialog = MainDialog.MainDialog(
            title, splineC0, splineC1, splineC2)
        self.dialog.show()

    def get_control_points_from_dialog(self):
        add_points_line_edit = []
        inserted_control_points = []

        if (not self.dialog.splineC0 and not self.dialog.splineC1 and not
                self.dialog.splineC2):
            for index in range(0, len(self.dialog.add_points_line_edit) - 1):
                add_points_line_edit.append(
                    self.dialog.add_points_line_edit[index])
        else:
            add_points_line_edit = self.dialog.add_points_line_edit

        for coordinates in add_points_line_edit:
            for index in range(0, 3):
                if coordinates[index] == "":
                    message_box = QtGui.QMessageBox()
                    message_box.setText(self.MISSING_COORDINATES_MESSAGE)
                    message_box.show()
                    raise InputException(self.MISSING_COORDINATES_MESSAGE)

        inserted_control_points = [
            Vec3D.Vec3D(float(coordinates[0].text()),
                        float(coordinates[1].text()),
                        float(coordinates[2].text()))
            for coordinates in add_points_line_edit]

        return inserted_control_points

    def show_Bezier_curve_dialog(self):
        self.show_dialog("New Bezier curve")

        self.dialog.draw_button.clicked.connect(
            self.create_Bezier_curve)

    def add_control_points_to_object(self, object_):
        inserted_control_points = []

        inserted_control_points = self.get_control_points_from_dialog()

        for point in inserted_control_points:
            if (isinstance(object_, Bezier_curves.BezierCurve) or
                    isinstance(object_, SplinesC0.SplineC0)):
                object_.append_point(point)
            else:
                object_.append_deBoor_point(point)

    def get_intervals_from_dialog(self):
        intervals = []
        intervals_line_edit = []

        for index in range(0, len(self.dialog.intervals_line_edit) - 1):
            intervals_line_edit.append(self.dialog.intervals_line_edit[index])

        for interval in intervals_line_edit:
            if interval.text() == "":
                raise InputException(self.EMPTY_INTERVAL)
            intervals.append(float(interval.text()))

        return intervals

    def create_Bezier_curve(self):
        curve = Bezier_curves.BezierCurve()
        self.add_control_points_to_object(curve)

        self.workspace.change_curve_visibility(curve)
        self.workspace.add_Bezier_curve_object(curve)

        self.dialog.hide()
        self.dialog = None

    def show_add_more_Bezier_points_dialog(self):
        self.show_dialog("Add more points")

        self.dialog.draw_button.clicked.connect(
            self.add_points_to_drawn_Bezier_curve)

    def add_points_to_drawn_Bezier_curve(self):
        for curve in self.workspace.objects[
                self.workspace.OBJECT_BEZIER_CURVES]:
            self.workspace.change_curve_visibility(curve)
            print(curve.to_be_drawn)
            self.add_control_points_to_object(curve)
            self.workspace.change_curve_visibility(curve)
            print(curve.to_be_drawn)

        self.dialog.hide()
        self.dialog = None

    def show_splineC0_dialog(self):
        self.show_dialog("New Spline C0", True)

        self.dialog.draw_button.clicked.connect(
            self.create_splineC0)

    def create_splineC0(self):
        splineC0 = SplinesC0.SplineC0(int(self.dialog.degree_line_edit.text()),
                                      self.get_intervals_from_dialog())
        self.add_control_points_to_object(splineC0)

        self.workspace.change_curve_visibility(splineC0)
        self.workspace.add_splineC0_object(splineC0)

        self.dialog.hide()
        self.dialog = None

    def show_splineC1_dialog(self):
        self.show_dialog("New Spline C1", splineC1=True)

        self.dialog.draw_button.clicked.connect(
            self.create_splineC1)

    def create_splineC1(self):
        splineC1 = SplinesC1.SplineC1(int(self.dialog.degree_line_edit.text()),
                                      self.get_intervals_from_dialog())
        self.add_control_points_to_object(splineC1)

        self.workspace.change_curve_visibility(splineC1)
        self.workspace.add_splineC1_object(splineC1)

        self.dialog.hide()
        self.dialog = None

    def show_splineC2_dialog(self):
        self.show_dialog("New Spline C2", splineC2=True)

        self.dialog.draw_button.clicked.connect(
            self.create_splineC2)

    def create_splineC2(self):
        splineC2 = SplinesC2.SplineC2(int(self.dialog.degree_line_edit.text()),
                                      self.get_intervals_from_dialog())
        self.add_control_points_to_object(splineC2)

        self.workspace.change_curve_visibility(splineC2)
        self.workspace.add_splineC2_object(splineC2)

        self.dialog.hide()
        self.dialog = None

    def show_derivative_dialog(self):
        degree, ok = QtGui.QInputDialog.getInt(
            None, "Derivative", "Derivative degree:", 1, 1, 100)

        if ok:
            for curve in self.workspace.objects[
                    self.workspace.OBJECT_BEZIER_CURVES]:
                self.workspace.change_derivative_visibility(curve, degree)

    def show_subdivision_dialog(self):
        parameter, ok = QtGui.QInputDialog.getDouble(
            None, "Subdivision", "Subdivision parameter:", 1, 0, 1)

        if ok:
            self.workspace.show_subdivision(parameter)


def main():
    app = QtGui.QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
