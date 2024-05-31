import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    @patch('main.pdf_service.extract', return_value={})
    @patch('main.get_stored_data', return_value={"key": "value"})
    def test_empty_extracted_data(self, mock_extract, mock_get_stored_data):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json(), dict))
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()["summary"], {})

    @patch('main.pdf_service.extract', return_value={"key": "value"})
    @patch('main.get_stored_data', return_value={})
    def test_empty_stored_data(self, mock_extract, mock_get_stored_data):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json(), dict))
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()["summary"], {})

    @patch('main.pdf_service.extract', return_value={})
    @patch('main.get_stored_data', return_value={})
    def test_empty_extracted_and_stored_data(self, mock_extract, mock_get_stored_data):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json(), dict))
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()["summary"], {})

    @patch('main.pdf_service.extract', return_value={"key": "value"})
    @patch('main.get_stored_data', return_value={"key": "value"})
    def test_non_empty_extracted_and_stored_data(self, mock_extract, mock_get_stored_data):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json(), dict))
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()["summary"], {"key": {"extracted": "value", "stored": "value", "match": True}})

    @patch('main.pdf_service.extract', side_effect=FileNotFoundError("Invalid file provided."))
    def test_invalid_file_provided(self, mock_extract):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 400)
        self.assertTrue(isinstance(response.json(), dict))
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()["detail"], "Cannot extract data. Invalid file provided.")


if __name__ == '__main__':
    unittest.main()
