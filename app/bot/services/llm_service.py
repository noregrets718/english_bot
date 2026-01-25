"""
Сервис для работы с LLM (Claude).
Генерация предложений и переводов.
"""

import anthropic
from loguru import logger

from app.config import settings
from app.bot.utils.exceptions import LLMError, TranslationError


class LLMService:
    """
    Сервис для работы с Anthropic Claude API.

    Основные функции:
    - Генерация примеров предложений с переводом
    - Получение перевода слова
    """

    def __init__(self):
        """Инициализация клиента Anthropic."""
        self.client = anthropic.Anthropic(
            api_key=settings.CLAUDE_API_KEY
        )
        self.model = "claude-3-5-haiku-20241022"  # Последняя модель
        logger.info("LLM Service initialized with Claude Haiku 3")

    async def generate_sentences(self, word: str, translation: str, count: int = 3) -> str:
        """
        Генерация примеров предложений с использованием слова.

        Returns:
            str: Raw text от LLM с предложениями
        """
        logger.info(f"Generating {count} sentences for word: '{word}' ({translation})")

        prompt = self._build_sentence_prompt(word, translation, count)

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}],
            )

            response_text = message.content[0].text
            logger.success(f"Generated sentences for '{word}'")
            return response_text

        except anthropic.APIError as e:
            logger.error(f"Anthropic API error: {e}")
            raise LLMError(f"Failed to generate sentences: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in generate_sentences: {e}")
            raise LLMError(f"Unexpected error: {str(e)}")

    async def get_translation(self, word: str) -> str:
        """
        Получить перевод слова на русский.

        Args:
            word: Английское слово

        Returns:
            str: Перевод на русский

        Raises:
            TranslationError: Если перевод не удался

        Example:
            "красивый"
        """
        logger.info(f"Getting translation for: '{word}'")

        prompt = f"""Переведи английское слово на русский язык. 
Дай только перевод без дополнительных объяснений.

Слово: {word}

Перевод:"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=100,
                temperature=0.3,  # Низкая температура для точного перевода
                messages=[{"role": "user", "content": prompt}],
            )

            translation = message.content[0].text.strip()
            logger.success(f"Translation for '{word}': {translation}")
            return translation

        except anthropic.APIError as e:
            logger.error(f"Translation API error: {e}")
            raise TranslationError(f"Failed to translate '{word}': {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in get_translation: {e}")
            raise TranslationError(f"Unexpected error: {str(e)}")

    def _build_sentence_prompt(self, word: str, translation: str, count: int) -> str:
        """
        Создать промпт для генерации предложений.

        Args:
            word: Английское слово
            translation: Перевод
            count: Количество предложений

        Returns:
            str: Промпт для Claude
        """
        return f"""Ты - опытный преподаватель английского языка. Твоя задача - помочь студенту запомнить новое слово, создав примеры предложений.

Слово: {word}
Перевод: {translation}

Создай {count} простых и понятных предложения на английском языке, которые помогут запомнить это слово. Каждое предложение должно:
1. Быть простым и естественным
2. Показывать разные контексты использования слова
3. Быть уровня A2-B1 (elementary-intermediate)

Для каждого предложения сразу дай перевод на русский.

Формат ответа (строго следуй ему):
1. [English sentence]
[Russian translation]

2. [English sentence]
[Russian translation]

3. [English sentence]
[Russian translation]

Пример:
1. I like to eat apples every morning.
Мне нравится есть яблоки каждое утро.

2. The apple tree in our garden is very old.
Яблоня в нашем саду очень старая.

3. She bought five red apples at the market.
Она купила пять красных яблок на рынке.

Теперь создай предложения для слова "{word}":"""