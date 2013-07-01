import unittest
import Vec3D
from Bezier_curves import BezierCurve


class BezierCurvesTest(unittest.TestCase):
    PARAMETERS = (0, 0.5, 1)

    def setUp(self):
        self.curve = BezierCurve()

    def tearDown(self):
        self.curve = None

    def test_append_point(self):
        points = [Vec3D.Vec3D(1, 2, -1),
                  Vec3D.Vec3D(2, 3, 4),
                  Vec3D.Vec3D(-3, 4, 8),
                  Vec3D.Vec3D(10, 10, 8)]

        for index in range(0, 4):
            self.curve.append_point(points[index])
            self.assertEqual(self.curve.control_points[index], points[index])

    def test_pop_last_point(self):
        points = [Vec3D.Vec3D(1, 2, -1),
                  Vec3D.Vec3D(2, 3, 4),
                  Vec3D.Vec3D(-3, 4, 8),
                  Vec3D.Vec3D(10, 10, 8)]

        for index in range(0, 4):
            self.curve.append_point(points[index])

        self.curve.pop_last_point()
        self.assertEqual(len(self.curve.control_points), 3)

        for index in range(0, 3):
            self.assertEqual(self.curve.control_points[index], points[index])

    def test_calculate_result_deCasteljau_algorithm_method(self):
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(0, 1, 1),
                  Vec3D.Vec3D(1, 1, 1)]
        result_points = [Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0.25, 0.75, 0.75),
                         Vec3D.Vec3D(1, 1, 1)]

        for index in range(0, 3):
            self.curve.append_point(points[index])

        for index in range(0, 3):
            algorithm_result = self.curve._deCasteljau_algorithm(
                self.PARAMETERS[index],
                self.curve.control_points)
            self.assertEqual(algorithm_result, result_points[index])

    def test_calculate_curve_interpolation(self):
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(0, 1, 1),
                  Vec3D.Vec3D(1, 1, 1)]

        for index in range(0, 3):
            self.curve.append_point(points[index])

        self.curve._curve_calculation(self.curve.control_points)

        self.assertEqual(self.curve.curve[0], Vec3D.Vec3D(0, 0, 0))
        self.assertEqual(self.curve.curve[self.curve.RANGE_STEP],
                         Vec3D.Vec3D(1, 1, 1))

    def test_calculate_linear_curves(self):
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(0, 1, 1),
                  Vec3D.Vec3D(0, 2, 2)]

        for index in range(0, 3):
            self.curve.append_point(points[index])

        curve_points = self.curve.draw()

        self.assertEqual(self.curve.curve[int(self.curve.RANGE_STEP / 2)],
                         points[1])

    def test_calculate_finite_difference(self):
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(2, 8, 6),
                  Vec3D.Vec3D(3, 5, 4),
                  Vec3D.Vec3D(4, 4, 5)]

        for index in range(0, 4):
            self.curve.append_point(points[index])

        derivative = []
        derivative = self.curve._finite_difference(2)
        self.assertEqual(derivative[0], Vec3D.Vec3D(-1, -11, -8))
        self.assertEqual(derivative[1], Vec3D.Vec3D(0, 2, 3))

        derivative = self.curve._finite_difference(3)
        self.assertEqual(derivative[0], Vec3D.Vec3D(1, 13, 11))

    def test_calculate_curve_derivative(self):
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(2, 8, 6),
                  Vec3D.Vec3D(3, 5, 4),
                  Vec3D.Vec3D(4, 4, 5)]

        for index in range(0, 4):
            self.curve.append_point(points[index])

        self.curve._derivative_calculation(2)

        self.assertEqual(self.curve.derivative[2][0],
                         Vec3D.Vec3D(-1, -11, -8))
        self.assertEqual(self.curve.derivative[2][self.curve.RANGE_STEP],
                         Vec3D.Vec3D(0, 2, 3))

    def test_calculate_subdivision_parameters(self):
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(0, 1, 1),
                  Vec3D.Vec3D(0, 2, 3)]

        result_points = {'left': [Vec3D.Vec3D(0, 0, 0),
                                  Vec3D.Vec3D(0, 0, 0),
                                  Vec3D.Vec3D(0, 0, 0)],
                         'right': [Vec3D.Vec3D(0, 0, 0),
                                   Vec3D.Vec3D(0, 1, 1),
                                   Vec3D.Vec3D(0, 2, 3)]}

        for index in range(0, 3):
            self.curve.append_point(points[index])

        curve_points = self.curve.draw()

        for index in range(0, 3):
            self.assertEqual(self.curve.subdivision_left[0][index],
                             result_points['left'][index])
            self.assertEqual(self.curve.subdivision_right[0][index],
                             result_points['right'][index])

    def test_calculate_result_subdivision_method(self):
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(0, 1, 1),
                  Vec3D.Vec3D(0, 2, 3)]

        result_points = [Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 1, 1),
                         Vec3D.Vec3D(0, 2, 3)]

        for index in range(0, 3):
            self.curve.append_point(points[index])

        subdivision = self.curve.subdivision(0, self.curve.control_points)

        curve_points = self.curve.draw()
        for index in range(0, 6):
            self.assertEqual(subdivision[index], result_points[index])

    def test_calculate_degree_elevation(self):
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(0, 1, 1),
                  Vec3D.Vec3D(0, 2, 3)]

        for index in range(0, 3):
            self.curve.append_point(points[index])

        elevation = self.curve.degree_elevation()

        self.assertEqual(elevation[1], Vec3D.Vec3D(0, 2 / 3, 2 / 3))
        self.assertEqual(len(elevation), 4)

if __name__ == '__main__':
    unittest.main()
