import SplinesC0


class SplineC1:
    NONE_EXISTING_SPLINE_MESSAGE = "Please increase the degree!"
    INCORRECT_COUNT_DEBOOR_POINTS = "Please insert more deBoor points!"

    def __init__(self, degree, interval):

        if (degree <= 1):
            raise SplinesC0.InvalidData(self.NONE_EXISTING_SPLINE_MESSAGE)

        self.splineC0 = SplinesC0.SplineC0(degree, interval)
        self.deBoor_points = []
        self.partial_curve_counter = 0

    def append_deBoor_point(self, point):
        if len(self.deBoor_points) == (self.splineC0.points_count -
                                       len(self.splineC0.intervals) + 1):
            raise IndexError

        self.deBoor_points.append(point)

    def _append_Bezier_points(self):
        counter = 0

        for count_point in range(0, len(self.deBoor_points)):
            self.splineC0.append_point(self.deBoor_points[count_point])
            len_points = len(self.splineC0.control_points)

            if (len_points % self.splineC0._degree == 0 and
                    len_points < (self.splineC0.points_count - 1) and
                    count_point > 0):
                counter += 1
                denominator = (self.splineC0.intervals[counter - 1] +
                               self.splineC0.intervals[counter])
                numerator = (self.splineC0.intervals[counter] *
                             self.deBoor_points[count_point] +
                             self.splineC0.intervals[counter - 1] *
                             self.deBoor_points[count_point + 1])
                calculated_point = numerator * (1 / denominator)
                self.splineC0.append_point(calculated_point)

    def draw_spline(self):
        if len(self.deBoor_points) < (self.splineC0.points_count -
                                      len(self.splineC0.intervals) + 1):
            raise SplinesC0.InvalidData(self.INCORRECT_COUNT_DEBOOR_POINTS)

        self._append_Bezier_points()
        return self.splineC0.draw_spline()
