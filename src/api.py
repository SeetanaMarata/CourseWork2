from abc import ABC, abstractmethod
from typing import Any, Dict, List

import requests


class API(ABC):
    """Абстрактный класс для работы с API сервиса с вакансиями"""

    @abstractmethod
    def get_vacancies(
        self, search_query: str, per_page: int = 100
    ) -> List[Dict[str, Any]]:
        """Получить вакансии по поисковому запросу"""
        pass


class HeadHunterAPI(API):
    """Класс для работы с API hh.ru"""

    def __init__(self):
        self._base_url = "https://api.hh.ru/vacancies"

    def __connect_to_api(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Приватный метод для подключения к API"""
        try:
            response = requests.get(self._base_url, params=params)
            # Добавляем проверку статус-кода
            if response.status_code != 200:
                raise ConnectionError(
                    f"Ошибка подключения к API hh.ru. Статус код: {response.status_code}"
                )
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Ошибка подключения к API hh.ru: {e}")

    def get_vacancies(
        self, search_query: str, per_page: int = 100
    ) -> List[Dict[str, Any]]:
        """Получить вакансии с hh.ru по поисковому запросу"""
        params = {
            "text": search_query,
            "per_page": per_page,
            "area": 113,  # Россия
            "only_with_salary": True,
        }

        data = self.__connect_to_api(params)
        return data.get("items", [])
