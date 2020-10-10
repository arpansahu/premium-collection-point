import random
import string

from django.shortcuts import render, redirect
from order.models import moneyOrder, Order
from account.models import Account
import datetime
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.

def generateCouponCode(amount):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(20))
    return result_str + str(amount)


def allMoneyOrdersManager(request):
    if request.user.is_authenticated:
        if request.user.is_kycied:
            if not request.user.is_staff:
                return redirect('branchHome')

            if request.POST:
                datefrom = request.POST['dateFrom']
                dateto = request.POST['dateTo']
                print(datetime.date.today())
                print(datefrom, dateto)

                allordersobjects0 = moneyOrder.objects.filter(orderApprovedBy=request.user.email, type="CREDIT")
                allordersobjects = allordersobjects0.filter(date__range=
                                                            [datefrom, dateto]).order_by('date', 'time')

                ordersarray = []

                for i in allordersobjects:
                    orderlist = {}

                    orderlist['id'] = i.id
                    orderlist['orderCreatedBy'] = i.orderCreatedBy
                    # orderlist['orderApprovedBy'] = i.orderApprovedBy
                    orderlist['orderAmount'] = i.orderAmount
                    orderlist['orderDate'] = i.date
                    orderlist['orderTime'] = i.time
                    orderlist['orderMode'] = i.orderMode
                    orderlist['From'] = i.From
                    orderlist['orderStatus'] = i.orderStatus
                    orderlist['orderRemark'] = i.orderRemark
                    orderlist['orderCouponCode'] = i.orderCouponCode
                    orderlist['isApproved'] = i.isApproved

                    ordersarray.append(orderlist)

                return render(request, 'manager/allMoneyOrdersmanager.html', {'allorders': ordersarray})

            ordersOfBranchI0 = moneyOrder.objects.filter(orderApprovedBy=request.user.email, type="CREDIT")
            ordersOfBranchI = ordersOfBranchI0.filter(date=datetime.date.today()).order_by('time')

            ordersarray = []

            for i in ordersOfBranchI:
                orderlist = {}

                orderlist['id'] = i.id
                orderlist['orderCreatedBy'] = i.orderCreatedBy
                # orderlist['orderApprovedBy'] = i.orderApprovedBy
                orderlist['orderAmount'] = i.orderAmount
                orderlist['orderDate'] = i.date
                orderlist['orderTime'] = i.time
                orderlist['orderMode'] = i.orderMode
                orderlist['From'] = i.From
                orderlist['orderStatus'] = i.orderStatus
                orderlist['orderRemark'] = i.orderRemark
                orderlist['orderCouponCode'] = i.orderCouponCode
                orderlist['isApproved'] = i.isApproved

                ordersarray.append(orderlist)

            return render(request, 'manager/allMoneyOrdersmanager.html', {'allorders': ordersarray})
        else:
            return redirect('getkyc')
    return redirect('login')


def allOrdersManager(request):
    if request.user.is_authenticated:
        if request.user.is_kycied:
            if not request.user.is_staff:
                return redirect('branchHome')

            if request.POST:
                datefrom = request.POST['dateFrom']
                dateto = request.POST['dateTo']
                print(datetime.date.today())
                print(datefrom, dateto)

                allorderslist = []

                allordersobjects0 = Order.objects.filter(approvedBy=request.user.email)
                allordersobjects = allordersobjects0.filter(date__range=
                                                            [datefrom, dateto]).order_by('date', 'time')

                for j in allordersobjects:
                    temporder = {}

                    temporder['id'] = j.id
                    temporder['policyNumber'] = j.policyNumber
                    temporder['policyHolder'] = j.policyHolderName
                    temporder['amount'] = j.amount
                    temporder['Due'] = j.dueDate
                    temporder['createdBy'] = j.createdBy
                    temporder['completed'] = j.completed

                    allorderslist.append(temporder)

                return render(request, 'manager/allOrdersManager.html', {'allorders': allorderslist})

            allOrdersOfCurrentManager = []

            ordersOfBranchI0 = Order.objects.filter(approvedBy=request.user.email)
            ordersOfBranchI = ordersOfBranchI0.filter(date=datetime.date.today()).order_by('time')
            for j in ordersOfBranchI:
                temporders = {}

                temporders['id'] = j.id
                temporders['policyNumber'] = j.policyNumber
                temporders['policyHolder'] = j.policyHolderName
                temporders['amount'] = j.amount
                temporders['Due'] = j.dueDate
                temporders['createdBy'] = j.createdBy
                temporders['completed'] = j.completed

                allOrdersOfCurrentManager.append(temporders)

            return render(request, 'manager/allOrdersManager.html', {'allorders': allOrdersOfCurrentManager})
        else:
            return redirect('getkyc')
    return redirect('login')


def invalidMoneyOrderDetails(request):
    return render(request, 'manager/invalidMoneyOrderDetails.html')


def invalidpremiumOrderDetails(request):
    return render(request, 'manager/invalidPremiumOrderDetails.html')


def managerHome(request):
    if request.user.is_authenticated:
        if request.user.is_kycied:
            #if not request.is_secure():
            #    return HttpResponseRedirect('https://www.premiumcollectionpoint.com')
            if not request.user.is_staff:
                return redirect('branchHome')
            if request.POST:
                try:
                    orderid = request.POST['orderId']

                    order = Order.objects.filter(id=orderid).first()
                    order.completed = True
                    order.save()
                    moneyOrder.create(order.amount, order.createdBy, request.user.email,
                                      generateCouponCode(order.amount), 'PREMIUM',
                                      order.policyNumber, "DEBIT", True, True).save()

                    return redirect('managerHome')
                except:
                    return redirect('invalidpremiumorderdetails')

            allOrdersOfCurrentManager = []

            ordersOfBranchI0 = Order.objects.filter(approvedBy=request.user.email)
            ordersOfBranchI1 = ordersOfBranchI0.filter(date=datetime.date.today()).order_by('time')

            for j in ordersOfBranchI1:
                temporders = {}

                temporders['id'] = j.id
                temporders['policyNumber'] = j.policyNumber
                temporders['policyHolder'] = j.policyHolderName
                temporders['amount'] = j.amount
                temporders['Due'] = j.dueDate
                temporders['createdBy'] = j.createdBy
                temporders['completed'] = j.completed

                allOrdersOfCurrentManager.append(temporders)

            return render(request, 'manager/managerHome.html', {'allorders': allOrdersOfCurrentManager})
        else:
            return redirect('getkyc')
    return redirect('login')


def moneyOrdersView(request):
    if request.user.is_authenticated:
        if request.user.is_kycied:
            if not request.user.is_staff:
                return redirect('branchHome')
            if request.POST:

                transactionId = request.POST['transactionId']

                orderAction = request.POST['transactionAction']
                branchEmail = ''
                apprTrans = moneyOrder.objects.filter(id=transactionId, type="CREDIT")

                if apprTrans.count() == 0:
                    return redirect('')
                tranmode = ''
                tranfrom = ''
                amount = 0
                couponCode = ''

                for i in apprTrans:
                    amount = i.orderAmount
                    couponCode = i.orderCouponCode
                    tranfrom = i.From
                    tranmode = i.orderMode
                    branchEmail = i.orderCreatedBy

                if orderAction == "DECLINE":
                    if tranmode == "UPI":
                        subject = 'Money Order Declined'
                        message = 'Your Money order request with Amount: {0} has been declined due to incorrect ' \
                                  'information\nPlease Enter correct information while placing a money order ' \
                                  'request.\nNote: While filling FROM in UPI Transactions please enter your UPI ' \
                                  'instead of {1}' \
                                  'Address from which you are transferring money\nRegards ,\nPremium Collection Point ' \
                                  'Team'.format(amount, tranfrom)

                        email_from = settings.EMAIL_HOST_USER
                        recipient_list = [branchEmail, ]
                        send_mail(subject, message, email_from, recipient_list)

                    elif tranmode == "BankTransfer":
                        subject = 'Money Order Declined'
                        message = 'Your Money order request with Amount: {0} has been declined due to incorrect ' \
                                  'information\nPlease Enter correct information while placing a money order ' \
                                  'request.\nNote: While filling FROM in BankTransfer IMPS/NEFT/RTGS Transactions ' \
                                  'please enter transaction ref no instead of {1}, which you can check in your mobile ' \
                                  'banking ' \
                                  'app\nRegards ,\nPremium Collection Point Team'.format(amount, tranfrom)

                        email_from = settings.EMAIL_HOST_USER
                        recipient_list = [branchEmail, ]
                        send_mail(subject, message, email_from, recipient_list)

                    elif tranmode == "QR":
                        subject = 'Money Order Declined'
                        message = 'Your Money order request with Amount: {0} has been declined due to incorrect ' \
                                  'information\nPlease Enter correct information while placing a money order ' \
                                  'request.\nNote: While filling FROM in  QR Transactions ' \
                                  'please enter BANK ACCOUNT holders name instead of {1}, which you can check in your ' \
                                  'mobile banking ' \
                                  'app\nRegards ,\nPremium Collection Point Team'.format(amount, tranfrom)
                        email_from = settings.EMAIL_HOST_USER
                        recipient_list = [branchEmail, ]
                        send_mail(subject, message, email_from, recipient_list)

                    for i in apprTrans:
                        if not i.orderStatus:
                            apprTrans.delete()

                elif orderAction == "APPROVE":
                    subject = 'Money Order Details'
                    message = 'Amount: {0}\nTransaction Id: {1}\nCoupon Code: {2}'.format(amount, transactionId,
                                                                                          couponCode)
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [branchEmail, ]
                    send_mail(subject, message, email_from, recipient_list)

                    for i in apprTrans:
                        i.isApproved = True
                        i.save()

                return redirect('moneyorders')

            orders = moneyOrder.objects.filter(orderApprovedBy=request.user.email)
            orders = orders.filter(orderStatus=False, type="CREDIT")

            ordersarray = []

            for i in orders:
                orderlist = {}

                orderlist['id'] = i.id
                orderlist['orderCreatedBy'] = i.orderCreatedBy
                # orderlist['orderApprovedBy'] = i.orderApprovedBy
                orderlist['orderAmount'] = i.orderAmount
                orderlist['orderDate'] = i.date
                orderlist['orderTime'] = i.time
                orderlist['orderMode'] = i.orderMode
                orderlist['From'] = i.From
                orderlist['orderStatus'] = i.orderStatus
                orderlist['orderRemark'] = i.orderRemark
                orderlist['orderCouponCode'] = i.orderCouponCode
                orderlist['isApproved'] = i.isApproved

                ordersarray.append(orderlist)
                # print(orderlist)
            return render(request, 'manager/moneyorders.html', {'orderdlist': ordersarray})

        else:
            return redirect('getkyc')

    return redirect('login')
