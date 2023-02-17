import typing
from hashlib import sha256

from sqlalchemy import select

from app.admin.models import Admin, AdminModel
from app.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def get_by_email(self, email: str) -> Admin | None:
        query = select(AdminModel).where(AdminModel.email == email)
        async with self.app.database.session.begin() as session:
            admin = (await session.scalars(query)).first()
        if not admin:
            return None
        return admin.dataclass

    async def create_admin(self, email: str, password: str) -> Admin:
        admin = AdminModel(email=email, password=sha256(password.encode()).hexdigest())
        async with self.app.database.session.begin() as session:
            session.add(admin)
            await session.commit()
        return AdminModel.dataclass

