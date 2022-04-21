import random
import random
import string

from django.shortcuts import render, redirect
from order.models import Moneyorder, Order
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


def all_money_orders_manager(request):
    if request.user.is_authenticated:
        if request.user.is_kyc:
            if not request.user.is_staff:
                return redirect('branch_home')

            if request.POST:
                date_from = request.POST['date_from']
                date_to = request.POST['date_to']

                all_orders = Moneyorder.objects.filter(order_approved_by=request.user.email, order_type=1, date__range=
                                                            [date_from, date_to]).order_by('date', 'time')

                return render(request, 'manager/all_money_orders_manager.html', {'all_orders': all_orders})

            all_orders = Moneyorder.objects.filter(order_approved_by=request.user.email, order_type=1, date=datetime.date.today()).order_by('time')

            return render(request, 'manager/all_money_orders_manager.html', {'all_orders': all_orders})
        else:
            return redirect('get_kyc')
    return redirect('login')


def all_orders_manager(request):
    if request.user.is_authenticated:
        if request.user.is_kyc:
            if not request.user.is_staff:
                return redirect('branch_home')

            if request.POST:
                date_from = request.POST['date_from']
                date_to = request.POST['date_to']

                all_orders = Order.objects.filter(approved_by=request.user.email, date__range=
                [date_from, date_to]).order_by('date', 'time')

                return render(request, 'manager/all_orders_manager.html', {'all_orders': all_orders})

            all_orders = Order.objects.filter(approved_by=request.user.email, date=datetime.date.today()).order_by(
                'time')
            return render(request, 'manager/all_orders_manager.html', {'all_orders': all_orders})
        else:
            return redirect('get_kyc')
    return redirect('login')


def invalid_money_order_details(request):
    return render(request, 'manager/invalid_money_order_details.html')


def invalid_premium_order_details(request):
    return render(request, 'manager/invalid_premium_orders_details.html')


def manager_home(request):
    if request.user.is_authenticated:
        if request.user.is_kyc:
            # if not request.is_secure():
            #    return HttpResponseRedirect('https://www.premiumcollectionpoint.com')
            if not request.user.is_staff:
                return redirect('branch_home')
            if request.POST:
                try:
                    breakpoint()
                    orderid = request.POST['orderId']

                    order = Order.objects.filter(id=orderid).first()
                    order.completed = True
                    order.save()
                    Moneyorder(order_amount=order.amount, order_created_by=order.created_by,
                               order_approved_by=request.user.email,
                               order_coupon_code=generateCouponCode(order.amount),
                               order_remark='PREMIUM',
                               From=order.policy_number,
                               order_type=2, is_approved=True, order_status= True).save()

                    return redirect('manager_home')
                except:
                    return redirect('invalid_premium_order_details')

            orders_my_branch = Order.objects.filter(approved_by=request.user.email,
                                                    date=datetime.date.today()).order_by('time')

            return render(request, 'manager/manager_home.html', {'orders_my_branch': orders_my_branch})
        else:
            return redirect('get_kyc')
    return redirect('login')


def money_orders(request):
    if request.user.is_authenticated:
        if request.user.is_kyc:
            if not request.user.is_staff:
                return redirect('branch_home')
            if request.POST:
                transaction_id = request.POST['transaction_id']
                order_action = request.POST['transaction_action']
                breakpoint()
                # try:
                money_order = Moneyorder.objects.get(order_coupon_code=transaction_id, order_type=1)
                # except:
                #     return redirect('money_orders')

                amount = money_order.order_amount
                coupon_code = money_order.order_coupon_code
                tran_from = money_order.From
                tran_mode = money_order.order_mode
                # branch_email = money_order.order_created_by
                branch_email = 'arpanrocks95@gmail.com'

                if order_action == "DECLINE":
                    if tran_mode == 1:
                        subject = 'Money Order Declined'
                        message = 'Your Money order request with Amount: {0} has been declined due to incorrect ' \
                                  'information\nPlease Enter correct information while placing a money order ' \
                                  'request.\nNote: While filling FROM in UPI Transactions please enter your UPI ' \
                                  'instead of {1}' \
                                  'Address from which you are transferring money\nRegards ,\nPremium Collection Point ' \
                                  'Team'.format(amount, tran_from)

                        email_from = settings.EMAIL_HOST_USER
                        recipient_list = [branch_email, ]
                        send_mail(subject, message, email_from, recipient_list)

                    elif tran_mode == 2:
                        subject = 'Money Order Declined'
                        message = 'Your Money order request with Amount: {0} has been declined due to incorrect ' \
                                  'information\nPlease Enter correct information while placing a money order ' \
                                  'request.\nNote: While filling FROM in BankTransfer IMPS/NEFT/RTGS Transactions ' \
                                  'please enter transaction ref no instead of {1}, which you can check in your mobile ' \
                                  'banking ' \
                                  'app\nRegards ,\nPremium Collection Point Team'.format(amount, tran_from)

                        email_from = settings.EMAIL_HOST_USER
                        recipient_list = [branch_email, ]
                        send_mail(subject, message, email_from, recipient_list)

                    elif tran_mode == 3:
                        subject = 'Money Order Declined'
                        message = 'Your Money order request with Amount: {0} has been declined due to incorrect ' \
                                  'information\nPlease Enter correct information while placing a money order ' \
                                  'request.\nNote: While filling FROM in CASH Transactions ' \
                                  'please enter BANK ACCOUNT holders name instead of {1}, which you can check in your ' \
                                  'mobile banking ' \
                                  'app\nRegards ,\nPremium Collection Point Team'.format(amount, tran_from)
                        email_from = settings.EMAIL_HOST_USER
                        recipient_list = [branch_email, ]
                        send_mail(subject, message, email_from, recipient_list)

                    money_order.delete()

                elif order_action == "APPROVE":
                    subject = 'Money Order Details'
                    message = 'Amount: {0}\nTransaction Id: {1}\nCoupon Code: {2}'.format(money_order.order_amount,
                                                                                          money_order.id,
                                                                                          money_order.order_coupon_code)
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [branch_email, ]
                    send_mail(subject, message, email_from, recipient_list)

                    money_order.is_approved = True
                    money_order.save()

                return redirect('money_orders')

            orders = Moneyorder.objects.filter(order_approved_by=request.user.email, order_status=False, order_type=1)
            return render(request, 'manager/money_orders.html', {'orders': orders})

        else:
            return redirect('get_kyc')

    return redirect('login')
