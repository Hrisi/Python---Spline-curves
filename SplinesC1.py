import SplinesC0


class SplineC1:
    NONE_EXISTING_SPLINE_MESSAGE = "Please increase the degree!"

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
        counter = self.partial_curve_counter

        for count_point in range(0, len(self.deBoor_points)):
            self.splineC0.append_point(self.deBoor_points[count_point])
            len_points = len(self.splineC0.control_points)

            if ((len_points - 1) % self.splineC0._degree == 0 and
                    len_points < self.splineC0.points_count and
                    count_point > 0):
                counter += 1
                print(counter, count_point, len_points)
                denominator = (self.splineC0.intervals[counter - 1] +
                               self.splineC0.intervals[counter])
                numerator = (self.splineC0.intervals[counter] *
                             self.deBoor_points[count_point - 1] +
                             self.splineC0.intervals[counter - 1] *
                             self.deBoor_points[count_point])

                calculated_point = numerator * (1 / denominator)
                self.splineC0.append_point(calculated_point)

    def draw_spline(self):
        self._append_Bezier_points()
        return self.splineC0.draw_spline()
