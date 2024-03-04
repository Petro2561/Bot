class ValidationError(Exception):
    """Класс исключений для валидации"""

    def __init__(self, message):
        super().__init__(message)
