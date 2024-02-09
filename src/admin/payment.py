from sqladmin import ModelView

from src.payment.models import PaymentDetails


class PaymentAdmin(ModelView, model=PaymentDetails):
    column_list = [
        PaymentDetails.info,
        PaymentDetails.iban,
        PaymentDetails.coffee_url,
        PaymentDetails.patreon_url,
        PaymentDetails.qr_code_url,
    ]
    column_details_exclude_list = ["id"]
    can_export = False
    can_edit = True
    can_create = False
    can_delete = False
