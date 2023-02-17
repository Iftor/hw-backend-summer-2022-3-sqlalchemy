from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    Answer,
    Question,
    Theme,
    ThemeModel,
    QuestionModel, AnswerModel,
)


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        theme = ThemeModel(title=title)
        async with self.app.database.session.begin() as session:
            session.add(theme)
            await session.commit()
        return theme.dataclass

    async def get_theme_by_title(self, title: str) -> Theme | None:
        query = select(ThemeModel).where(ThemeModel.title == title)
        async with self.app.database.session.begin() as session:
            theme = (await session.scalars(query)).first()
        if not theme:
            return None
        return theme.dataclass

    async def get_theme_by_id(self, id_: int) -> Theme | None:
        query = select(ThemeModel).where(ThemeModel.id == id_)
        async with self.app.database.session.begin() as session:
            theme = (await session.scalars(query)).first()
        if not theme:
            return None
        return theme.dataclass

    async def list_themes(self) -> list[Theme]:
        async with self.app.database.session.begin() as session:
            themes = await session.scalars(select(ThemeModel))
        return [theme.dataclass for theme in themes]

    async def create_answers(self, question_id: int, answers: list[Answer]) -> list[AnswerModel]:
        answers_ = []
        for answer in answers:
            answer_ = AnswerModel(title=answer.title, is_correct=answer.is_correct, question_id=question_id)
            answers_.append(answer_)
        return answers_

    async def create_question(self, title: str, theme_id: int, answers: list[Answer]) -> Question:
        question = QuestionModel(title=title, theme_id=theme_id)
        async with self.app.database.session.begin() as session:
            session.add(question)
            await session.flush()
            answers_ = await self.create_answers(question.id, answers)
            session.add_all(answers_)
            await session.commit()
        return await self.get_question_by_title(question.title)

    async def get_question_by_title(self, title: str) -> Question | None:
        query = select(QuestionModel).options(joinedload(QuestionModel.answers)).where(QuestionModel.title == title)
        async with self.app.database.session.begin() as session:
            question = (await session.scalars(query)).first()
        if not question:
            return None
        return question.dataclass

    async def list_questions(self, theme_id: int | None = None) -> list[Question]:
        query = select(QuestionModel).options(joinedload(QuestionModel.answers))
        if theme_id:
            query = query.where(QuestionModel.theme_id == theme_id)
        async with self.app.database.session.begin() as session:
            questions = (await session.scalars(query)).unique()
        return [question.dataclass for question in questions]
