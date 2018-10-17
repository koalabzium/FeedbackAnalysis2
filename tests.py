# PRZETESTUJ:
# - czy json i csv otwierają to samo

import unittest
from feedback_analysis import Feedback
from create_data import generate_random_data, serialize_tojson, serialize_tocsv
from os import remove


class TestReadingFile(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        data = generate_random_data(10)
        serialize_tocsv(data, 'test_file.csv')
        serialize_tojson(data, 'test_file.json')

    @classmethod
    def tearDownClass(cls):
        remove('test_file.csv')
        remove('test_file.json')

    def test_file_format(self):
        file_path = 'test_file'
        self.assertRaises(ValueError, Feedback, file_path)

    def test_same_read_format(self):
        f1 = Feedback('test_file.json')
        f2 = Feedback('test_file.csv')
        self.assertEqual(f1.feedback, f2.feedback)


class TestAnalysisWithNormalData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        d = dict(message=["These", "are", "some", "messages"],
                 airline_code=[8, 2, 2, 8],
                 number_of_fellow_passengers=[2, 1, 1, 0],
                 did_receive_compensation=[False, True, True, False],
                 total_compensation_amount=[0, 2000, 500, 0])
        serialize_tojson(d, 'test_file.json')
        cls.f = Feedback('test_file.json')

    @classmethod
    def tearDownClass(cls):
        remove('test_file.json')

    def test_calculate_average_compensation_per_passenger(self):
        result = self.f.calculate_average_compensation_per_passenger()
        self.assertEqual(625, result)

    def test_most_popular_airline(self):
        result = self.f.find_most_popular_airline()
        self.assertEqual({2, 8}, result)

    def test_calculate_got_compensation_percentage(self):
        result = self.f.calculate_got_compensation_percentage()
        self.assertEqual(50, result)

    def test_extract_messages(self):
        result = self.f.extract_messages()
        self.assertEqual(self.f.feedback["message"], result)

    def test_distribution_fellow_passengers(self):
        result1 = self.f.distribution_fellow_passengers()
        result2 = [(0, 1), (1, 2), (2, 1)]
        self.assertEqual(result1, result2)


class TestAnalysisWithEmptyDictionary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        d = dict(message=[],
                 airline_code=[],
                 number_of_fellow_passengers=[],
                 did_receive_compensation=[],
                 total_compensation_amount=[])
        serialize_tojson(d, 'test_file.json')
        cls.f = Feedback('test_file.json')

    @classmethod
    def tearDownClass(cls):
        remove('test_file.json')

    def test_calculate_average_compensation_per_passenger(self):
        with self.assertRaises(ZeroDivisionError):
            self.f.calculate_average_compensation_per_passenger()

    def test_most_popular_airline(self):
        with self.assertRaises(ValueError):
            self.f.find_most_popular_airline()

    def test_calculate_got_compensation_percentage(self):
        with self.assertRaises(ZeroDivisionError):
            self.f.calculate_got_compensation_percentage()

    def test_extract_messages(self):
        result = self.f.extract_messages()
        self.assertEqual([], result)

    def test_distribution_fellow_passengers(self):
        result = self.f.distribution_fellow_passengers()
        self.assertEqual([], result)


if __name__ == '__main__':
    unittest.main()
