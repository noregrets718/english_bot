from datetime import datetime
from typing import List

from sqlalchemy import BigInteger, String
from app.dao.database import Base
from sqlalchemy import Integer, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]

    words: Mapped[List["Word"]] = relationship(
        "Word",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<User(telegram_id={self.id}, username={self.username})>"


class Word(Base):
    """
    Модель слова для изучения.

    Связана с пользователем (one-to-many).
    Одно слово может иметь несколько предложений.
    """

    __tablename__ = "words"

    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True)

    # Foreign Key к пользователю
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Само слово (на английском)
    word: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        comment="Английское слово"
    )

    # Перевод слова
    translation: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        comment="Перевод на родной язык"
    )

    user: Mapped["User"] = relationship("User", back_populates="words")