from fastapi import Request
from fastapi.responses import RedirectResponse
from sqladmin import BaseView, expose
from httpx import AsyncClient
from starlette.responses import HTMLResponse

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


class PasswordRecoveryAdmin(BaseView):
    def is_visible(self, request: Request) -> bool:
        return False

    async def call_forgot_password_endpoint(self, email: str):
        async with AsyncClient() as client:
            response = await client.post(
                f"{settings.BASE_URL}/api/v1/auth/forgot-password",
                json={
                    "email": email,
                },
            )
        return response

    async def call_reset_password_endpoint(self, token: str, password: str):
        async with AsyncClient() as client:
            response = await client.post(
                f"{settings.BASE_URL}/api/v1/auth/reset-password",
                json={
                    "token": token,
                    "password": password,
                },
            )
        return response

    @expose("/forgot-password", methods=["GET", "POST"])
    async def forgot_password(self, request: Request):
        context = {}
        if request.method == "GET":
            context["forgot_password"] = "forgot"
            return await self.templates.TemplateResponse(
                request, "forgot_password.html", context=context
            )
        else:
            form = await request.form()
            email = form.get("email", None)
            response = await self.call_forgot_password_endpoint(email)
            if response.status_code == 202:
                context["success_message"] = (
                    "Password recovery request sent successfully."
                )
            else:
                context["error_message"] = (
                    response.json().get("detail", None)
                    if response.json()
                    else "Unexpected error"
                )
        return await self.templates.TemplateResponse(request, "login.html", context)

    @expose("/forgot-password/reset", methods=["GET", "POST"])
    async def reset_password(self, request: Request):
        context = {}
        if request.method == "GET":
            context["forgot_password"] = "reset"
            return await self.templates.TemplateResponse(
                request, "forgot_password.html", context
            )
        else:
            token = request.query_params.get("token")
            form = await request.form()
            new_password = form.get("new_password", None)
            confirm_password = form.get("confirm_password", None)
            if new_password == confirm_password:
                response = await self.call_reset_password_endpoint(token, new_password)
                if response.status_code == 200:
                    context["success_message"] = (
                        "Password has been successfully recovered."
                    )
                else:
                    error = response.json().get("detail", None)
                    if error:
                        context["error_message"] = "SERVER ERROR"
                        if error == "RESET_PASSWORD_BAD_TOKEN":
                            context["error_message"] = "Invalid password recovery link"
                        elif isinstance(error, dict):
                            reason = error.get("reason")
                            if reason:
                                context["error_message"] = reason
                    return await self.templates.TemplateResponse(
                        request, "forgot_password.html", context
                    )
            else:
                context["error"] = "passwords must match"
                return await self.templates.TemplateResponse(
                    request,
                    "forgot_password.html",
                    context=context,
                )
        return await self.templates.TemplateResponse(request, "login.html", context)
