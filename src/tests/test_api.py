import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
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



class TestUploadPdf(unittest.IsolatedAsyncioTestCase):
    @patch('main.os.remove')
    async def test_upload_pdf_cleans_up_saved_file(self, mock_remove):
        client = TestClient(app)

        # Mock the pdf_service.extract method to return a sample extracted_data
        pdf_service_extract_mock = Mock(return_value={'key1': 'value1', 'key2': 'value2'})
        with patch('main.pdf_service.extract', pdf_service_extract_mock):
            # Mock the get_stored_data method to return a sample stored_data
            get_stored_data_mock = Mock(return_value={'key1': 'stored_value1', 'key2': 'stored_value2'})
            with patch('main.get_stored_data', get_stored_data_mock):
                # Mock the compare_data method to return a sample summary
                compare_data_mock = Mock(return_value={
                    'key1': {'extracted': 'value1', 'stored': 'stored_value1', 'match': True},
                    'key2': {'extracted': 'value2', 'stored': 'stored_value2', 'match': True}
                })
                with patch('main.compare_data', compare_data_mock):
                    # Mock the csv_to_dict method to return a sample stored_data
                    csv_to_dict_mock = Mock(return_value={'HealthInc': {'key1': 'stored_value1', 'key2': 'stored_value2'}})
                    with patch('main.csv_to_dict', csv_to_dict_mock):
                        # Call the function under test
                        response = client.post(
                            "/upload/",
                            data={"company_name": "HealthInc"},
                            files={"file": ("test.pdf", b"test content")}
                        )

                        # Assert the status code and response
                        self.assertEqual(response.status_code, 200)
                        self.assertTrue("summary" in response.json())

                        # Assert that the saved file is removed after processing
                        mock_remove.assert_called_once_with("assets/test.pdf")


if __name__ == '__main__':
    unittest.main()
