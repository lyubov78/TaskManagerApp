import json
from typing import List, Optional

from .task import Task


class TaskManager:
    """
    Класс для управления задачами.
    """
    def __init__(self, filename: str = "tasks.json") -> None:
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def load_tasks(self) -> None:
        """
        Загружает задачи из JSON-файла для последующей загрузки в приложение.
        """
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                tasks_data = json.load(f)
                self.tasks = [Task(**task) for task in tasks_data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []  # Если файл не существует или не может быть прочитан, инициализируем пустой список

    def save_tasks(self) -> None:
        """
        Сохраняет задачи в JSON-файл для последующей загрузки в приложение.
        """
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([task.__dict__ for task in self.tasks], f, ensure_ascii=False, indent=4)

    def view_all_tasks(self) -> List[str]:
        """
        Возвращает список всех задач в строковом представлении.
        """
        return [str(task) + "\n" + "-"*20 for task in self.tasks]  # Разделитель между задачами для удобства чтения

    def add_task(self, title: str, description: str, category: str, due_date: str, priority: str) -> None:
        """
        Добавляет новую задачу в список задач.
        """
        new_task_id = max([task.id for task in self.tasks], default=0) + 1  # Находим последней id и увеличиваем на 1
        new_task = Task(title, description, category, due_date, priority, id=new_task_id)  # Передаем новый id
        self.tasks.append(new_task)
        self.save_tasks()

    def view_tasks_by_category(self, category: str) -> List[str]:
        """
        Возвращает список задач по категории.
        """
        category = category.lower()    # Приводим к нижнему регистру, чтобы сравнение было точным
        result = []
        for task in self.tasks:
            if task.category.lower() == category:
                result.append(str(task) + "\n" + "-"*20)  # Разделитель между задачами для удобства чтения
        return result

    def search_tasks(self, keyword: str) -> List[str]:
        """
        Находит задачи по ключевому слову в названии или описании, статусу или приоритету.
        """
        result = []
        keyword_lower = keyword.lower()   # Приводим ключевое слово к нижнему регистру для сравнения
        for task in self.tasks:
            title_match = keyword_lower in task.title.lower()        # Поиск в названии
            description_match = keyword_lower in task.description.lower()  # Поиск в описании
            status_match = keyword_lower == task.status.lower()            # Поиск точного совпадения статуса
            priority_match = keyword_lower == task.priority.lower()        # Поиск точного совпадения приоритета

            if title_match or description_match or status_match or priority_match:
                result.append(str(task) + "\n" + "-"*20)

        return result

    def mark_task_completed(self, task_id: str) -> bool:
        """
        Находит задачу по id и присваивает ей статус "Выполнена".
        Возвращает True, если задача найдена и статус изменён, иначе False.
        """
        task = None
        for t in self.tasks:
            if t.id == int(task_id):
                task = t
                break  # Прерываем цикл, если нашли нужную задачу

        if task:
            task.mark_as_completed()
            self.save_tasks()
            return True  # Задача найдена и статус обновлен
        else:
            return False  # Задача не найдена

    def remove_tasks(self, task_id: Optional[str] = None, category: Optional[str] = None) -> bool:
        """
        Удаляет одну задачу по указанному id или все задачи в выбранной категории.
        Возвращает True, если задача или задачи удалены, иначе False.
        """
        # Если передан id
        if task_id:
            task_to_remove = None
            for task in self.tasks:
                if task.id == int(task_id):
                    task_to_remove = task
                    break      # Прерываем цикл, если нашли нужную задачу

            if task_to_remove:
                self.tasks = [task for task in self.tasks if task.id != int(task_id)]
                self.save_tasks()
                return True   # Задача найдена по id и удалена
            else:
                return False  # Задача с таким id не найдена

        # Если передана категория
        elif category:
            tasks_to_remove = [task for task in self.tasks if task.category.lower() == category.lower()]
            if tasks_to_remove:
                self.tasks = [task for task in self.tasks if task.category.lower() != category.lower()]
                self.save_tasks()
                return True   # Задачи с указанной категорией удалены
            else:
                return False  # Задачи с такой категорией не найдены

        return False  # Если ничего не указано

    def edit_task(self, task_id: str, title: Optional[str] = None, description: Optional[str] = None,
                  category: Optional[str] = None, due_date: Optional[str] = None,
                  priority: Optional[str] = None) -> bool:
        """
        Находит задачу по id и редактирует её.
        Возвращает True, если задача найдена и отредактирована, иначе False.
        """
        task = None
        for t in self.tasks:
            if t.id == int(task_id):
                task = t
                break  # Прерываем цикл, если нашли нужную задачу

        if task:
            if title:
                task.title = title
            if description:
                task.description = description
            if category:
                task.category = category
            if due_date:
                task.due_date = due_date
            if priority:
                task.priority = priority
            self.save_tasks()
            return True  # Задача отредактирована успешно
        else:
            return False  # Задача с таким id не найдена
