import unittest
from unittest.mock import patch, MagicMock
from main import get_stored_data, csv_to_dict

class TestGetStoredData(unittest.TestCase):

    def setUp(self):
        self.file_path = 'data/database.csv'
        self.mock_csv_to_dict = patch('main.csv_to_dict').start()
        self.mock_csv_to_dict.return_value = {'Company1': {'Revenue': 100000, 'Profit': 20000}}
        self.addCleanup(patch.stopall)

    def test_get_stored_data_valid_company(self):
        result = get_stored_data('Company1')
        self.assertEqual(result, {'Revenue': 100000, 'Profit': 20000})

    def test_get_stored_data_invalid_company(self):
        result = get_stored_data('InvalidCompany')
        self.assertIsNone(result)

    def test_get_stored_data_csv_to_dict_failure(self):
        self.mock_csv_to_dict.return_value = None
        with self.assertRaises(Exception):
            get_stored_data('Company1')

    # def test_get_stored_data_cache_hit(self):
    #     get_stored_data('Company1')  # First call to populate cache
    #     result = get_stored_data('Company1')  # Second call should hit the cache
    #     self.assertEqual(result, {'Revenue': 100000, 'Profit': 20000})
    #     self.mock_csv_to_dict.assert_called_once_with(self.file_path)


if __name__ == '__main__':
    unittest.main()
