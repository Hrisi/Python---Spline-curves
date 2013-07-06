from PyQt4 import QtGui, QtCore


class MainDialog(QtGui.QDialog):
    DEGREE_LABEL = "Enter spline degree:"
    INTERVALS_LABEL = "Enter intervals lengths:"
    ADD_POINTS_TEXT = "Add points"
    DRAW_TEXT = "Draw"

    def __init__(self, title, splineC0, splineC1, splineC2):
        super(MainDialog, self).__init__()

        self.setWindowTitle(title)
        self.setMinimumSize(250, 300)
        self.fixed_control_points = None
        self.splineC0 = splineC0
        self.splineC1 = splineC1
        self.splineC2 = splineC2

        self.init_degree_and_intervals()
        self.init_scrollable_area()

        self.main_frame_layout = QtGui.QVBoxLayout()
        self.main_frame_layout.addWidget(self.degree_frame)
        self.main_frame_layout.addWidget(self.intervals_scrollable)
        self.main_frame_layout.addWidget(self.add_points_button)
        self.main_frame_layout.addWidget(self.scrollable)
        self.main_frame_layout.addWidget(self.draw_button)

        self.setLayout(self.main_frame_layout)

        if splineC0 or splineC1 or splineC2:
            self.scrollable.hide()
            self.draw_button.hide()
        else:
            self.degree_frame.hide()
            self.intervals_scrollable.hide()
            self.add_points_button.hide()

    def init_degree_and_intervals(self):
        self.degree_label = QtGui.QLabel(self.DEGREE_LABEL)
        self.degree_line_edit = QtGui.QLineEdit()
        self.degree_line_edit.setValidator(QtGui.QIntValidator())
        self.degree_label.setBuddy(self.degree_line_edit)

        self.intervals_line_edit = []
        self.intervals_label = QtGui.QLabel(self.INTERVALS_LABEL)

        self.degree_frame = QtGui.QFrame()
        self.degree_frame_layout = QtGui.QHBoxLayout()
        self.degree_frame_layout.addWidget(self.degree_label)
        self.degree_frame_layout.addWidget(self.degree_line_edit)
        self.degree_frame.setLayout(self.degree_frame_layout)

        self.intervals_scrollable = QtGui.QScrollArea()
        self.intervals_scrollable.setWidgetResizable(True)
        self.intervals_scrollable.setEnabled(True)
        self.intervals_frame = QtGui.QWidget()
        self.intervals_scrollable.setWidget(self.intervals_frame)
        self.intervals_frame_layout = QtGui.QVBoxLayout()
        self.intervals_frame_layout.addWidget(self.intervals_label)

        self.add_interval_input()
        self.intervals_label.setBuddy(self.intervals_line_edit[0])

        self.intervals_frame.setLayout(self.intervals_frame_layout)

        self.add_points_button = QtGui.QPushButton(self.ADD_POINTS_TEXT)
        self.add_points_button.setDefault(True)

    def init_scrollable_area(self):
        self.scrollable = QtGui.QScrollArea()
        self.scrollable.setWidgetResizable(True)
        self.scrollable.setEnabled(True)
        self.add_points_widget = QtGui.QWidget()
        self.scrollable.setWidget(self.add_points_widget)
        self.add_points_button.clicked.connect(self.set_visible)

        self.add_points_line_edit = []
        self.add_points_layout = QtGui.QVBoxLayout()
        self.point_coordinates_frame = []
        self.point_coordinates_layout = []

        self.add_point_input()

        self.add_points_widget.setLayout(self.add_points_layout)

        self.draw_button = QtGui.QPushButton(self.DRAW_TEXT)
        self.draw_button.setDefault(True)

    def set_visible(self):
        self.scrollable.setVisible(True)
        self.draw_button.setVisible(True)

    def add_interval_input(self):
        self.intervals_line_edit.append(QtGui.QLineEdit())
        self.intervals_line_edit[-1].textChanged.connect(self.add_interval)
        self.intervals_frame_layout.addWidget(self.intervals_line_edit[-1])
        self.intervals_line_edit[-1].setValidator(QtGui.QDoubleValidator())

    def add_interval(self):
        if self.intervals_line_edit[-1].text() != "":
            self.intervals_line_edit[-1].textChanged.disconnect()
            self.add_interval_input()

    def add_point_input(self):
        if self.splineC0 and self.degree_line_edit.text() != "":
            self.fixed_control_points = (
                int(self.degree_line_edit.text()) *
                (len(self.intervals_line_edit) - 1) + 1)

        if self.splineC1 and self.degree_line_edit.text() != "":
            self.fixed_control_points = (
                2 * int(self.degree_line_edit.text()) +
                (int(self.degree_line_edit.text()) - 1) *
                (len(self.intervals_line_edit) - 3))

        if self.splineC2 and self.degree_line_edit.text() != "":
            self.fixed_control_points = (
                2 * (int(self.degree_line_edit.text()) - 1) +
                len(self.intervals_line_edit) - 2)

        if (self.fixed_control_points and
                self.fixed_control_points == len(self.add_points_line_edit)):
            return

        self.point_coordinates_frame.append(QtGui.QFrame())
        self.point_coordinates_layout.append(QtGui.QHBoxLayout())
        self.add_points_coordinate = []

        for index in range(0, 3):
            self.add_points_coordinate.append(QtGui.QLineEdit())
            self.add_points_coordinate[index].setValidator(
                QtGui.QDoubleValidator())

        self.add_points_line_edit.append(self.add_points_coordinate)
        self.add_points_line_edit[-1][2].textChanged.connect(self.add_point)

        for index in range(0, 3):
            self.point_coordinates_layout[-1].addWidget(
                self.add_points_line_edit[-1][index])

        self.point_coordinates_frame[-1].setLayout(
            self.point_coordinates_layout[-1])
        self.add_points_layout.addWidget(self.point_coordinates_frame[-1])

    def add_point(self):
        if self.add_points_line_edit[-1][2].text() != "":
            self.add_points_line_edit[-1][2].textChanged.disconnect()
            self.add_point_input()
