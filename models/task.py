from typing import Optional


class Task:
    """
    Класс задачи.
    :param id: Идентификатор задачи (по умолчанию генерируется автоматически).
    :param title: Название задачи.
    :param description: Описание задачи.
    :param category: Категория задачи.
    :param due_date: Срок выполнения задачи (в формате YYYY-MM-DD).
    :param priority: Приоритет задачи.
    :param status: Статус задачи (по умолчанию новая задача создаётся со статусом "Не выполнена").
    """
    def __init__(self, title: str, description: str, category: str, due_date: str, priority: str,
                 status: str = "Не выполнена", id: Optional[int] = None) -> None:
        self.id = id or Task.get_task_id()
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status

    @classmethod
    def get_task_id(cls) -> int:
        """
        Присваивает каждой новой задаче уникальный id.
        """
        if not hasattr(cls, 'id'):    # Проверяем, существует ли атрибут id в текущем экземпляре
            cls.id = 1
        task_id = cls.id
        cls.id += 1
        return task_id

    def mark_as_completed(self) -> None:
        """
        Изменяет статус задачи на "Выполнена".
        """
        self.status = "Выполнена"

    def __str__(self) -> str:
        """
        Строковое представление задачи.
        """
        return (
            f"id: {self.id}\n"
            f"Название: {self.title}\n"
            f"Описание: {self.description}\n"
            f"Категория: {self.category}\n"
            f"Срок выполнения: {self.due_date}\n"
            f"Приоритет: {self.priority}\n"
            f"Статус: {self.status}"
        )
