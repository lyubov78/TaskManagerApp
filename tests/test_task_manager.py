import pytest

from models.task_manager import TaskManager


@pytest.fixture
def task_manager():
    """
    Фикстура для инициализации TaskManager с тестовым файлом.
    """
    manager = TaskManager(filename="test_tasks.json")
    manager.tasks = []  # Очищаем задачи перед тестами
    return manager

@pytest.fixture
def setup_test_data(task_manager):
    """
    Фикстура для добавления тестовых данных.
    """
    task_manager.add_task(
        title="Тестовая задача 1",
        description="Описание задачи 1",
        category="Работа",
        due_date="2024-12-01",
        priority="Высокий"
    )
    task_manager.add_task(
        title="Текстовая задача 2",
        description="Описание задачи 2",
        category="Обучение",
        due_date="2024-12-02",
        priority="Средний"
    )
    task_manager.add_task(
        title="Текстовая задача 3",
        description="Описание задачи 3",
        category="Покупки",
        due_date="2024-12-31",
        priority="Низкий"
    )
    return task_manager

def test_add_task(task_manager):
    """
    Тест на добавление задачи.
    """
    initial_count = len(task_manager.tasks)
    task_manager.add_task(
        title="Новая задача",
        description="Описание новой задачи",
        category="Личное",
        due_date="2025-01-11",
        priority="Низкий"
    )
    assert len(task_manager.tasks) == initial_count + 1  # Проверяем, что количество задач увеличилось

def test_view_all_tasks(setup_test_data):
    """
    Тест на просмотр всех задач.
    """
    tasks = setup_test_data.view_all_tasks()
    assert len(tasks) == 3  # Должно быть 3 задачи
    assert "Название: Тестовая задача 1" in tasks[0]

def test_edit_task(setup_test_data):
    """
    Тест на редактирование задачи.
    """
    task_id = setup_test_data.tasks[0].id
    result = setup_test_data.edit_task(task_id=str(task_id), title="Новое название задачи")
    assert result is True  # Задача должна быть отредактирована
    assert setup_test_data.tasks[0].title == "Новое название задачи"

def test_remove_task(setup_test_data):
    """
    Тест на удаление задачи по ID.
    """
    task_id = setup_test_data.tasks[0].id
    result = setup_test_data.remove_tasks(task_id=str(task_id))
    assert result is True  # Задача должна быть удалена
    assert len(setup_test_data.tasks) == 2  # Должна остаться 2 задача

def test_remove_task_by_category(setup_test_data):
    """
    Тест на удаление задач по категории.
    """
    result = setup_test_data.remove_tasks(category="Обучение")
    assert result is True  # Задача из категории 'Обучение' должна быть удалена
    assert len(setup_test_data.tasks) == 2  # Должны остаться 2 задачи из других категорий

def test_search_tasks(setup_test_data):
    """
    Тест на поиск задач.
    """
    result = setup_test_data.search_tasks("тестовая задача 1")
    assert len(result) == 1  # Должна быть найдена только одна задача
    assert "Тестовая задача 1" in result[0]
