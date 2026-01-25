from pydantic import BaseModel


class SWord(BaseModel):
    id: int
    user_id: int
    word: str
    translation: str


class SWordCreate(BaseModel):
    user_id: int
    word: str
    translation: str


class SWordFilter(BaseModel):
    id: int | None = None
    user_id: int | None = None
    word: str | None = None


class SWordUpdate(BaseModel):
    sentences_text: str | None = None