from django.utils.translation import gettext_lazy as _
ROLE_CHOICES = (
    (1, _("Branch")),
    (2, _("Manager")),
)

MONEY_ORDER_TRANSACTION_TYPE_CHOICES = (
    (1, _("CREDIT")),
    (2, _("DEBIT")),
)

MONEY_ORDER_TRANSACTION_MODE_CHOICES = (
    (1, _("UPI")),
    (2, _("BANK TRANSFER")),
    (3, _("CASH")),
    (4, _("REFUND")),
)