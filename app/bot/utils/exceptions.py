"""
Кастомные исключения для приложения.
"""


class BotError(Exception):
    """Базовый класс для всех ошибок бота."""

    def __init__(self, message: str = "An error occurred"):
        self.message = message
        super().__init__(self.message)


class LLMError(BotError):
    """Ошибка при работе с LLM API."""

    def __init__(self, message: str = "LLM API error"):
        super().__init__(f"LLM Error: {message}")


class WordNotFoundError(BotError):
    """Слово не найдено в базе данных."""

    def __init__(self, word: str):
        super().__init__(f"Word '{word}' not found")
        self.word = word


class WordAlreadyExistsError(BotError):
    """Слово уже существует в базе пользователя."""

    def __init__(self, word: str):
        super().__init__(f"Word '{word}' already exists")
        self.word = word


class TranslationError(BotError):
    """Ошибка при получении перевода."""

    def __init__(self, message: str = "Translation failed"):
        super().__init__(f"Translation Error: {message}")


class RateLimitError(BotError):
    """Превышен лимит запросов к API."""

    def __init__(self, retry_after: int = 60):
        self.retry_after = retry_after
        super().__init__(f"Rate limit exceeded. Retry after {retry_after}s")