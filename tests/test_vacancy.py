import unittest

from src.vacancy import Vacancy


class TestVacancy(unittest.TestCase):
    def setUp(self):
        self.vacancy1 = Vacancy(
            "Python Developer",
            "https://hh.ru/vacancy/1",
            100000,
            150000,
            "RUR",
            "Develop Python apps",
            "Python 3+",
            "Company A",
        )
        self.vacancy2 = Vacancy(
            "Java Developer",
            "https://hh.ru/vacancy/2",
            120000,
            180000,
            "RUR",
            "Develop Java apps",
            "Java 8+",
            "Company B",
        )
        self.vacancy_no_salary = Vacancy(
            "Developer",
            "https://hh.ru/vacancy/3",
            None,
            None,
            "RUR",
            "Develop apps",
            "Experience",
            "Company C",
        )

    def test_vacancy_creation(self):
        self.assertEqual(self.vacancy1.title, "Python Developer")
        self.assertEqual(self.vacancy1.salary_from, 100000)
        self.assertEqual(self.vacancy1.salary_to, 150000)

    def test_salary_display(self):
        self.assertIn("100 000", self.vacancy1.get_salary_display())
        self.assertEqual(
            self.vacancy_no_salary.get_salary_display(), "Зарплата не указана"
        )

    def test_comparison(self):
        self.assertTrue(self.vacancy1 < self.vacancy2)
        self.assertTrue(self.vacancy2 > self.vacancy1)

    def test_to_dict_from_dict(self):
        vacancy_dict = self.vacancy1.to_dict()
        new_vacancy = Vacancy.from_dict(vacancy_dict)

        self.assertEqual(self.vacancy1.title, new_vacancy.title)
        self.assertEqual(self.vacancy1.salary_from, new_vacancy.salary_from)
