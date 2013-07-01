import unittest
import Vec3D
from Bezier_curves import BezierCurve
from SplinesC0 import SplineC0, InvalidData


class SplinesC0Test(unittest.TestCase):
    def test_raises_exception_negative_data(self):
        with self.assertRaises(InvalidData):
            spline = SplineC0(-3, [1, 3])

    def test_raises_exception_not_int_data(self):
        with self.assertRaises(InvalidData):
            spline = SplineC0(3.5, [1, 3])

    def test_raises_exception_no_intervals(self):
        with self.assertRaises(InvalidData):
            spline = SplineC0(2, [])

    def test_raises_exception_negative_interval_lengths(self):
        with self.assertRaises(InvalidData):
            spline = SplineC0(2, [-1, 2])

    def test_partial_curves_instance(self):
        spline = SplineC0(3, [1, 3, 3])

        for index in range(0, 3):
            self.assertIsInstance(spline.partial_curves[index], BezierCurve)

    def test_calculate_partial_curves_count(self):
        spline = SplineC0(3, [1, 3, 3])
        count = 3

        self.assertEqual(len(spline.partial_curves), 3)

    def test_calculate_count_partial_curves_points(self):
        spline = SplineC0(3, [1, 3, 3])

        for index in range(0, 10):
            spline.append_point(Vec3D.Vec3D(index, index + 1, index + 2))

        for index in range(0, 3):
            self.assertEqual(len(spline.partial_curves[index].control_points),
                             spline._degree + 1)

    def test_calculate_partial_curves_points(self):
        spline = SplineC0(3, [1, 3, 3])
        points = []

        for index in range(0, 10):
            points.append(Vec3D.Vec3D(index, index + 1, index + 2))

        for index in range(0, 10):
            spline.append_point(points[index])

        for index in range(0, 4):
            self.assertEqual(spline.partial_curves[0].control_points[index],
                             points[index])
        for index in range(3, 7):
            self.assertEqual(
                spline.partial_curves[1].control_points[index - 3],
                points[index])
        for index in range(6, 10):
            self.assertEqual(
                spline.partial_curves[2].control_points[index - 6],
                points[index])

    def test_calculate_control_points_in_replace_point_method(self):
        spline1 = SplineC0(3, [1, 3, 3])
        spline2 = SplineC0(3, [1, 3, 3])
        points = []

        for index in range(0, 10):
            spline1.append_point(Vec3D.Vec3D(index, index + 1, index + 2))

        for index in range(0, 9):
            spline2.append_point(Vec3D.Vec3D(index, index + 1, index + 2))

        spline2.append_point(Vec3D.Vec3D(11, 11, 11))
        spline1.replace_point(9, Vec3D.Vec3D(11, 11, 11))

        for index in range(0, 10):
            self.assertEqual(spline1.control_points[index],
                             spline2.control_points[index])

    def test_calculate_spline_points_in_replace_point_method(self):
        spline1 = SplineC0(3, [1, 3, 3])
        spline2 = SplineC0(3, [1, 3, 3])
        points = []

        for index in range(0, 10):
            spline1.append_point(Vec3D.Vec3D(index, index + 1, index + 2))

        for index in range(0, 9):
            spline2.append_point(Vec3D.Vec3D(index, index + 1, index + 2))

        spline2.append_point(Vec3D.Vec3D(0, 0, 0))
        spline1.replace_point(9, Vec3D.Vec3D(0, 0, 0))

        draw_spline1 = spline1.draw()
        draw_spline2 = spline2.draw()

        for index in range(0, 1000):
            self.assertEqual(draw_spline1[index], draw_spline2[index])

    def test_raises_exception_in_draw_spline_method(self):
        spline = SplineC0(3, [1, 3, 3])
        points = []

        for index in range(0, 10):
            points.append(Vec3D.Vec3D(index, index + 1, index + 2))

        for index in range(0, 9):
            spline.append_point(points[index])

        with self.assertRaises(InvalidData):
            spline.draw()

if __name__ == '__main__':
    unittest.main()
