from src.api import HeadHunterAPI
from src.storage import JSONSaver
from src.utils import (
    filter_vacancies,
    get_top_vacancies,
    get_vacancies_by_salary,
    print_vacancies,
    sort_vacancies,
)
from src.vacancy import Vacancy


def user_interaction():
    """Функция для взаимодействия с пользователем"""
    print("Добро пожаловать в программу поиска вакансий!")
    print("=" * 50)

    # Инициализация компонентов
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()

    # Получение данных от пользователя
    search_query = input(
        "Введите поисковый запрос (например: Python разработчик): "
    ).strip()

    if not search_query:
        print("Поисковый запрос не может быть пустым!")
        return

    try:
        # Получение вакансий с hh.ru
        print("Получаем вакансии с hh.ru...")
        hh_vacancies_data = hh_api.get_vacancies(search_query, per_page=50)
        vacancies_list = Vacancy.cast_to_object_list(hh_vacancies_data)

        if not vacancies_list:
            print("По вашему запросу вакансий не найдено.")
            return

        # Сохранение в файл
        json_saver.add_vacancies(vacancies_list)
        print(f"Найдено и сохранено {len(vacancies_list)} вакансий.")

        # Дополнительные критерии
        try:
            top_n = int(
                input("Введите количество вакансий для вывода в топ N: ").strip()
                or "10"
            )
        except ValueError:
            top_n = 10

        filter_words_input = input(
            "Введите ключевые слова для фильтрации вакансий (через пробел): "
        ).strip()
        filter_words = filter_words_input.split() if filter_words_input else []

        salary_range = input(
            "Введите диапазон зарплат (например: 100000-150000): "
        ).strip()

        # Фильтрация и сортировка
        filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
        ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
        sorted_vacancies = sort_vacancies(ranged_vacancies)
        top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

        # Вывод результатов
        print(f"\nРезультаты поиска ({len(top_vacancies)} вакансий):")
        print_vacancies(top_vacancies)

        # Дополнительные опции
        while True:
            print("\nДополнительные опции:")
            print("1 - Сохранить результаты в файл")
            print("2 - Очистить файл с вакансиями")
            print("3 - Показать все сохраненные вакансии")
            print("0 - Выход")

            choice = input("Выберите опцию: ").strip()

            if choice == "1":
                # Сохранение отфильтрованных результатов
                temp_saver = JSONSaver("filtered_vacancies.json")
                temp_saver.add_vacancies(top_vacancies)
                print("Результаты сохранены в файл 'filtered_vacancies.json'")

            elif choice == "2":
                confirm = (
                    input("Вы уверены, что хотите очистить файл? (y/n): ")
                    .strip()
                    .lower()
                )
                if confirm == "y":
                    json_saver.clear()
                    print("Файл очищен.")

            elif choice == "3":
                all_vacancies = json_saver.get_vacancies()
                print(f"\nВсе сохраненные вакансии ({len(all_vacancies)}):")
                print_vacancies(all_vacancies[:10])  # Показываем первые 10

            elif choice == "0":
                break

            else:
                print("Неверный выбор. Попробуйте снова.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    user_interaction()
