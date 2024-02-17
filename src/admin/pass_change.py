from sqladmin import BaseView, expose
from httpx import AsyncClient

from src.config import settings


class ChangePasswordAdmin(BaseView):
    name = "Зміна паролю"
    icon = "fa-solid fa-key"

    async def call_change_password_endpoint(
        self, old_password, new_password, confirm_password, token: str
    ):
        async with AsyncClient() as client:
            response = await client.post(
                f"{settings.BASE_URL}/api/v1/auth/change-password",
                data={
                    "old_password": old_password,
                    "new_password": new_password,
                    "new_password_confirm": confirm_password,
                },
                headers={"Authorization": f"Bearer {token}"},
            )
        return response

    @expose("/change_password", methods=["GET", "POST"])
    async def change_pass_page(self, request):
        error_message = None
        success_message = None
        if request.method == "POST":
            form = await request.form()
            old_password = form["old_password"]
            new_password = form["new_password"]
            confirm_password = form["confirm_password"]
            token = request.session["token"]
            response = await self.call_change_password_endpoint(
                old_password, new_password, confirm_password, token
            )
            if response.status_code == 200:
                success_message = "Password changed successfully!"
            else:
                error_message = response.json().get("detail")
        return await self.templates.TemplateResponse(
            request,
            "change_password.html",
            context={
                "error_message": error_message,
                "success_message": success_message,
            },
        )
