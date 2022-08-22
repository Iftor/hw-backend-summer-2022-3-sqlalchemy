from dataclasses import dataclass
from app.store.database.sqlalchemy_base import db


@dataclass
class Theme:
    id: int | None
    title: str


@dataclass
class Question:
    id: int | None
    title: str
    theme_id: int
    answers: list["Answer"]


@dataclass
class Answer:
    title: str
    is_correct: bool


class ThemeModel(db):
    __tablename__ = "themes"
    pass


class QuestionModel(db):
    __tablename__ = "questions"
    pass


class AnswerModel(db):
    __tablename__ = "answers"
    pass
