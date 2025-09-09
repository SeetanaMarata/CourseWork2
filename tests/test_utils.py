import unittest
from unittest.mock import patch

from src.utils import (filter_vacancies, get_top_vacancies,
                       get_vacancies_by_salary, print_vacancies,
                       sort_vacancies)
from src.vacancy import Vacancy


class TestUtils(unittest.TestCase):
    def setUp(self):
        # Создаем тестовые вакансии
        self.vacancy1 = Vacancy(
            "Python Developer",
            "https://hh.ru/vacancy/1",
            100000,
            150000,
            "RUR",
            "Develop Python apps",
            "Python 3+ experience required",
            "Company A",
        )
        self.vacancy2 = Vacancy(
            "Java Developer",
            "https://hh.ru/vacancy/2",
            80000,
            120000,
            "RUR",
            "Develop Java applications",
            "Java Spring framework",
            "Company B",
        )
        self.vacancy3 = Vacancy(
            "Senior Python Developer",
            "https://hh.ru/vacancy/3",
            150000,
            200000,
            "RUR",
            "Senior Python development",
            "Python Django Flask",
            "Company C",
        )
        self.vacancies = [self.vacancy1, self.vacancy2, self.vacancy3]

    def test_filter_vacancies_with_keywords(self):
        # Фильтрация по ключевым словам
        filtered = filter_vacancies(self.vacancies, ["Python"])
        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0].title, "Python Developer")
        self.assertEqual(filtered[1].title, "Senior Python Developer")

    def test_filter_vacancies_empty_keywords(self):
        # Фильтрация без ключевых слов
        filtered = filter_vacancies(self.vacancies, [])
        self.assertEqual(len(filtered), 3)

    def test_filter_vacancies_no_matches(self):
        # Фильтрация с ключевыми словами, которых нет
        filtered = filter_vacancies(self.vacancies, ["JavaScript"])
        self.assertEqual(len(filtered), 0)

    def test_get_vacancies_by_salary_range(self):
        # Фильтрация по диапазону зарплат
        filtered = get_vacancies_by_salary(self.vacancies, "90000-160000")
        self.assertEqual(len(filtered), 2)

    def test_get_vacancies_by_salary_min(self):
        # Фильтрация по минимальной зарплате
        filtered = get_vacancies_by_salary(self.vacancies, "120000")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].title, "Senior Python Developer")

    def test_get_vacancies_by_salary_empty_range(self):
        # Фильтрация с пустым диапазоном
        filtered = get_vacancies_by_salary(self.vacancies, "")
        self.assertEqual(len(filtered), 3)

    def test_get_vacancies_by_salary_invalid_range(self):
        # Фильтрация с неверным форматом
        filtered = get_vacancies_by_salary(self.vacancies, "invalid")
        self.assertEqual(len(filtered), 3)  # Должен вернуть все вакансии при ошибке

    def test_sort_vacancies(self):
        # Сортировка вакансий
        sorted_vacancies = sort_vacancies(self.vacancies)
        self.assertEqual(sorted_vacancies[0].title, "Senior Python Developer")
        self.assertEqual(sorted_vacancies[1].title, "Python Developer")
        self.assertEqual(sorted_vacancies[2].title, "Java Developer")

    def test_get_top_vacancies(self):
        # Получение топ N вакансий - сначала нужно отсортировать!
        sorted_vacancies = sort_vacancies(self.vacancies)
        top_vacancies = get_top_vacancies(sorted_vacancies, 2)
        self.assertEqual(len(top_vacancies), 2)
        self.assertEqual(top_vacancies[0].title, "Senior Python Developer")
        self.assertEqual(top_vacancies[1].title, "Python Developer")

    def test_get_top_vacancies_more_than_available(self):
        # Получение большего количества, чем есть
        top_vacancies = get_top_vacancies(self.vacancies, 5)
        self.assertEqual(len(top_vacancies), 3)

    def test_get_top_vacancies_zero(self):
        # Получение 0 вакансий
        top_vacancies = get_top_vacancies(self.vacancies, 0)
        self.assertEqual(len(top_vacancies), 0)

    def test_print_vacancies_with_data(self):
        # Тест вывода вакансий с данными
        with patch("builtins.print") as mock_print:
            print_vacancies(self.vacancies)
            self.assertTrue(mock_print.called)

    def test_print_vacancies_empty(self):
        # Тест вывода пустого списка вакансий
        with patch("builtins.print") as mock_print:
            print_vacancies([])
            # Проверяем, что была вызвана печать сообщения о пустом списке
            mock_print.assert_called_with("Вакансии не найдены.")


if __name__ == "__main__":
    unittest.main()
