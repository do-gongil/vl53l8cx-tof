"""parse_frame 단위 테스트.  실행: python -m unittest discover -s tools"""
import math
import pathlib
import unittest

from tof_viewer import GRID, parse_frame


def line(values):
    return "F," + ",".join(str(v) for v in values)


class ParseFrameTest(unittest.TestCase):
    def test_valid_frame(self):
        values = list(range(GRID * GRID))
        values[10] = -1
        frame = parse_frame(line(values))
        self.assertEqual(frame.shape, (GRID, GRID))
        self.assertEqual(frame[0, 1], 1)
        self.assertEqual(frame[7, 7], 63)        # 인덱스 = y*8 + x
        self.assertTrue(math.isnan(frame[1, 2]))  # -1 → 무효 셀

    def test_wrong_count(self):
        self.assertIsNone(parse_frame(line(range(GRID * GRID - 1))))
        self.assertIsNone(parse_frame(line(range(GRID * GRID + 1))))

    def test_non_numeric(self):
        values = [str(v) for v in range(GRID * GRID)]
        values[5] = "abc"
        self.assertIsNone(parse_frame(line(values)))

    def test_status_line(self):
        self.assertIsNone(parse_frame("# VL53L8CX start"))

    def test_sample_file(self):
        lines = (pathlib.Path(__file__).parent / "sample_frames.txt").read_text().splitlines()
        frames = [parse_frame(l) for l in lines if l.startswith("F,")]
        self.assertTrue(frames)
        self.assertTrue(all(f is not None for f in frames))


if __name__ == "__main__":
    unittest.main()
