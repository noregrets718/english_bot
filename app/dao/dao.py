from datetime import date, datetime
from typing import Dict

from loguru import logger
from sqlalchemy import select, update, delete, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from app.dao.base import BaseDAO
from app.dao.models import User, Word


class UserDAO(BaseDAO[User]):
    model = User


class WordDAO(BaseDAO[Word]):
    model = Word