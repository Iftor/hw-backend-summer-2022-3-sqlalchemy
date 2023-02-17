from aiohttp.web import HTTPForbidden, HTTPUnauthorized
from aiohttp_apispec import request_schema, response_schema
from aiohttp_session import new_session

from app.admin.schemes import AdminSchema
from app.web.app import View
from app.web.utils import json_response


class AdminLoginView(View):
    @request_schema(AdminSchema)
    @response_schema(AdminSchema, 200)
    async def post(self):
        email = self.data["email"]
        password = self.data["password"]

        manager_data = await self.store.admins.get_by_email(email)
        if not manager_data:
            raise HTTPForbidden

        if not manager_data.is_password_valid(password):
            raise HTTPForbidden

        session = await new_session(self.request)
        raw_manager_data = AdminSchema().dump(manager_data)
        session["admin"] = raw_manager_data

        return json_response(data=raw_manager_data)


class AdminCurrentView(View):
    @response_schema(AdminSchema, 200)
    async def get(self):
        if not (manager_data := self.request.admin):
            raise HTTPUnauthorized
        return json_response(data=AdminSchema().dump(manager_data))
