from django.db import models
import datetime
from account.models import Account
from account.choices import MONEY_ORDER_TRANSACTION_TYPE_CHOICES, MONEY_ORDER_TRANSACTION_MODE_CHOICES


# Create your models here.

class Order(models.Model):
    policy_number = models.CharField(max_length=60)
    policy_holder_name = models.CharField(max_length=60)
    amount = models.FloatField(default=None)
    due_date = models.CharField(max_length=30)
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    approved_by = models.EmailField(max_length=60, default='notdoneyet@gmail.com')
    date = models.DateField(auto_now_add=True, auto_now=False)
    time = models.TimeField(auto_now_add=True, auto_now=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(
            self.policy_number + " | " + self.policy_holder_name + " | " + str(
                self.amount) + " | " + self.created_by.email)


class Moneyorder(models.Model):
    order_amount = models.IntegerField(default=0)
    order_created_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    order_approved_by = models.EmailField(max_length=60, default='notdoneyet@gmail.com')
    order_coupon_code = models.CharField(max_length=30, default='00')
    order_status = models.BooleanField(default=False)
    order_mode =  models.IntegerField(choices=MONEY_ORDER_TRANSACTION_MODE_CHOICES, default=1)
    order_remark = models.CharField(max_length=60, default='InProgress')
    date = models.DateField(auto_now_add=True, auto_now=False)
    time = models.TimeField(auto_now_add=True, auto_now=False)
    is_approved = models.BooleanField(default=False)
    From = models.CharField(max_length=60, default='NULL')
    order_type = models.IntegerField(choices=MONEY_ORDER_TRANSACTION_TYPE_CHOICES, default=1)

    # def __str__(self):
    #     return str(
    #         str(self.order_created_by) + " | " +
    #         str(self.order_amount) + " | " + str(self.From) + " | " + str(self.order_type) + " | " + self.order_approved_by.email)
