import os
import sys

from models.task_manager import TaskManager
from models.validators import get_input, get_validated_category, get_validated_date, get_validated_priority


class TaskManagerApp:
    """
    Класс приложения для работы с задачами.
    """
    def __init__(self) -> None:
        self.task_manager = TaskManager()
        self.task_manager.load_tasks()

    @staticmethod
    def clear_console() -> None:
        """
        Очищает консоль для удобного визуального отображения.
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def show_menu() -> None:
        """
        Показывает главное меню приложения.
        """
        print("Вас приветствует менеджер задач! Что Вы хотите сделать?\n")
        print("1. Посмотреть список всех задач")
        print("2. Посмотреть задачи по категории")
        print("3. Добавить задачу")
        print("4. Редактировать задачу")
        print("5. Отметить задачу как выполненную")
        print("6. Удалить задачу")
        print("7. Найти задачу по ключевому слову")
        print("8. Выход")

    def handle_choice(self, choice: str) -> None:
        """
        Обрабатывает выбор пользователя из главного меню.
        """
        if choice == "1":
            self.view_all_tasks()

        elif choice == "2":
            self.view_tasks_by_category()

        elif choice == "3":
            self.add_task()

        elif choice == "4":
            self.edit_task()

        elif choice == "5":
            self.mark_task_completed()

        elif choice == "6":
            self.remove_task()

        elif choice == "7":
            self.search_task()

        elif choice == "8":
            print("Выход из программы.")
            self.task_manager.save_tasks()
            sys.exit(0)

        else:
            print("\nТакого действия нет. Попробуйте снова.")
            input("\n---Нажмите Enter, чтобы продолжить---")

    def view_all_tasks(self) -> None:
        """
        Показывает все существующие задачи.
        """
        self.clear_console()

        tasks = self.task_manager.view_all_tasks()

        if tasks:
            print("Все задачи:\n")
            for task in tasks:
                print(task)
        else:
            print("Список задач пуст.\n"
                  "\nПопробуйте добавить новую задачу!")

        input("\n---Нажмите Enter для продолжения---")

    def view_tasks_by_category(self) -> None:
        """
        Показывает задачи по указанной категории.
        """
        self.clear_console()

        # Если задач нет
        if not self.task_manager.tasks:
            print("Список задач пуст.\n"
                  "\nПопробуйте добавить новую задачу!")
            input("\n---Нажмите Enter, чтобы вернуться в меню---")
            return  # Прерываем выполнение метода

        # Далее код выполняется если задачи есть
        category = get_validated_category()   # Получаем категорию из валидатора
        tasks = self.task_manager.view_tasks_by_category(category)

        if tasks:
            print(f"\nЗадачи в категории '{category}':\n")
            for task in tasks:
                print(task)
        else:
            print(f"\nНет задач в категории '{category}'.")

        input("\n---Нажмите Enter, чтобы вернуться в меню---")

    def add_task(self) -> None:
        """
        Добавляет новую задачу.
        """
        self.clear_console()

        print("Создание новой задачи.\n")

        title = get_input("Название: ")
        description = get_input("Описание: ")
        category = get_validated_category()   # Получаем валидные данные
        due_date = get_validated_date()
        priority = get_validated_priority()

        self.task_manager.add_task(title, description, category, due_date, priority)  # Добавляем задачу
        print("\nЗадача добавлена.")
        self.task_manager.save_tasks()  # Сохраняем

        input("\n---Нажмите Enter, чтобы вернуться в меню---")

    def edit_task(self) -> None:
        """
        Редактирует существующую задачу.
        """
        self.view_all_tasks()  # Показываем все задачи

        # Если задач нет
        if not self.task_manager.tasks:
            return      # Прерываем выполнение метода

        # Далее код выполняется если задачи есть
        task_id = get_input("\nВведите id задачи, которую хотите редактировать: ").strip()

        # Проверяем, существует ли задача с таким id
        task_exists = any(task.id == int(task_id) for task in self.task_manager.tasks)

        if not task_exists:
            print(f"\nЗадача с id {task_id} не найдена.")
            input("\n---Нажмите Enter, чтобы вернуться в меню---")
            return      # Прерываем выполнение метода, если задача не найдена

        # Если задача существует, запрашиваем новые значения
        print("\nВведите новые значения для полей."
              "\nЕсли Вы хотите оставить какое-то поле без изменений, просто нажимайте Enter.\n")

        title = get_input("Название: ", allow_empty=True) or None
        description = get_input("Описание: ", allow_empty=True) or None
        category = get_validated_category() or None
        due_date = get_validated_date() or None
        priority = get_validated_priority() or None

        # Делаем редактирование
        self.task_manager.edit_task(task_id, title, description, category, due_date, priority)
        print("\nЗадача успешно отредактирована.")

        # Сохраняем изменения в файл
        self.task_manager.save_tasks()

        input("\n---Нажмите Enter, чтобы вернуться в меню---")

    def mark_task_completed(self) -> None:
        """
        Отмечает задачу как выполненную.
        """
        self.view_all_tasks()

        # Если задач нет
        if not self.task_manager.tasks:
            return  # Прерываем выполнение метода

        # Далее код выполняется если задачи есть
        task_id = get_input("\nВведите id задачи, которой хотите установить статус 'Выполнена': ").strip()

        if self.task_manager.mark_task_completed(task_id):   # Проверяем есть ли задача с заданным id
            print("\nЗадаче присвоен статус 'Выполнена'.")
        else:
            print(f"\nЗадача с id {task_id} не найдена.")

        input("\n---Нажмите Enter, чтобы вернуться в меню---")

    def remove_task(self) -> None:
        """
        Удаляет задачу.
        """
        self.clear_console()

        # Если задач нет
        if not self.task_manager.tasks:
            print("Список задач пуст.\n"
                  "\nПопробуйте добавить новую задачу!")
            input("\n---Нажмите Enter, чтобы вернуться в меню---")
            return  # Прерываем выполнение метода

        # Далее код выполняется если задачи есть
        print("Выберите способ удаления задачи:\n"
              "\n1. Удалить задачу по id \n"
              "2. Удалить все задачи в категории\n")

        sub_choice = get_input("Введите 1 или 2: ")

        if sub_choice == "1":
            self.view_all_tasks()    # Показываем все задачи, чтобы выбрать нужную
            task_id = get_input("\nВведите id задачи, которую хотите удалить: ").strip()
            if self.task_manager.remove_tasks(task_id=task_id):
                print("\nЗадача успешно удалена.")
            else:
                print(f"\nЗадача с id {task_id} не найдена.")

        elif sub_choice == "2":
            category = get_validated_category()
            if self.task_manager.remove_tasks(category=category):
                print(f"\nВсе задачи в категории '{category}' успешно удалены.")
            else:
                print(f"\nЗадачи в категории '{category}' не найдены.")

        else:
            print("Такого действия нет. Попробуйте снова.")   # Проверка введенных данных

        self.task_manager.save_tasks()
        input("\n---Нажмите Enter, чтобы вернуться в меню---")

    def search_task(self) -> None:
        """
        Осуществляет поиск задачи по ключевому слову.
        """
        self.clear_console()

        # Если задач нет
        if not self.task_manager.tasks:
            print("Список задач пуст.\n"
                  "\nПопробуйте добавить новую задачу!")
            input("\n---Нажмите Enter, чтобы вернуться в меню---")
            return  # Прерываем выполнение метода

        # Далее код выполняется если задачи есть
        print("Поиск задачи возможен по слову в названии или описании, по статусу или приоритету.\n")
        keyword = get_input("Введите слово для поиска: ").strip()
        results = self.task_manager.search_tasks(keyword)

        if results:
            print("\nРезультаты поиска:\n")
            for result in results:
                print(result)
        else:
            print("\nЗадачи с таким словом не найдены.")

        input("\n---Нажмите Enter, чтобы вернуться в меню.---")

    def run(self) -> None:
        """
        Запускает главный цикл приложения.
        """
        while True:
            self.clear_console()
            self.show_menu()
            choice = get_input("\nВыберите действие: ")
            self.handle_choice(choice)


if __name__ == "__main__":
    app = TaskManagerApp()
    app.run()
