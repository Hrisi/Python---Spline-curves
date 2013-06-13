import unittest
import Vec3D
from Bezier_curves import *


class BezierCurvesTest(unittest.TestCase):
    PARAMETER1 = 0.5
    PARAMETER2 = 0
    PARAMETER3 = 1

    def test_append_point(self):
        point = Vec3D.Vec3D(1, 2, -1)
        curve = BezierCurves(3)

        for i in range(0, 4):
            curve.append_point(point)
            self.assertEqual(curve.control_points[i], point)

    def test_deCasteljau_algorithm(self):
        curve = BezierCurves(2)
        first_point = Vec3D.Vec3D(0, 0, 0)
        second_point = Vec3D.Vec3D(0, 1, 1)
        third_point = Vec3D.Vec3D(1, 1, 1)
        curve.append_point(first_point)
        curve.append_point(second_point)
        curve.append_point(third_point)

        self.assertEqual(curve.deCasteljau_algorithm(self.PARAMETER1,
                         curve.control_points), Vec3D.Vec3D(0.25, 0.75, 0.75))
        self.assertEqual(curve.deCasteljau_algorithm(self.PARAMETER2,
                         curve.control_points), Vec3D.Vec3D(0, 0, 0))
        self.assertEqual(curve.deCasteljau_algorithm(self.PARAMETER3,
                         curve.control_points), Vec3D.Vec3D(1, 1, 1))

    def test_curve_interpolation(self):
        curve = BezierCurves(2)
        first_point = Vec3D.Vec3D(0, 0, 0)
        second_point = Vec3D.Vec3D(0, 1, 1)
        third_point = Vec3D.Vec3D(1, 1, 1)
        curve.append_point(first_point)
        curve.append_point(second_point)
        curve.append_point(third_point)

        curve.curve_calculation(curve.control_points)
        self.assertEqual(curve.curve_points[0], Vec3D.Vec3D(0, 0, 0))
        self.assertEqual(curve.curve_points[curve.RANGE_STEP],
                         Vec3D.Vec3D(1, 1, 1))

    def test_linear_curves(self):
        curve = BezierCurves(2)
        first_point = Vec3D.Vec3D(0, 0, 0)
        second_point = Vec3D.Vec3D(0, 1, 1)
        third_point = Vec3D.Vec3D(0, 2, 2)
        curve.append_point(first_point)
        curve.append_point(second_point)
        curve.append_point(third_point)

        curve.curve_calculation(curve.control_points)

        self.assertEqual(curve.curve_points[int(curve.RANGE_STEP / 2)],
                         second_point)

    def test_finite_difference(self):
        curve = BezierCurves(3)
        first_point = Vec3D.Vec3D(0, 0, 0)
        second_point = Vec3D.Vec3D(2, 8, 6)
        third_point = Vec3D.Vec3D(3, 5, 4)
        forth_point = Vec3D.Vec3D(4, 4, 5)
        curve.append_point(first_point)
        curve.append_point(second_point)
        curve.append_point(third_point)
        curve.append_point(forth_point)

        derivative = []
        derivative = curve.finite_difference(2)
        self.assertEqual(derivative[0], Vec3D.Vec3D(-1, -11, -8))
        self.assertEqual(derivative[1], Vec3D.Vec3D(0, 2, 3))

        derivative = curve.finite_difference(3)
        self.assertEqual(derivative[0], Vec3D.Vec3D(1, 13, 11))

    def test_curve_derivative(self):
        curve = BezierCurves(3)
        first_point = Vec3D.Vec3D(0, 0, 0)
        second_point = Vec3D.Vec3D(2, 8, 6)
        third_point = Vec3D.Vec3D(3, 5, 4)
        forth_point = Vec3D.Vec3D(4, 4, 5)
        curve.append_point(first_point)
        curve.append_point(second_point)
        curve.append_point(third_point)
        curve.append_point(forth_point)

        curve.curve_derivative(2)

        self.assertEqual(curve.derivative_points[2][0],
                         Vec3D.Vec3D(-1, -11, -8))
        self.assertEqual(curve.derivative_points[2][curve.RANGE_STEP],
                         Vec3D.Vec3D(0, 2, 3))

if __name__ == '__main__':
    unittest.main()
