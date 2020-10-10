from django.db import models
import datetime


# Create your models here.

class Order(models.Model):
    policyNumber = models.CharField(max_length=60)
    policyHolderName = models.CharField(max_length=60)
    amount = models.FloatField(default=None)
    dueDate = models.CharField(max_length=30)
    createdBy = models.EmailField(max_length=60)
    approvedBy = models.EmailField(max_length=60, default='fake@gmail.com')
    date = models.DateField(auto_now_add=True, auto_now=False)
    time = models.TimeField(auto_now_add=True, auto_now=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(
            self.policyNumber + " | " + self.policyHolderName + " | " + str(self.amount) + " | " + self.createdBy)

    @classmethod
    def getdata(cls):
        return {'policyNumber': cls.policyNumber, 'policyHolderName': cls.policyHolderName, 'amount': cls.amount,
                'dueDate': cls.dueDate, 'createdBy': cls.createdBy, 'date': cls.date, 'time': cls.time,
                'completed': cls.completed
                }

    @classmethod
    def create(cls, policyNumber, policyHolderName, amount, dueDate, createdBy, approvedBy, completed):
        order = cls(
            policyNumber=policyNumber,
            policyHolderName=policyHolderName,
            amount=amount,
            dueDate=dueDate,
            createdBy=createdBy,
            approvedBy=approvedBy,
            completed=completed,
            time=datetime.time,
            date=datetime.date.today()

        )

        return order


class moneyOrder(models.Model):
    orderAmount = models.IntegerField(default=0)
    orderCreatedBy = models.EmailField(max_length=60)
    orderApprovedBy = models.EmailField(max_length=60, default='notdoneyet@gmail.com')
    orderCouponCode = models.CharField(max_length=30, default='00')
    orderStatus = models.BooleanField(default=False)
    orderMode = models.CharField(max_length=30, default='NONE')
    orderRemark = models.CharField(max_length=60, default='InProgress')
    date = models.DateField(auto_now_add=True, auto_now=False)
    time = models.TimeField(auto_now_add=True, auto_now=False)
    isApproved = models.BooleanField(default=False)
    From = models.CharField(max_length=60, default='NULL')
    type = models.CharField(max_length=60, default='CREDIT')

    def __str__(self):
        return str(
            self.orderCreatedBy + " | " + str(
                self.orderAmount) + " | " + self.From + " | " + self.type + " | " + self.orderApprovedBy)

    @classmethod
    def create(cls, orderAmount, orderCreatedBy, orderApprovedby, orderCouponCode, orderMode, From, Type,
               IsApproved=False, OrderStatus=False):
        moneyorder = cls(
            orderAmount=orderAmount,
            orderCreatedBy=orderCreatedBy,
            time=datetime.time,
            date=datetime.date.today(),
            orderApprovedBy=orderApprovedby,
            orderCouponCode=orderCouponCode,
            orderMode=orderMode,
            From=From,
            type=Type,
            isApproved=IsApproved,
            orderStatus=OrderStatus,
        )

        return moneyorder
