import SplinesC0


class SplineC1:
    NONE_EXISTING_SPLINE = "Please increase the degree!"

    def __init__(self, degree, interval):

        if (degree <= 1):
            raise (self.NONE_EXISTING_SPLINE)

        self.spline = SplinesC0.SplineC0(degree, interval)
        self.deBoor_points = []
        self.partial_curve_counter = 0

    def append_deBoor_point(self, point):
        if len(self.deBoor_points) == 2 * len(self.spline._degree):
            raise IndexError

        self.deBoor_points.append(point)

    def _append_Bezier_points(self):
        counter = self.partial_curve_counter
        len_points = self.spline.counts_count
        for count_point in range(0, len_points):
            if i % self.spline._degree == 0 and count_point < len_points - 1:
                counter += 1
                denominator = (self.spline.interval[counter - 1] +
                               self.spline.interval[counter])
                numerator = (self.spline.interval[counter] *
                             self.deBoor_points[count_point - 1] +
                             self.spline.interval[count] *
                             self.deBoor_points[count_point - 1])

                calculated_point = numerator / denominator
                self.spline.append_point(calculated_point)

                continue

            self.spline.append_point(self.deBoor_points[count_point])

    def draw_spline(self):
        self._append_Bezier_points()
        self.spline.draw()
