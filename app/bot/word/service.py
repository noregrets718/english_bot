from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.dao import UserDAO, WordDAO
from app.dao.models import Word
from app.bot.word.schemas import SWordCreate, SWordFilter, SWordUpdate
from app.bot.services.llm_service import LLMService


class WordService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_dao = UserDAO(session)
        self.word_dao = WordDAO(session)
        self.llm = LLMService()

    async def add_word(self, user_id: int, word: str, translation: str | None = None) -> Word:
        if translation is None:
            translation = await self.llm.get_translation(word)

        existing = await self.word_dao.find_one_or_none(SWordFilter(user_id=user_id, word=word))
        if existing:
            logger.warning(f"Word '{word}' already exists for user {user_id}")
            return existing

        word_schema = SWordCreate(user_id=user_id, word=word, translation=translation)
        word_obj = await self.word_dao.add(word_schema)
        logger.info(f"Word '{word}' added for user {user_id}")
        return word_obj

    async def get_user_words(self, user_id: int) -> list[Word]:
        words = await self.word_dao.find_all(SWordFilter(user_id=user_id))
        return words

    async def get_word_by_id(self, word_id: int) -> Word | None:
        return await self.word_dao.find_one_or_none_by_id(word_id)

    async def delete_word(self, word_id: int) -> int:
        return await self.word_dao.delete(SWordFilter(id=word_id))

    async def generate_sentences(self, word_id: int) -> str | None:
        word = await self.word_dao.find_one_or_none_by_id(word_id)
        if not word:
            logger.warning(f"Word with id {word_id} not found")
            return None

        sentences_text = await self.llm.generate_sentences(word.word, word.translation)

        await self.word_dao.update(
            SWordFilter(id=word_id),
            SWordUpdate(sentences_text=sentences_text)
        )

        logger.info(f"Generated sentences for word '{word.word}'")
        return sentences_text

    async def get_sentences(self, word_id: int) -> str | None:
        word = await self.word_dao.find_one_or_none_by_id(word_id)
        return word.sentences_text if word else None

    async def regenerate_sentences(self, word_id: int) -> str | None:
        return await self.generate_sentences(word_id)