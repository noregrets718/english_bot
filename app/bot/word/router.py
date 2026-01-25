from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.router import Router
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.word.service import WordService
from app.bot.word.kbs import words_list_kb, word_detail_kb, confirm_delete_kb, sentences_kb
from app.bot.utils.exceptions import RateLimitError, TranslationError, LLMError
from app.bot.user.kbs import main_user_kb

router = Router()


@router.message(F.text)
async def handle_new_word(message: Message, session_with_commit: AsyncSession):
    word = message.text.strip().lower()
    user_id = message.from_user.id

    service = WordService(session_with_commit)
    try:
        word_obj = await service.add_word(user_id=user_id, word=word)
        text = f"✅ Слово добавлено:\n\n{word_obj.word} - {word_obj.translation}"
        await message.answer(text, reply_markup=main_user_kb(user_id))
    except RateLimitError:
        await message.answer("⏳ Сервис перегружен. Попробуйте через минуту.")
    except TranslationError:
        await message.answer("❌ Не удалось получить перевод. Попробуйте позже.")


@router.callback_query(F.data == "my_words")
async def show_words(callback: CallbackQuery, session_without_commit: AsyncSession):
    user_id = callback.from_user.id
    service = WordService(session_without_commit)
    words = await service.get_user_words(user_id)

    if not words:
        await callback.message.edit_text("📚 Ваш словарь пуст")
        return

    await callback.message.edit_text("📚 Ваш словарь:", reply_markup=words_list_kb(words))
    await callback.answer()


@router.callback_query(F.data.startswith("word_"))
async def show_word_detail(callback: CallbackQuery, session_without_commit: AsyncSession):
    word_id = int(callback.data.split("_")[1])
    service = WordService(session_without_commit)
    word = await service.get_word_by_id(word_id)

    if not word:
        await callback.answer("Слово не найдено", show_alert=True)
        return

    has_sentences = bool(word.sentences_text)

    text = f"📝 {word.word}\n\n🔤 Перевод: {word.translation}"
    await callback.message.edit_text(text, reply_markup=word_detail_kb(word_id, has_sentences))
    await callback.answer()


@router.callback_query(F.data.startswith("delete_word_"))
async def confirm_delete(callback: CallbackQuery):
    word_id = int(callback.data.split("_")[2])
    await callback.message.edit_text("Удалить слово?", reply_markup=confirm_delete_kb(word_id))
    await callback.answer()


@router.callback_query(F.data.startswith("confirm_delete_"))
async def delete_word(callback: CallbackQuery, session_with_commit: AsyncSession):
    word_id = int(callback.data.split("_")[2])
    service = WordService(session_with_commit)
    await service.delete_word(word_id)

    await callback.message.edit_text("✅ Слово удалено",reply_markup=main_user_kb(callback.from_user.id))
    await callback.answer()


@router.callback_query(F.data.startswith("generate_"))
async def generate_sentences(callback: CallbackQuery, session_with_commit: AsyncSession):
    word_id = int(callback.data.split("_")[1])

    await callback.message.edit_text("⏳ Генерирую предложения...")
    await callback.answer()

    try:
        sentences_text = await WordService(session_with_commit).generate_sentences(word_id)
        if sentences_text:
            text = f"✅ Предложения созданы:\n\n{sentences_text}"
            await callback.message.edit_text(text, reply_markup=sentences_kb(word_id))
        else:
            await callback.message.edit_text("❌ Не удалось создать предложения")
    except (RateLimitError, LLMError):
        await callback.message.edit_text("⏳ Сервис перегружен. Попробуйте позже.")


@router.callback_query(F.data.startswith("sentences_"))
async def show_sentences(callback: CallbackQuery, session_without_commit: AsyncSession):
    word_id = int(callback.data.split("_")[1])

    sentences_text = await WordService(session_without_commit).get_sentences(word_id)
    if not sentences_text:
        await callback.answer("Предложения не найдены", show_alert=True)
        return

    text = f"📖 Предложения:\n\n{sentences_text}"
    await callback.message.edit_text(text, reply_markup=sentences_kb(word_id))
    await callback.answer()


@router.callback_query(F.data.startswith("regen_"))
async def regenerate_sentences(callback: CallbackQuery, session_with_commit: AsyncSession):
    word_id = int(callback.data.split("_")[1])

    await callback.message.edit_text("⏳ Перегенерирую предложения...")
    await callback.answer()

    try:
        sentences_text = await WordService(session_with_commit).regenerate_sentences(word_id)
        if sentences_text:
            text = f"✅ Новые предложения:\n\n{sentences_text}"
            await callback.message.edit_text(text, reply_markup=sentences_kb(word_id))
        else:
            await callback.message.edit_text("❌ Не удалось создать предложения")
    except (RateLimitError, LLMError):
        await callback.message.edit_text("⏳ Сервис перегружен. Попробуйте позже.")