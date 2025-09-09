import unittest
from unittest.mock import Mock, patch

from src.api import HeadHunterAPI


class TestHeadHunterAPI(unittest.TestCase):
    def setUp(self):
        self.api = HeadHunterAPI()

    @patch("src.api.requests.get")
    def test_get_vacancies_success(self, mock_get):
        # Мокируем успешный ответ
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "name": "Python Developer",
                    "alternate_url": "https://hh.ru/vacancy/123",
                    "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                    "description": "Test description",
                    "snippet": {"requirement": "Python experience"},
                    "employer": {"name": "Test Company"},
                }
            ]
        }
        mock_get.return_value = mock_response

        vacancies = self.api.get_vacancies("Python")

        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0]["name"], "Python Developer")

    @patch("src.api.requests.get")
    def test_get_vacancies_error_status(self, mock_get):
        # Мокируем ответ с ошибкой
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(ConnectionError):
            self.api.get_vacancies("Python")

    @patch("src.api.requests.get")
    def test_get_vacancies_empty(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        vacancies = self.api.get_vacancies("NonexistentQuery")

        self.assertEqual(len(vacancies), 0)
