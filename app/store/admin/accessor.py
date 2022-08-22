import typing

from sqlalchemy import select

from app.admin.models import Admin, AdminModel
from app.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def get_by_email(self, email: str) -> Admin | None:
        raise NotImplemented

    async def create_admin(self, email: str, password: str) -> Admin:
        raise NotImplemented
