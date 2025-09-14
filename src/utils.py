from typing import List

from .vacancy import Vacancy


def filter_vacancies(
    vacancies: List[Vacancy], filter_words: List[str]
) -> List[Vacancy]:
    """Фильтровать вакансии по ключевым словам"""
    if not filter_words:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        vacancy_text = (
            f"{vacancy.title} {vacancy.description} {vacancy.requirements}".lower()
        )
        if any(word.lower() in vacancy_text for word in filter_words):
            filtered.append(vacancy)

    return filtered


def get_vacancies_by_salary(
    vacancies: List[Vacancy], salary_range: str
) -> List[Vacancy]:
    """Получить вакансии по диапазону зарплат"""
    if not salary_range or salary_range.strip() == "":
        return vacancies

    try:
        # Обработка формата "100000-150000" или "100000 - 150000"
        if "-" in salary_range:
            parts = salary_range.replace(" ", "").split("-")
            min_salary = int(parts[0])
            max_salary = int(parts[1]) if len(parts) > 1 else float("inf")
        else:
            min_salary = int(salary_range)
            max_salary = float("inf")

        filtered = []
        for vacancy in vacancies:
            # Используем salary_from для сравнения
            vacancy_salary = vacancy.salary_from
            if min_salary <= vacancy_salary <= max_salary:
                filtered.append(vacancy)

        return filtered
    except ValueError:
        # При ошибке парсинга возвращаем все вакансии
        return vacancies


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Отсортировать вакансии по зарплате (по убыванию)"""
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """Получить топ N вакансий"""
    return vacancies[:top_n]


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """Вывести вакансии в читаемом формате"""
    if not vacancies:
        print("Вакансии не найдены.")
        return

    for i, vacancy in enumerate(vacancies, 1):
        print(f"\n{'=' * 50}")
        print(f"ВАКАНСИЯ #{i}")
        print(f"{'=' * 50}")
        print(vacancy)
