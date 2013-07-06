import unittest
import Vec3D
from SplinesC0 import InvalidData
from SplinesC2 import *


class TestSplinesC2(unittest.TestCase):
    def test_raises_none_existing_spline_exception(self):
        with self.assertRaises(InvalidData):
            spline = SplineC2(1, [2, 1])

        with self.assertRaises(InvalidData):
            spline = SplineC2(2, [2, 1])

    def test_raises_exception_negative_data(self):
        with self.assertRaises(InvalidData):
            spline = SplineC2(-3, [1, 3])

    def test_raises_exception_not_int_data(self):
        with self.assertRaises(InvalidData):
            spline = SplineC2(3.5, [1, 3])

    def test_raises_exception_no_intervals(self):
        with self.assertRaises(InvalidData):
            spline = SplineC2(3, [])

    def test_raises_exception_negative_interval_lengths(self):
        with self.assertRaises(InvalidData):
            spline = SplineC2(3, [-1, 2])

    def test_raises_exception_draw_spline(self):
        spline = SplineC2(4, [1, 3, 3])

        for index in range(0, 7):
            spline.append_deBoor_point(Vec3D.Vec3D(index, index + 1,
                                       index + 2))

        with self.assertRaises(InvalidData):
            spline.draw()

    def test_raises_indexerror_while_append_deBoor_points(self):
        spline = SplineC2(3, [1, 3, 3])

        for index in range(0, 6):
            spline.append_deBoor_point(Vec3D.Vec3D(index, index + 1,
                                       index + 2))

        with self.assertRaises(IndexError):
            spline.append_deBoor_point(Vec3D.Vec3D(0, 0, 0))

    def test_raises_exception_while_appending_deBoor_points_to_splineC1(self):
        spline = SplineC2(3, [2, 1])

        for count in range(0, 6):
            spline.splineC1.append_deBoor_point(
                Vec3D.Vec3D(count, count + 1, count))

        with self.assertRaises(IndexError):
            spline.splineC1.append_deBoor_point(Vec3D.Vec3D(1, 1, 1))

        points = [Vec3D.Vec3D(1, 2, -1),
                  Vec3D.Vec3D(2, 3, 4),
                  Vec3D.Vec3D(-3, 4, 8),
                  Vec3D.Vec3D(10, 10, 8),
                  Vec3D.Vec3D(12, 12, 8),
                  Vec3D.Vec3D(10, 15, 8),
                  Vec3D.Vec3D(10, 12, 13)]
        spline = SplineC2(3, [2, 1])

        for count in range(0, 3):
            spline.splineC1.append_deBoor_point(points[count])

        with self.assertRaises(InvalidData):
            spline.splineC1.draw()

    def test_raise_exception_when_drawing_splineC1(self):
        points = [Vec3D.Vec3D(1, 2, -1),
                  Vec3D.Vec3D(2, 3, 4),
                  Vec3D.Vec3D(-3, 4, 8),
                  Vec3D.Vec3D(10, 10, 8),
                  Vec3D.Vec3D(12, 12, 8),
                  Vec3D.Vec3D(10, 15, 8),
                  Vec3D.Vec3D(10, 12, 13)]
        spline = SplineC2(3, [2, 1])

        for count in range(0, 3):
            spline.splineC1.append_deBoor_point(points[count])

        with self.assertRaises(InvalidData):
            spline.splineC1.draw()

    def test_Bezier_points_count(self):
        spline = SplineC2(3, [1, 3, 3])
        count = 10

        for index in range(0, 6):
            spline.append_deBoor_point(Vec3D.Vec3D(index, index + 1,
                                       index + 2))

        spline.draw()
        self.assertEqual(count,
                         spline.splineC1.splineC0.points_count)

    def test_count_deBoor_points_for_splineC1(self):
        spline = SplineC2(3, [1, 3, 3])
        count = 8

        for index in range(0, 6):
            spline.append_deBoor_point(Vec3D.Vec3D(index, index + 1,
                                       index + 2))
        spline.draw()
        self.assertEqual(count,
                         len(spline.splineC1.deBoor_points))

    def test_calculation_for_deBoor_points_for_splineC1(self):
        spline = SplineC2(3, [1, 3])
        splineC2 = SplineC2(3, [1, 5])

        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(0, 1, 0),
                  Vec3D.Vec3D(2, 1, 0),
                  Vec3D.Vec3D(3, 0, 0),
                  Vec3D.Vec3D(4, -1, 0),
                  Vec3D.Vec3D(4, -1, 0)]

        for index in range(0, 5):
            splineC2.append_deBoor_point(points[index])
        splineC2.draw()
        self.assertEqual(6,
                         len(splineC2.splineC1.deBoor_points))

        points = [Vec3D.Vec3D(1, 1, 1),
                  Vec3D.Vec3D(4, 4, 4),
                  Vec3D.Vec3D(8, 4, 4),
                  Vec3D.Vec3D(4, 8, 4),
                  Vec3D.Vec3D(8, 8, 6)]

        result_points = [Vec3D.Vec3D(1, 1, 1),
                         Vec3D.Vec3D(4, 4, 4),
                         Vec3D.Vec3D(5, 4, 4),
                         Vec3D.Vec3D(7, 5, 4),
                         Vec3D.Vec3D(4, 8, 4),
                         Vec3D.Vec3D(8, 8, 6)]

        for index in range(0, 5):
            spline.append_deBoor_point(points[index])

        spline.draw()

        for index in range(0, 6):
            self.assertEqual(result_points[index],
                             spline.splineC1.deBoor_points[index])

    def test_result_in_replace_point_method(self):
        spline = SplineC2(3, [1, 3, 3, 4])

        for index in range(0, 7):
            spline.append_deBoor_point(Vec3D.Vec3D(index, index + 1,
                                       index + 2))

        spline.draw()

        spline.replace_point(0, Vec3D.Vec3D(0, 0, 0))
        self.assertEqual(spline.deBoor_points[0], Vec3D.Vec3D(0, 0, 0))
        self.assertEqual(spline.splineC1.deBoor_points[0],
                         Vec3D.Vec3D(0, 0, 0))

        spline.replace_point(3, Vec3D.Vec3D(0, 0, 0))
        self.assertEqual(spline.deBoor_points[3], Vec3D.Vec3D(0, 0, 0))

        spline.replace_point(6, Vec3D.Vec3D(0, 0, 0))
        self.assertEqual(spline.deBoor_points[6], Vec3D.Vec3D(0, 0, 0))

    def test_raises_exception_when_drawing_splineC0(self):
        points = [Vec3D.Vec3D(1, 2, -1),
                  Vec3D.Vec3D(2, 3, 4),
                  Vec3D.Vec3D(-3, 4, 8),
                  Vec3D.Vec3D(10, 10, 8),
                  Vec3D.Vec3D(12, 12, 8),
                  Vec3D.Vec3D(10, 15, 8),
                  Vec3D.Vec3D(10, 12, 13)]
        spline = SplineC2(3, [2, 1])

        for count in range(0, 6):
            spline.splineC1.append_deBoor_point(points[count])

        spline.splineC1.draw()

        control_points = spline.splineC1.splineC0.control_points
        control_points.pop()
        spline.splineC1.splineC0.control_points = control_points

        with self.assertRaises(InvalidData):
            spline.splineC1.splineC0.draw()

    def test_raises_indexerror_while_appending_points_to_splineC0(self):
        spline = SplineC2(3, [1, 3, 3])

        for index in range(0, 8):
            spline.splineC1.append_deBoor_point(
                Vec3D.Vec3D(index, index + 3, index))

        spline.splineC1.draw()

        with self.assertRaises(IndexError):
            spline.splineC1.splineC0.append_point(Vec3D.Vec3D(0, 0, 0))

    def test_calculate_control_points_in_pop_points_from_partial_curve(self):
        spline = SplineC2(3, [1, 3, 3])
        points = []

        for index in range(0, 8):
            points.append(Vec3D.Vec3D(index, index + 1, index + 2))

        for index in range(0, 6):
            spline.append_deBoor_point(points[index])

        spline.draw()

        for index in range(0, 4):
            spline.splineC1.splineC0.partial_curves[2].pop_last_point()

        self.assertEqual(
            spline.splineC1.splineC0.partial_curves[2].control_points, [])

    def test_calculate_partial_curve_derivative(self):
        spline = SplineC2(3, [1, 3, 3])
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(2, 8, 6),
                  Vec3D.Vec3D(3, 5, 4),
                  Vec3D.Vec3D(4, 4, 5)]

        for index in range(0, 6):
            spline.append_deBoor_point(Vec3D.Vec3D(index, index, index))

        spline.draw()

        splineC1 = spline.splineC1.splineC0
        for index in range(0, 4):
            splineC1.partial_curves[2].control_points[index] = points[index]

        splineC1.partial_curves[2].draw_derivative(2)
        self.assertEqual(splineC1.partial_curves[2].derivative[2][0],
                         Vec3D.Vec3D(-1, -11, -8))
        self.assertEqual(splineC1.partial_curves[2].derivative[2][
            splineC1.partial_curves[2].RANGE_STEP], Vec3D.Vec3D(0, 2, 3))

    def test_calculate_partial_curves_subdivision(self):
        spline = SplineC2(3, [1, 3, 3])
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(0, 1, 1),
                  Vec3D.Vec3D(0, 2, 3)]
        result_points = [Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 1, 1),
                         Vec3D.Vec3D(0, 2, 3)]

        splineC1 = spline.splineC1.splineC0

        for index in range(0, 3):
            splineC1.partial_curves[2].append_point(points[index])

        subdivision = splineC1.partial_curves[2].subdivision(
            0, splineC1.partial_curves[2].control_points)

        curve_points = splineC1.partial_curves[2].draw()
        for index in range(0, 6):
            self.assertEqual(subdivision[index], result_points[index])

    def test_calculate_partial_curves_degree_elevation(self):
        spline = SplineC2(3, [1, 3, 3])
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(0, 1, 1),
                  Vec3D.Vec3D(0, 2, 3)]
        result_points = [Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 1, 1),
                         Vec3D.Vec3D(0, 2, 3)]

        splineC1 = spline.splineC1.splineC0

        for index in range(0, 3):
            splineC1.partial_curves[2].append_point(points[index])

        elevation = splineC1.partial_curves[2].degree_elevation()

        self.assertEqual(elevation[1], Vec3D.Vec3D(0, 2 / 3, 2 / 3))
        self.assertEqual(len(elevation), 4)

    def test_calculate_raises_indexerror_when_drawing_partial_curves(self):
        spline = SplineC2(3, [1, 3, 3])
        points = []

        splineC1 = spline.splineC1.splineC0

        for index in range(0, 10):
            points.append(Vec3D.Vec3D(index, index + 1, index + 2))

        for index in range(0, 10):
            splineC1.append_point(points[index])

        with self.assertRaises(IndexError):
            splineC1.partial_curves[2].draw_derivative(4)


if __name__ == '__main__':
    unittest.main()
