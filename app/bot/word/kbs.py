from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def words_list_kb(words: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for word in words:
        kb.add(InlineKeyboardButton(
            text=f"{word.word} - {word.translation}",
            callback_data=f"word_{word.id}"
        ))
    # kb.add(InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main"))
    kb.adjust(1)
    return kb.as_markup()


def word_detail_kb(word_id: int, has_sentences: bool = False) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if has_sentences:
        kb.add(InlineKeyboardButton(text="📖 Предложения", callback_data=f"sentences_{word_id}"))
        kb.add(InlineKeyboardButton(text="🔄 Перегенерировать", callback_data=f"regen_{word_id}"))
    else:
        kb.add(InlineKeyboardButton(text="✨ Создать предложения", callback_data=f"generate_{word_id}"))
    kb.add(InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delete_word_{word_id}"))
    kb.add(InlineKeyboardButton(text="◀️ Назад", callback_data="my_words"))
    kb.adjust(1)
    return kb.as_markup()


def confirm_delete_kb(word_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="✅ Да", callback_data=f"confirm_delete_{word_id}"))
    kb.add(InlineKeyboardButton(text="❌ Нет", callback_data=f"word_{word_id}"))
    kb.adjust(2)
    return kb.as_markup()


def sentences_kb(word_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="🔄 Перегенерировать", callback_data=f"regen_{word_id}"))
    kb.add(InlineKeyboardButton(text="◀️ К слову", callback_data=f"word_{word_id}"))
    kb.adjust(1)
    return kb.as_markup()