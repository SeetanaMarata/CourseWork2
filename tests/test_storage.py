import unittest
from pathlib import Path

from src.storage import JSONSaver
from src.vacancy import Vacancy


class TestJSONSaver(unittest.TestCase):
    def setUp(self):
        self.filename = "test_vacancies.json"
        self.saver = JSONSaver(self.filename)
        self.vacancy = Vacancy(
            "Test Developer",
            "https://hh.ru/vacancy/test",
            100000,
            150000,
            "RUR",
            "Test description",
            "Test requirements",
            "Test Company",
        )

    def tearDown(self):
        # Очистка тестового файла
        test_file = Path("data") / self.filename
        if test_file.exists():
            test_file.unlink()

    def test_add_and_get_vacancy(self):
        self.saver.add_vacancy(self.vacancy)
        vacancies = self.saver.get_vacancies()

        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0].title, "Test Developer")

    def test_duplicate_vacancy(self):
        self.saver.add_vacancy(self.vacancy)
        self.saver.add_vacancy(self.vacancy)  # Дубликат

        vacancies = self.saver.get_vacancies()
        self.assertEqual(len(vacancies), 1)  # Дубликат не добавлен

    def test_delete_vacancy(self):
        self.saver.add_vacancy(self.vacancy)
        self.saver.delete_vacancy(self.vacancy)

        vacancies = self.saver.get_vacancies()
        self.assertEqual(len(vacancies), 0)

    def test_filter_vacancies(self):
        self.saver.add_vacancy(self.vacancy)
        # Используем точное совпадение вместо подстроки
        vacancies = self.saver.get_vacancies({"title": "Test Developer"})

        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0].title, "Test Developer")
