import unittest
import Vec3D
from SplinesC0 import InvalidData
from SplinesC1 import SplineC1


class TestSplinesC1(unittest.TestCase):
    def test_raises_none_existing_spline_exception(self):
        with self.assertRaises(InvalidData):
            spline = SplineC1(1, [2, 1])

    def test_raises_exception_while_appending_deBoor_points(self):
        spline = SplineC1(3, [2, 1])

        for count in range(0, 6):
            spline.append_deBoor_point(Vec3D.Vec3D(count, count + 1, count))

        with self.assertRaises(IndexError):
            spline.append_deBoor_point(Vec3D.Vec3D(1, 1, 1))

    def test_raises_exception_negative_data(self):
        with self.assertRaises(InvalidData):
            spline = SplineC1(-3, [1, 3])

    def test_raises_exception_not_int_data(self):
        with self.assertRaises(InvalidData):
            spline = SplineC1(3.5, [1, 3])

    def test_raises_exception_no_intervals(self):
        with self.assertRaises(InvalidData):
            spline = SplineC1(2, [])

    def test_raises_exception_negative_interval_lengths(self):
        with self.assertRaises(InvalidData):
            spline = SplineC1(2, [-1, 2])

    def test_raises_indexerror_while_appending_points_to_splineC0(self):
        spline = SplineC1(3, [1, 3, 3])

        for index in range(0, 8):
            spline.append_deBoor_point(Vec3D.Vec3D(index, index + 3, index))

        spline.draw()

        with self.assertRaises(IndexError):
            spline.splineC0.append_point(Vec3D.Vec3D(0, 0, 0))

    def test_Bezier_points_count(self):
        spline = SplineC1(3, [2, 1])

        for count in range(0, 6):
            spline.append_deBoor_point(Vec3D.Vec3D(count, count + 1, count))

        spline.draw()
        self.assertEqual(spline.splineC0.points_count,
                         len(spline.splineC0.control_points))

    def test_correct_calculation_Bezier_points(self):
        points = [Vec3D.Vec3D(0, 1, 1),
                  Vec3D.Vec3D(0, 2, 1),
                  Vec3D.Vec3D(0, 3, 3),
                  Vec3D.Vec3D(2, 5, 5),
                  Vec3D.Vec3D(3, 6, 6),
                  Vec3D.Vec3D(2, 2, 6),
                  Vec3D.Vec3D(2, 2, 7.5),
                  Vec3D.Vec3D(2, 2, 12),
                  Vec3D.Vec3D(3, 5, 8),
                  Vec3D.Vec3D(4, 2, 9)]
        spline = SplineC1(3, [2, 1, 3])

        for count in range(0, 3):
            spline.append_deBoor_point(points[count])

        for count in range(4, 6):
            spline.append_deBoor_point(points[count])

        for count in range(7, 10):
            spline.append_deBoor_point(points[count])

        spline.draw()

        for count in range(0, 10):
            self.assertEqual(points[count],
                             spline.splineC0.control_points[count])

    def test_calculate_control_points_after_replacing_point(self):
        points = [Vec3D.Vec3D(0, 1, 1),
                  Vec3D.Vec3D(0, 2, 1),
                  Vec3D.Vec3D(0, 3, 3),
                  Vec3D.Vec3D(2, 5, 5),
                  Vec3D.Vec3D(3, 6, 6),
                  Vec3D.Vec3D(2, 2, 6),
                  Vec3D.Vec3D(2, 2, 7.5),
                  Vec3D.Vec3D(2, 2, 12),
                  Vec3D.Vec3D(3, 5, 8),
                  Vec3D.Vec3D(4, 2, 9)]
        spline = SplineC1(3, [2, 1, 3])

        for count in range(0, 3):
            spline.append_deBoor_point(points[count])

        for count in range(4, 6):
            spline.append_deBoor_point(points[count])

        for count in range(7, 9):
            spline.append_deBoor_point(points[count])

        spline.append_deBoor_point(Vec3D.Vec3D(0, 0, 0))
        spline.draw()
        spline.replace_point(7, points[9])

        for index in (0, 8):
            self.assertEqual(spline.control_points[index],
                             points[index])

        spline.replace_point(0, points[2])
        self.assertEqual(spline.control_points[0], points[2])
        self.assertEqual(spline.splineC0.control_points[0], points[2])

        spline.replace_point(3, points[2])
        self.assertEqual(spline.control_points[3], points[2])
        self.assertEqual(spline.splineC0.control_points[4], points[2])

        spline.replace_point(4, points[2])
        self.assertEqual(spline.control_points[4], points[2])
        self.assertEqual(spline.splineC0.control_points[5], points[2])

        spline.replace_point(2, points[2])
        self.assertEqual(spline.control_points[2], points[2])
        self.assertEqual(spline.splineC0.control_points[2], points[2])

    def test_draw_spline_raise_exception(self):
        points = [Vec3D.Vec3D(1, 2, -1),
                  Vec3D.Vec3D(2, 3, 4),
                  Vec3D.Vec3D(-3, 4, 8),
                  Vec3D.Vec3D(10, 10, 8),
                  Vec3D.Vec3D(12, 12, 8),
                  Vec3D.Vec3D(10, 15, 8),
                  Vec3D.Vec3D(10, 12, 13)]
        spline = SplineC1(3, [2, 1])

        for count in range(0, 3):
            spline.append_deBoor_point(points[count])

        with self.assertRaises(InvalidData):
            spline.draw()

    def test_raises_exception_when_drawing_splineC0(self):
        points = [Vec3D.Vec3D(1, 2, -1),
                  Vec3D.Vec3D(2, 3, 4),
                  Vec3D.Vec3D(-3, 4, 8),
                  Vec3D.Vec3D(10, 10, 8),
                  Vec3D.Vec3D(12, 12, 8),
                  Vec3D.Vec3D(10, 15, 8),
                  Vec3D.Vec3D(10, 12, 13)]
        spline = SplineC1(3, [2, 1])

        for count in range(0, 6):
            spline.append_deBoor_point(points[count])

        spline.draw()

        control_points = spline.splineC0.control_points
        control_points.pop()
        spline.splineC0.control_points = control_points

        with self.assertRaises(InvalidData):
            spline.splineC0.draw()

    def test_calculate_control_points_in_pop_points_from_partial_curve(self):
        spline = SplineC1(3, [1, 3, 3])
        points = []

        for index in range(0, 8):
            points.append(Vec3D.Vec3D(index, index + 1, index + 2))

        for index in range(0, 8):
            spline.append_deBoor_point(points[index])

        spline.draw()

        for index in range(0, 4):
            spline.splineC0.partial_curves[2].pop_last_point()

        self.assertEqual(spline.splineC0.partial_curves[2].control_points, [])

    def test_calculate_partial_curve_derivative(self):
        spline = SplineC1(3, [1, 3, 3])
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(2, 8, 6),
                  Vec3D.Vec3D(3, 5, 4),
                  Vec3D.Vec3D(4, 4, 5)]

        for index in range(0, 8):
            spline.append_deBoor_point(Vec3D.Vec3D(index, index, index))

        spline.draw()

        splineC0 = spline.splineC0
        for index in range(0, 4):
            splineC0.partial_curves[2].control_points[index] = points[index]

        splineC0.partial_curves[2].draw_derivative(2)
        self.assertEqual(splineC0.partial_curves[2].derivative[2][0],
                         Vec3D.Vec3D(-1, -11, -8))
        self.assertEqual(splineC0.partial_curves[2].derivative[2][
            splineC0.partial_curves[2].RANGE_STEP], Vec3D.Vec3D(0, 2, 3))

    def test_calculate_partial_curves_subdivision(self):
        spline = SplineC1(2, [1, 3, 3])
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(0, 1, 1),
                  Vec3D.Vec3D(0, 2, 3)]
        result_points = [Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 1, 1),
                         Vec3D.Vec3D(0, 2, 3)]

        splineC0 = spline.splineC0

        for index in range(0, 3):
            splineC0.partial_curves[2].append_point(points[index])

        subdivision = splineC0.partial_curves[2].subdivision(
            0, splineC0.partial_curves[2].control_points)

        curve_points = splineC0.partial_curves[2].draw()
        for index in range(0, 6):
            self.assertEqual(subdivision[index], result_points[index])

    def test_calculate_partial_curves_degree_elevation(self):
        spline = SplineC1(2, [1, 3, 3])
        points = [Vec3D.Vec3D(0, 0, 0),
                  Vec3D.Vec3D(0, 1, 1),
                  Vec3D.Vec3D(0, 2, 3)]
        result_points = [Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 0, 0),
                         Vec3D.Vec3D(0, 1, 1),
                         Vec3D.Vec3D(0, 2, 3)]

        splineC0 = spline.splineC0

        for index in range(0, 3):
            splineC0.partial_curves[2].append_point(points[index])

        elevation = splineC0.partial_curves[2].degree_elevation()

        self.assertEqual(elevation[1], Vec3D.Vec3D(0, 2 / 3, 2 / 3))
        self.assertEqual(len(elevation), 4)

    def test_calculate_raises_indexerror_when_drawing_partial_curves(self):
        spline = SplineC1(3, [1, 3, 3])
        points = []

        splineC0 = spline.splineC0

        for index in range(0, 10):
            points.append(Vec3D.Vec3D(index, index + 1, index + 2))

        for index in range(0, 10):
            splineC0.append_point(points[index])

        with self.assertRaises(IndexError):
            splineC0.partial_curves[2].draw_derivative(4)


if __name__ == '__main__':
    unittest.main()
