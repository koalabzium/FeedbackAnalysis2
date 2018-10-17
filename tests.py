import unittest
import feedback_analysis as fa


class TestReadingFile(unittest.TestCase):

    def test_read_file(self):
        file_path = 'test_file'
        self.assertRaises(ValueError, fa.Feedback, file_path)



if __name__ == '__main__':
    unittest.main()
