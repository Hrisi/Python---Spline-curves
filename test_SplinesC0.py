import unittest
import Vec3D
from SplinesC0 import *


class SplinesC0Test(unittest.TestCase):
    def test_raises_exception_negative_data(self):
        with self.assertRaises(InvalidData):
            spline = SplineC0(-3, [[1, 2], [2, 5]])

    def test_raises_exception_not_int_data(self):
        with self.assertRaises(InvalidData):
            spline = SplineC0(3.5, [[1, 2], [2, 5]])

    def test_raises_exception_no_intervals(self):
        with self.assertRaises(InvalidData):
            spline = SplineC0(2, [])

    def test_raises_exception_incorrect_input_intervals(self):
        with self.assertRaises(InvalidData):
            spline = SplineC0(2, [[4, 5], [7, 8]])

    def test_partial_curves_instance(self):
        spline = SplineC0(3, [[1, 2], [2, 5], [5, 8]])

        for i in range(0, 3):
            self.assertIsInstance(spline.partial_curves[i],
                                  Bezier_curves.BezierCurve)

    def test_partial_curves_count(self):
        spline = SplineC0(3, [[1, 2], [2, 5], [5, 8]])
        count = 3

        self.assertEqual(len(spline.partial_curves), 3)

    def test_partial_curves_points_count(self):
        spline = SplineC0(3, [[1, 2], [2, 5], [5, 8]])

        for i in range(0, 10):
            spline.append_point(Vec3D.Vec3D(i, i + 1, i + 2))

        for i in range(0, 3):
            self.assertEqual(len(spline.partial_curves[i].control_points),
                             spline._degree + 1)

    def test_partial_curves_points_calculation(self):
        spline = SplineC0(3, [[1, 2], [2, 5], [5, 8]])
        points = []

        for i in range(0, 10):
            points.append(Vec3D.Vec3D(i, i + 1, i + 2))

        for i in range(0, 10):
            spline.append_point(points[i])

        for i in range(0, 4):
            self.assertEqual(spline.partial_curves[0].control_points[i],
                             points[i])
        for i in range(3, 7):
            self.assertEqual(spline.partial_curves[1].control_points[i - 3],
                             points[i])
        for i in range(6, 10):
            self.assertEqual(spline.partial_curves[2].control_points[i - 6],
                             points[i])

    def test_draw_spline_raise_exception(self):
        spline = SplineC0(3, [[1, 2], [2, 5], [5, 8]])
        points = []

        for i in range(0, 10):
            points.append(Vec3D.Vec3D(i, i + 1, i + 2))

        for i in range(0, 9):
            spline.append_point(points[i])

        with self.assertRaises(InvalidData):
            spline.draw()

if __name__ == '__main__':
    unittest.main()
