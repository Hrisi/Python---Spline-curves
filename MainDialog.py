from PyQt4 import QtGui, QtCore


class MainDialog(QtGui.QDialog):
    DEGREE_LABEL = "Enter spline degree"
    INTERVALS_LABEL = "Enter intervals"
    ADD_POINTS_TEXT = "Add points"
    DRAW_TEXT = "Draw"

    def __init__(self, title, fixed_control_points=None):
        super(MainDialog, self).__init__()

        self.setWindowTitle(title)

        self.init_degree_and_intervals()
        self.init_scrollable_area()

        self.main_frame_layout = QtGui.QVBoxLayout()
        self.main_frame_layout.addWidget(self.degree_frame)
        self.main_frame_layout.addWidget(self.intervals_frame)
        self.main_frame_layout.addWidget(self.add_points_button)
        self.main_frame_layout.addWidget(self.scrollable)

        self.setLayout(self.main_frame_layout)

        if fixed_control_points:
            #self.degree_frame.show()
            #self.intervals_frame.show()
            self.scrollable.hide()
        else:
            #self.scrollable.show()
            self.degree_frame.hide()
            self.intervals_frame.hide()

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

        self.intervals_frame = QtGui.QFrame()
        self.intervals_frame_layout = QtGui.QVBoxLayout()
        self.intervals_frame_layout.addWidget(self.intervals_label)
        self.append_interval_input()
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
        QtGui.QMainWindow.connect(self.add_points_button,
                                  QtCore.SIGNAL('clicked()'),
                                  self.set_visible)

        self.draw_button = QtGui.QPushButton(self.DRAW_TEXT)
        self.draw_button.setDefault(True)

        self.add_points_layout = QtGui.QVBoxLayout()
        self.point_coordinates_upper_frame = QtGui.QFrame()
        self.point_coordinates_upper_layout = QtGui.QHBoxLayout()
        self.point_coordinates_lower_frame = QtGui.QFrame()
        self.point_coordinates_lower_layout = QtGui.QHBoxLayout()

        for index in range(0, 3):
            self.point_coordinates_upper_layout.addWidget(QtGui.QInputDialog())
            self.point_coordinates_lower_layout.addWidget(QtGui.QInputDialog())

        self.point_coordinates_upper_frame.setLayout(
            self.point_coordinates_upper_layout)
        self.point_coordinates_lower_frame.setLayout(
            self.point_coordinates_lower_layout)

        self.add_points_layout.addWidget(self.point_coordinates_upper_frame)
        self.add_points_layout.addWidget(self.point_coordinates_lower_frame)
        self.add_points_layout.addWidget(QtGui.QPushButton(self.draw_button))

        self.add_points_widget.setLayout(self.add_points_layout)

    def set_visible(self):
        print("Foo")
        self.scrollable.setVisible(True)

    def append_interval_input(self):
        self.intervals_line_edit.append(QtGui.QLineEdit())
        self.intervals_line_edit[-1].textChanged.connect(self.add_interval)
        self.intervals_frame_layout.addWidget(self.intervals_line_edit[-1])
        self.intervals_line_edit[-1].setValidator(QtGui.QDoubleValidator())
        #self.intervals_line_edit[0].setRange(0, 100000)

    def add_interval(self):
        if self.intervals_line_edit[-1].text() != "":
            self.intervals_line_edit[-1].textChanged.disconnect()
            self.append_interval_input()
