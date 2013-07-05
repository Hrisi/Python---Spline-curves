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

    def test_raises_indexerror_while_appending_points(self):
        spline = SplineC0(3, [1, 3, 3])

        for index in range(0, 10):
            spline.append_point(Vec3D.Vec3D(index, index + 3, index + 3))

        with self.assertRaises(IndexError):
            spline.append_point(Vec3D.Vec3D(0, 0, 0))

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
        spline = SplineC0(3, [1, 3, 3])

        for index in range(0, 10):
            spline.append_point(Vec3D.Vec3D(index, index + 1, index + 2))

        spline.replace_point(9, Vec3D.Vec3D(11, 11, 11))
        self.assertEqual(spline.control_points[9], Vec3D.Vec3D(11, 11, 11))
        self.assertEqual(spline.partial_curves[2].control_points[3],
                         Vec3D.Vec3D(11, 11, 11))

        spline.replace_point(0, Vec3D.Vec3D(0, 0, 0))
        self.assertEqual(spline.control_points[0], Vec3D.Vec3D(0, 0, 0))
        self.assertEqual(spline.partial_curves[0].control_points[0],
                         Vec3D.Vec3D(0, 0, 0))

        spline.replace_point(3, Vec3D.Vec3D(4, 4, 4))
        self.assertEqual(spline.control_points[3], Vec3D.Vec3D(4, 4, 4))
        self.assertEqual(spline.partial_curves[1].control_points[0],
                         Vec3D.Vec3D(4, 4, 4))
        self.assertEqual(spline.partial_curves[0].control_points[3],
                         Vec3D.Vec3D(4, 4, 4))

        spline.replace_point(4, Vec3D.Vec3D(3, 3, 3))
        self.assertEqual(spline.control_points[4], Vec3D.Vec3D(3, 3, 3))
        self.assertEqual(spline.partial_curves[1].control_points[1],
                         Vec3D.Vec3D(3, 3, 3))

        spline.replace_point(2, Vec3D.Vec3D(11, 11, 11))
        self.assertEqual(spline.control_points[2], Vec3D.Vec3D(11, 11, 11))
        self.assertEqual(spline.partial_curves[0].control_points[2],
                         Vec3D.Vec3D(11, 11, 11))

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

    def test_calculate_control_points_in_pop_points_from_partial_curve(self):
        spline = SplineC0(3, [1, 3, 3])
        points = []

        for index in range(0, 10):
            points.append(Vec3D.Vec3D(index, index + 1, index + 2))

        for index in range(0, 10):
            spline.append_point(points[index])

        for index in range(0, 4):
            spline.partial_curves[2].pop_last_point()

        self.assertEqual(spline.partial_curves[2].control_points, [])

    def test_calculate_partial_curve_derivative(self):
        spline = SplineC0(3, [1, 3, 3])
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(2, 8, 6),
                  Vec3D.Vec3D(3, 5, 4),
                  Vec3D.Vec3D(4, 4, 5)]

        for index in range(0, 6):
            spline.append_point(Vec3D.Vec3D(index, index, index))

        for index in range(0, 4):
            spline.append_point(points[index])

        spline.partial_curves[2].draw_derivative(2)
        self.assertEqual(spline.partial_curves[2].derivative[2][0],
                         Vec3D.Vec3D(-1, -11, -8))
        self.assertEqual(spline.partial_curves[2].derivative[2][
            spline.partial_curves[2].RANGE_STEP], Vec3D.Vec3D(0, 2, 3))

    def test_calculate_partial_curves_subdivision(self):
        spline = SplineC0(2, [1, 3, 3])
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(0, 1, 1),
                  Vec3D.Vec3D(0, 2, 3)]
        result_points = [Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 1, 1),
                         Vec3D.Vec3D(0, 2, 3)]

        for index in range(0, 4):
            spline.append_point(Vec3D.Vec3D(index, index, index))

        for index in range(0, 3):
            spline.append_point(points[index])

        subdivision = spline.partial_curves[2].subdivision(
            0, spline.partial_curves[2].control_points)

        curve_points = spline.partial_curves[2].draw()
        for index in range(0, 6):
            self.assertEqual(subdivision[index], result_points[index])

    def test_calculate_partial_curves_degree_elevation(self):
        spline = SplineC0(2, [1, 3, 3])
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(0, 1, 1),
                  Vec3D.Vec3D(0, 2, 3)]
        result_points = [Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 1, 1),
                         Vec3D.Vec3D(0, 2, 3)]

        for index in range(0, 4):
            spline.append_point(Vec3D.Vec3D(index, index, index))

        for index in range(0, 3):
            spline.append_point(points[index])

        elevation = spline.partial_curves[2].degree_elevation()

        self.assertEqual(elevation[1], Vec3D.Vec3D(0, 2 / 3, 2 / 3))
        self.assertEqual(len(elevation), 4)

    def test_calculate_raises_indexerror_when_drawing_partial_curves(self):
        spline = SplineC0(3, [1, 3, 3])
        points = []

        for index in range(0, 10):
            points.append(Vec3D.Vec3D(index, index + 1, index + 2))

        for index in range(0, 10):
            spline.append_point(points[index])

        with self.assertRaises(IndexError):
            spline.partial_curves[2].draw_derivative(4)

if __name__ == '__main__':
    unittest.main()
