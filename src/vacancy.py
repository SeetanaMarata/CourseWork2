from __future__ import annotations

from typing import Any, Dict, List


class Vacancy:
    """Класс для работы с вакансиями"""

    __slots__ = (
        "_title",
        "_url",
        "_salary_from",
        "_salary_to",
        "_currency",
        "_description",
        "_requirements",
        "_employer",
    )

    def __init__(
        self,
        title: str,
        url: str,
        salary_from: int | None,
        salary_to: int | None,
        currency: str,
        description: str,
        requirements: str,
        employer: str,
    ):
        self._title = self._validate_title(title)
        self._url = self._validate_url(url)
        self._salary_from = self._validate_salary(salary_from)
        self._salary_to = self._validate_salary(salary_to)
        self._currency = self._validate_currency(currency)
        self._description = self._validate_text(description)
        self._requirements = self._validate_text(requirements)
        self._employer = self._validate_text(employer)

    @staticmethod
    def _validate_title(title: str) -> str:
        """Валидация названия вакансии (статический метод)"""
        if not title or not isinstance(title, str):
            return "Название не указано"
        return title.strip()

    @staticmethod
    def _validate_url(url: str) -> str:
        """Валидация URL (статический метод)"""
        if not url or not isinstance(url, str):
            return "URL не указан"
        return url.strip()

    @staticmethod
    def _validate_salary(salary: int | None) -> int:
        """Валидация зарплаты (статический метод)"""
        if salary is None or not isinstance(salary, (int, float)):
            return 0
        return max(0, int(salary))

    @staticmethod
    def _validate_currency(currency: str) -> str:
        """Валидация валюты (статический метод)"""
        if not currency or not isinstance(currency, str):
            return "RUR"
        return currency.upper().strip()

    @staticmethod
    def _validate_text(text: str) -> str:
        """Валидация текста (статический метод)"""
        if not text or not isinstance(text, str):
            return "Не указано"
        return text.strip()

    @property
    def title(self) -> str:
        return self._title

    @property
    def url(self) -> str:
        return self._url

    @property
    def salary_from(self) -> int:
        return self._salary_from

    @property
    def salary_to(self) -> int:
        return self._salary_to

    @property
    def currency(self) -> str:
        return self._currency

    @property
    def description(self) -> str:
        return self._description

    @property
    def requirements(self) -> str:
        return self._requirements

    @property
    def employer(self) -> str:
        return self._employer

    def get_salary_display(self) -> str:
        """Получить отформатированную строку зарплаты"""
        if self._salary_from == 0 and self._salary_to == 0:
            return "Зарплата не указана"

        if self._salary_from == self._salary_to:
            return f"{self._salary_from:,} {self._currency}".replace(",", " ")

        if self._salary_from > 0 and self._salary_to > 0:
            return (
                f"{self._salary_from:,} - {self._salary_to:,} {self._currency}".replace(
                    ",", " "
                )
            )

        if self._salary_from > 0:
            return f"от {self._salary_from:,} {self._currency}".replace(",", " ")

        return f"до {self._salary_to:,} {self._currency}".replace(",", " ")

    def __str__(self) -> str:
        return (
            f"{self._title}\n"
            f"Компания: {self._employer}\n"
            f"Зарплата: {self.get_salary_display()}\n"
            f"Требования: {self._requirements[:100]}...\n"
            f"Ссылка: {self._url}\n"
        )

    def __repr__(self) -> str:
        return f"Vacancy('{self._title}', '{self._url}')"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return (
            self._title == other._title
            and self._url == other._url
            and self._salary_from == other._salary_from
            and self._salary_to == other._salary_to
        )

    def __lt__(self, other: Vacancy) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        # Сравниваем по минимальной зарплате
        self_avg = self._salary_from if self._salary_from > 0 else self._salary_to
        other_avg = other._salary_from if other._salary_from > 0 else other._salary_to
        return self_avg < other_avg

    def __le__(self, other: Vacancy) -> bool:
        return self < other or self == other

    def __gt__(self, other: Vacancy) -> bool:
        return not self <= other

    def __ge__(self, other: Vacancy) -> bool:
        return not self < other

    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать вакансию в словарь"""
        return {
            "title": self._title,
            "url": self._url,
            "salary_from": self._salary_from,
            "salary_to": self._salary_to,
            "currency": self._currency,
            "description": self._description,
            "requirements": self._requirements,
            "employer": self._employer,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Vacancy:
        """Создать вакансию из словаря"""
        return cls(
            title=data.get("title", ""),
            url=data.get("url", ""),
            salary_from=data.get("salary_from", 0),
            salary_to=data.get("salary_to", 0),
            currency=data.get("currency", "RUR"),
            description=data.get("description", ""),
            requirements=data.get("requirements", ""),
            employer=data.get("employer", ""),
        )

    @classmethod
    def cast_to_object_list(cls, vacancies_data: List[Dict[str, Any]]) -> List[Vacancy]:
        """Преобразовать список словарей в список объектов Vacancy"""
        vacancies = []
        for vacancy_data in vacancies_data:
            try:
                # Парсинг данных из API hh.ru
                salary = vacancy_data.get("salary")
                salary_from = salary.get("from") if salary else None
                salary_to = salary.get("to") if salary else None
                currency = salary.get("currency") if salary else "RUR"

                vacancy = cls(
                    title=vacancy_data.get("name", ""),
                    url=vacancy_data.get("alternate_url", ""),
                    salary_from=salary_from,
                    salary_to=salary_to,
                    currency=currency,
                    description=vacancy_data.get("description", ""),
                    requirements=vacancy_data.get("snippet", {}).get("requirement", ""),
                    employer=vacancy_data.get("employer", {}).get("name", ""),
                )
                vacancies.append(vacancy)
            except (KeyError, TypeError, AttributeError) as e:
                print(f"Ошибка при создании вакансии: {e}")
                continue

        return vacancies
