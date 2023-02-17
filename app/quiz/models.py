from dataclasses import dataclass

from sqlalchemy import BigInteger, Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

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

    id = Column(BigInteger(), primary_key=True)
    title = Column(String(50), nullable=False, unique=True)

    @property
    def dataclass(self) -> Theme:
        return Theme(id=self.id, title=self.title)

    def __repr__(self) -> str:
        return self.title


class AnswerModel(db):
    __tablename__ = "answers"

    id = Column(BigInteger(), primary_key=True)
    title = Column(String(50), nullable=False)
    is_correct = Column(Boolean(), nullable=False)
    question_id = Column(ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)

    @property
    def dataclass(self) -> Answer:
        return Answer(title=self.title, is_correct=self.is_correct)

    def __repr__(self) -> str:
        return self.title


class QuestionModel(db):
    __tablename__ = "questions"

    id = Column(BigInteger(), primary_key=True)
    title = Column(String(50), nullable=False, unique=True)
    theme_id = Column(ForeignKey("themes.id", ondelete="CASCADE"), nullable=False)
    answers = relationship("AnswerModel")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self._answers: list[AnswerModel] = []

    @property
    def dataclass(self) -> Question:
        return Question(
            id=self.id,
            title=self.title,
            theme_id=self.theme_id,
            answers=[answer.dataclass for answer in self.answers],
        )

    def __repr__(self):
        return self.title
