import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional

from .vacancy import Vacancy


class Storage(ABC):
    """Абстрактный класс для работы с хранилищем данных"""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавить вакансию в хранилище"""
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Vacancy]:
        """Получить вакансии по критериям"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удалить вакансию из хранилища"""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Очистить хранилище"""
        pass


class JSONSaver(Storage):
    """Класс для работы с JSON-файлом"""

    def __init__(self, filename: str = "vacancies.json"):
        self._filename = filename
        self._ensure_data_directory()

    def _ensure_data_directory(self) -> None:
        """Убедиться, что директория data существует"""
        Path("data").mkdir(exist_ok=True)
        self._filepath = Path("data") / self._filename

    def _read_vacancies(self) -> List[Dict[str, Any]]:
        """Прочитать вакансии из файла"""
        if not self._filepath.exists():
            return []

        try:
            with open(self._filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_vacancies(self, vacancies: List[Dict[str, Any]]) -> None:
        """Записать вакансии в файл"""
        with open(self._filepath, "w", encoding="utf-8") as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=2)

    @staticmethod
    def _vacancy_exists(vacancy: Vacancy, vacancies_data: List[Dict[str, Any]]) -> bool:
        """Проверить, существует ли вакансия (статический метод)"""
        vacancy_dict = vacancy.to_dict()
        for existing_vacancy in vacancies_data:
            if (
                existing_vacancy["title"] == vacancy_dict["title"]
                and existing_vacancy["url"] == vacancy_dict["url"]
            ):
                return True
        return False

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавить вакансию в файл"""
        vacancies_data = self._read_vacancies()
        vacancy_dict = vacancy.to_dict()

        # Проверка на дубликаты
        if not self._vacancy_exists(vacancy, vacancies_data):
            vacancies_data.append(vacancy_dict)
            self._write_vacancies(vacancies_data)

    def add_vacancies(self, vacancies: List[Vacancy]) -> None:
        """Добавить несколько вакансий"""
        for vacancy in vacancies:
            self.add_vacancy(vacancy)

    def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Vacancy]:
        """Получить вакансии по критериям"""
        vacancies_data = self._read_vacancies()
        vacancies = [Vacancy.from_dict(data) for data in vacancies_data]

        if not criteria:
            return vacancies

        filtered_vacancies = []
        for vacancy in vacancies:
            match = True
            for key, value in criteria.items():
                if hasattr(vacancy, key):
                    attr_value = getattr(vacancy, key)
                    # Поиск подстроки в строковых полях
                    if isinstance(attr_value, str) and isinstance(value, str):
                        if value.lower() not in attr_value.lower():
                            match = False
                            break
                    # Точное сравнение для числовых полей
                    elif attr_value != value:
                        match = False
                        break
                else:
                    match = False
                    break
            if match:
                filtered_vacancies.append(vacancy)

        return filtered_vacancies

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удалить вакансию из файла"""
        vacancies_data = self._read_vacancies()
        vacancy_dict = vacancy.to_dict()

        # Удаляем вакансию
        vacancies_data = [
            v
            for v in vacancies_data
            if not (
                v["title"] == vacancy_dict["title"] and v["url"] == vacancy_dict["url"]
            )
        ]

        self._write_vacancies(vacancies_data)

    def clear(self) -> None:
        """Очистить файл"""
        self._write_vacancies([])
