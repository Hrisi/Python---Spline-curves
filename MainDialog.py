from PyQt4 import QtGui, QtCore


class MainDialog(QtGui.QDialog):
    DEGREE_LABEL = "&Enter spline degree"
    INTERVALS_LABEL = "&Enter intervals"
    ADD_POINTS_TEXT = "&Add points"
    DRAW_TEXT = "&Draw"

    def __init__(self):
        super(MainDialog, self).__init__()

        self.setWindowTitle('Splines')
        self.degree_label = QtGui.QLabel(self.DEGREE_LABEL)
        self.intervals_count_label = QtGui.QLabel(self.INTERVALS_LABEL)
        self.degree_line_edit = QtGui.QLineEdit()
        self.degree_label.setBuddy(self.degree_line_edit)
        self.intervals_count_line_edit = QtGui.QLineEdit()
        self.intervals_count_line_edit.setValidator(QtGui.QIntValidator())
        self.intervals_count_label.setBuddy(self.intervals_count_line_edit)

        self.degree_frame = QtGui.QFrame()
        self.degree_frame_layout = QtGui.QHBoxLayout()
        self.degree_frame_layout.addWidget(self.degree_label)
        self.degree_frame_layout.addWidget(self.degree_line_edit)
        self.degree_frame.setLayout(self.degree_frame_layout)

        self.intervals_frame = QtGui.QFrame()
        self.intervals_frame_layout = QtGui.QHBoxLayout()
        self.intervals_frame_layout.addWidget(self.intervals_count_label)
        self.intervals_frame_layout.addWidget(self.intervals_count_line_edit)
        self.intervals_frame.setLayout(self.intervals_frame_layout)

        self.add_points_button = QtGui.QPushButton(self.ADD_POINTS_TEXT)
        self.add_points_button.setDefault(True)
        self.draw_button = QtGui.QPushButton(self.DRAW_TEXT)
        self.draw_button.setDefault(True)

        self.add_points_widget = QtGui.QScrollArea()
        self.add_points_widget.setWidgetResizable(True)
        self.add_points_widget.setEnabled(True)
        self.tmp = QtGui.QWidget()
        self.add_points_widget.setWidget(self.tmp)
        QtGui.QMainWindow.connect(self.add_points_button,
                                  QtCore.SIGNAL('clicked()'),
                                  self.set_visible)

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

        self.tmp.setLayout(self.add_points_layout)

        #self.main_frame = QtGui.QFrame(self)
        #self.main_frame.setMinimumSize(300, 200)
        self.main_frame_layout = QtGui.QVBoxLayout()
        self.main_frame_layout.addWidget(self.degree_frame)
        self.main_frame_layout.addWidget(self.intervals_frame)
        self.main_frame_layout.addWidget(self.add_points_button)
        self.main_frame_layout.addWidget(self.add_points_widget)

        self.add_points_widget.hide()

        self.setLayout(self.main_frame_layout)

    def set_visible(self):
        print("Foo")
        print(self.intervals_count_line_edit.text())
        self.add_points_widget.setVisible(True)
