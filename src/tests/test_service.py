import unittest
from fastapi.testclient import TestClient
from typing import Dict
from main import compare_data, app

client = TestClient(app)

class TestCompareData(unittest.TestCase):
    def test_compare_data_empty_input(self):
        """
        This test case checks the behavior of the compare_data function when both extracted_data and stored_data are empty dictionaries.

        Parameters:
        - extracted_data (dict): An empty dictionary representing the extracted data.
        - stored_data (dict): An empty dictionary representing the stored data.
        - expected_summary (dict): An empty dictionary representing the expected summary.

        Returns:
        - summary (dict): An empty dictionary representing the actual summary returned by the compare_data function.

        Raises:
        - AssertionError: If the actual summary does not match the expected summary.
        """
        extracted_data: Dict = {}
        stored_data: Dict = {}
        expected_summary: Dict = {}

        summary = compare_data(extracted_data, stored_data)
        self.assertEqual(summary, expected_summary)

    def test_compare_data_different_keys(self):
        """
        This test case checks the behavior of the compare_data function when the keys in the extracted_data and stored_data dictionaries are different.

        Parameters:
        - extracted_data (dict): A dictionary representing the extracted data. It is expected to have at least one key.
        - stored_data (dict): A dictionary representing the stored data. It is expected to have at least one key.
        - expected_summary (dict): A dictionary representing the expected summary. It is expected to have keys corresponding to the keys in extracted_data and stored_data.

        Returns:
        - summary (dict): A dictionary representing the actual summary returned by the compare_data function. It is expected to have keys corresponding to the keys in extracted_data and stored_data.

        Raises:
        - AssertionError: If the actual summary does not match the expected summary.

        Usage:
        ```python
        extracted_data = {"key1": "value1"}
        stored_data = {"key2": "value2"}
        expected_summary = {
            "key1": {"extracted": "value1", "stored": None, "match": False},
            "key2": {"extracted": None, "stored": "value2", "match": False}
        }

        summary = compare_data(extracted_data, stored_data)
        self.assertEqual(summary, expected_summary)
        ```
        """
        extracted_data: Dict = {"key1": "value1"}
        stored_data: Dict = {"key2": "value2"}
        expected_summary: Dict = {
            "key1": {"extracted": "value1", "stored": None, "match": False},
            "key2": {"extracted": None, "stored": "value2", "match": False}
        }

        summary = compare_data(extracted_data, stored_data)
        self.assertEqual(summary, expected_summary)

    def test_compare_data_same_keys_different_values(self):
        extracted_data: Dict = {"key1": "value1"}
        stored_data: Dict = {"key1": "value2"}
        expected_summary: Dict = {
            "key1": {"extracted": "value1", "stored": "value2", "match": False}
        }

        summary = compare_data(extracted_data, stored_data)
        self.assertEqual(summary, expected_summary)

    def test_compare_data_same_keys_same_values(self):
        extracted_data: Dict = {"key1": "value1"}
        stored_data: Dict = {"key1": "value1"}
        expected_summary: Dict = {
            "key1": {"extracted": "value1", "stored": "value1", "match": True}
        }

        summary = compare_data(extracted_data, stored_data)
        self.assertEqual(summary, expected_summary)

    def test_compare_data_same_keys_different_types(self):
        extracted_data: Dict = {"key1": 123}
        stored_data: Dict = {"key1": "123"}
        expected_summary: Dict = {
            "key1": {"extracted": 123, "stored": "123", "match": False}
        }

        summary = compare_data(extracted_data, stored_data)
        self.assertEqual(summary, expected_summary)

if __name__ == '__main__':
    unittest.main()
