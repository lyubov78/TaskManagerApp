import re


def get_input(prompt: str, error_msg: str = "\nПоле не должно быть пустым!\n", allow_empty: bool = False) -> str | None:
    """
    Проверяет, что ввод пользователя не пустой, если allow_empty=False.
    Если allow_empty=True и разрешен пустой ввод, возвращает None для пустого ввода.
    """
    while True:
        user_input = input(prompt).strip()  # Удаляем пробелы в начале и конце строки
        if not user_input and not allow_empty:  # Проверка на пустое значение, если пустой ввод не разрешен
            print(error_msg)
            continue
        if user_input == "" and allow_empty:  # Если разрешен пустой ввод
            return None
        return user_input

def get_validated_category() -> str | None:
    """
    Запрашивает у пользователя категорию и проверяет корректность ввода.
    Если ввод пустой, возвращает None.
    """
    while True:
        category = get_input("Категория (работа, личное, покупки, обучение): ", allow_empty=True)
        if category:  # Применяем title() только если категория не пустая
            category = category.title()
        if category is None or validate_category(category):
            return category
        else:
            print("\nТакой категории нет. Выберите одну из следующих: работа, личное, покупки, обучение.\n")

def validate_category(category: str) -> bool:
    """
    Проверяет, что категория находится в списке допустимых значений.
    """
    valid_categories = ["Работа", "Личное", "Покупки", "Обучение"]
    return category in valid_categories

def get_validated_date() -> str | None:
    """
    Запрашивает у пользователя дату и проверяет правильность формата (YYYY-MM-DD).
    Если ввод пустой, возвращает None.
    """
    while True:
        due_date = get_input("Срок выполнения (в формате YYYY-MM-DD): ", allow_empty=True)
        if due_date is None or validate_date(due_date):
            return due_date
        else:
            print("\nНеверный формат даты. Используйте YYYY-MM-DD.\n")

def validate_date(date: str) -> bool:
    """
    Проверяет, что дата соответствует формату YYYY-MM-DD.
    """
    return bool(re.match(r"\d{4}-\d{2}-\d{2}", date))

def get_validated_priority() -> str | None:
    """
    Запрашивает у пользователя приоритет и проверяет корректность ввода.
    Если ввод пустой, возвращает None.
    """
    while True:
        priority = get_input("Приоритет (низкий, средний, высокий): ", allow_empty=True)
        if priority:  # Применяем title() только если приоритет не пустой
            priority = priority.title()
        if priority is None or validate_priority(priority):
            return priority
        else:
            print("\nТакого варианта нет. Возможные приоритеты: низкий, средний или высокий.\n")

def validate_priority(priority: str) -> bool:
    """
    Проверяет, что приоритет находится в списке допустимых значений.
    """
    valid_priorities = ["Низкий", "Средний", "Высокий"]
    return priority in valid_priorities
