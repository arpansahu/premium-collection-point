import time

from django.core.mail import send_mail
from selenium import webdriver

# for ubuntu
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import random
import string
from django.shortcuts import render, redirect

from SahuBeemaKendra10 import settings
from order.models import Order, Moneyorder
import datetime
import os
from account.models import Account
from django.http import HttpResponseRedirect

# Create your views here.

order_details = {}


def generate_coupon(amount):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(20))
    return result_str + str(amount)


def refer_n_earn(request):
    if request.user.is_authenticated:
        if request.user.is_kyc:
            if request.user.is_staff:
                return redirect('manager_home')

            if request.POST:
                full_name = request.POST['full_name']
                email_id = request.POST['email_id']
                mob_no = request.POST['mob_no']
                adhaar_number = request.POST['adhaar_number']
                pan = request.POST['pan']

                subject = 'Money Order Place By {0}'.format(request.user.email)
                message = 'Full Name: {0}\nEmail Id: {1}\nMob No: {2}\nAdhaar: {3}\nPan: {4}\nReferred By: {5}'.format(
                    full_name, email_id,
                    mob_no, adhaar_number, pan, request.user.email
                )
                email_from = settings.EMAIL_HOST_USER
                recipient_list = ['whatsapp.pcpoint@gmail.com', ]
                send_mail(subject, message, email_from, recipient_list)

                return render(request, 'branch/refer_success.html')

            return render(request, 'branch/refer_n_earn.html')
        else:
            return redirect('get_kyc')
    return redirect('login')


def my_branch_earnings_utility(request, date_from, date_to):
    my_earnings = 0

    orders = Order.objects.filter(created_by=request.user, completed=True, date__range=[date_from, date_to])

    for j in orders:
        my_earnings += j.amount
    # print("MYEarnings", my_earnings)
    return my_earnings * 0.005


def my_referral_earnings_utility(request, date_from, date_to):
    total_referral_earning = 0
    list_of_referral_earnings = []
    all_accounts_referred_by = Account.objects.filter(referred_by=request.user.email)
    for i in all_accounts_referred_by:
        orders = Order.objects.filter(created_by=i, completed=True, date__range=[date_from, date_to])
        branch_earning = 0
        for j in orders:
            branch_earning += j.amount
            # print(j.created_by, j.amount)
        # print(branch_earning)
        branch_earning *= 0.005
        branch_earning *= 0.1
        list_of_referral_earnings.append([i.email, branch_earning])
        total_referral_earning += branch_earning
    # print(list_of_referral_earnings)
    return [list_of_referral_earnings, total_referral_earning]


def my_branch_earnings(request):
    if request.user.is_authenticated:
        if request.user.is_kyc:
            if request.user.is_staff:
                return redirect('manager_home')

            if request.POST:
                date_from = request.POST['date_from']
                date_to = request.POST['date_to']

                my_earnings = my_branch_earnings_utility(request, date_from, date_to)
                temp = my_referral_earnings_utility(request, date_from, date_to)
                total_referral_earning = temp[1]
                list_of_referral_earnings = temp[0]
                return render(request, 'branch/my_branch_earnings.html',
                              {'referrals': list_of_referral_earnings, 'my_earnings': my_earnings,
                               'referral_earning': total_referral_earning,
                               'total': my_earnings + total_referral_earning})

            my_earnings = my_branch_earnings_utility(request, datetime.date.today().replace(day=1),
                                                     datetime.date.today())
            temp = my_referral_earnings_utility(request, datetime.date.today().replace(day=1), datetime.date.today())
            total_referral_earning = temp[1]
            list_of_referral_earnings = temp[0]

            return render(request, 'branch/my_branch_earnings.html',
                          {'referrals': list_of_referral_earnings, 'my_earnings': my_earnings,
                           'referral_earning': total_referral_earning, 'total': my_earnings + total_referral_earning})
        else:
            return redirect('get_kyc')
    return redirect('login')


def my_all_add_money(request):
    if request.user.is_authenticated:
        if request.user.is_kyc:
            if request.user.is_staff:
                return redirect('manager_home')
            total_amount = 0
            if request.POST:
                date_from = request.POST.get('date_from', datetime.date.today())
                date_to = request.POST.get('date_to', datetime.date.today())
                trans_type = request.POST.get('trans_type', 'ALL')

                all_orders = Moneyorder.objects.filter(order_created_by=request.user, order_type=2,
                                                       order_status=True,
                                                       date__range=[date_from, date_to]).order_by('date', 'time')
                if trans_type == "CREDIT":

                    for j in all_orders:
                        total_amount += j.order_amount


                elif trans_type == "DEBIT":

                    for j in all_orders:
                        total_amount += j.order_amount
                else:
                    for j in all_orders:
                        if j.order_type == 1:
                            total_amount += j.order_amount
                        if j.order_type == 2:
                            total_amount -= j.order_amount

                return render(request, 'branch/all_add_money.html',
                              {'all_orders': all_orders, 'total_amount': total_amount, 'date_from': date_from,
                               'date_to': date_to})

            all_orders = Moneyorder.objects.filter(order_created_by=request.user, order_status=True,
                                                   date=datetime.date.today()).order_by('time')

            for j in all_orders:
                if j.order_type == 1:
                    total_amount += j.order_amount
                if j.order_type == 2:
                    total_amount -= j.order_amount

            print(all_orders)
            return render(request, 'branch/all_add_money.html',
                          {'all_orders': all_orders, 'total_amount': total_amount,
                           'date_from': str(datetime.datetime.today()), 'date_to': str(datetime.datetime.today())})
        else:
            return redirect('get_kyc')
    return redirect('login')


def add_money_pre(request):
    if request.user.is_authenticated:
        if request.user.is_kyc:
            if request.user.is_staff:
                return redirect('manager_home')
            if request.POST:
                transaction_mode = int(request.POST['transaction_mode'])
                order_from = request.POST['from']
                amount = request.POST['amount']

                Moneyorder(order_amount=amount, order_created_by=request.user,
                           order_approved_by=request.user.supervisor,
                           order_coupon_code=generate_coupon(amount),
                           order_mode=transaction_mode,
                           From=order_from, order_type=1).save()

                subject = 'Money Order Place By {0}'.format(request.user.email)
                message = 'Amount: {0}\nFrom: {1}\nMode: {2}\nBranch: {3}'.format(
                    amount, order_from,
                    transaction_mode, request.user.email
                )
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.user.supervisor]
                send_mail(subject, message, email_from, recipient_list)
                return redirect('add_money')

            return render(request, 'branch/add_money_pre.html')
        else:
            return redirect('get_kyc')
    return redirect('login')


def all_orders_branch(request):
    if request.user.is_authenticated:
        if request.user.is_kyc:
            if request.user.is_staff:
                return redirect('manager_home')

            if request.POST:
                date_from = request.POST['date_from']
                date_to = request.POST['date_to']
                # print(datetime.date.today())
                # print(date_from, date_to)

                all_orders = Order.objects.filter(created_by=request.user, date__range=
                [date_from, date_to]).order_by('date', 'time')

                total_amount = 0
                for j in all_orders:
                    total_amount += j.amount

                return render(request, 'branch/all_orders_branch.html',
                              {'all_orders': all_orders, 'total_amount': total_amount})

            all_orders = Order.objects.filter(created_by=request.user, date=datetime.date.today()).order_by('time')

            total_amount = 0

            for j in all_orders:
                total_amount += j.amount

            return render(request, 'branch/all_orders_branch.html',
                          {'all_orders': all_orders, 'total_amount': total_amount})
        else:
            return redirect('get_kyc')
    return redirect('login')


def fetch_premium(policyNumber, created_by, count):
    # driver = webdriver.ChromiumEdge(r"C:\Users\Administrator\Desktop\awspcp\branch\msedgedriver.exe")

    # ubuntu
    chrome_options = Options()
    chrome_options.headless = False
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    # heroku
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")
    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    try:
        driver.get("https://www.amazon.in/hfc/bill/insurance?ref_=apay_deskhome_Insurance")
        elem = driver.find_element_by_id('a-autoid-1-announce')
        elem.click()
        elem = driver.find_element_by_id('INSURANCE_0')
        elem.click()

        time.sleep(1)
        policy_number = driver.find_element_by_xpath('//*[@id="Policy Number"]')
        policy_number.send_keys(str(policyNumber))
        time.sleep(1)

        email_id = driver.find_element_by_xpath('//*[@id="Email id"]')
        email_id.send_keys(str(created_by.email))
        time.sleep(1)

        driver.find_element_by_id('fetchBillActionId-announce').click()
        time.sleep(6)

        policy_holder_name = driver.find_element_by_xpath("//table/tbody/tr[2]/td[2]").text
        amount = driver.find_element_by_xpath("//table/tbody/tr[3]/td[2]").text
        due_date = driver.find_element_by_xpath("//table/tbody/tr[4]/td[2]").text

        temp = {}
        temp['policy_number'] = policyNumber
        temp['policy_holder_name'] = policy_holder_name
        temp['amount'] = amount
        # print(temp)
        raw_amount = ''
        for i in amount:
            if i in '1234567890.':
                raw_amount = raw_amount + i

        raw_amount = float(raw_amount)

        temp['raw_amount'] = raw_amount

        temp['due_date'] = due_date
        temp['created_by'] = created_by
        temp['status'] = False

        driver.quit()
        # return [policy_number, policy_holder_name, amount, raw_amount, due_date, created_by, False]
        order_details[policyNumber] = temp
        return 1
    except Exception as e:
        # print("Excep: ", e)
        order_details[policyNumber] = 'nobill'
        driver.quit()
        if count:
            fetch_premium(policyNumber, created_by, count - 1)
        return redirect('branch_home')


def confirm_order(request, policy_number=''):
    if request.user.is_authenticated:
        if request.user.is_kyc:
            try:
                my_order = order_details[policy_number]
                print(my_order)
                raw_amount = float(my_order['amount'].split(' ')[2])

            except:
                return redirect('branch_home')

            if request.user.is_staff:
                return redirect('manager_home')
            if request.POST:
                raw_amount = float(my_order['amount'].split(' ')[2])
                Order(policy_number=my_order['policy_number'], policy_holder_name=my_order['policy_holder_name'],
                      amount=raw_amount,
                      due_date=my_order['due_date'], created_by=my_order['created_by'],
                      approved_by=request.user.supervisor,
                      completed=my_order['status']).save()

                request.user.wallet_balance -= raw_amount

                # transaction update email
                subject = 'Transaction Alert {0}'.format(request.user.email)
                message = 'Amount: {0} have been deducted for Premium order with Policy Number: {1}\nRemaining balance is: {2}'.format(
                    order_details[policy_number]['amount'], order_details[policy_number]['policy_number'],
                    request.user.wallet_balance
                )
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.user.email, ]
                send_mail(subject, message, email_from, recipient_list)

                # email send
                subject = 'Premium Order Place By {0}'.format(request.user.email)
                message = 'PolicyNumber: {0}\nAccount Holder Name: {1}\nDue Date: {2}'.format(
                    order_details[policy_number]['policy_number'], order_details[policy_number]['policy_holder_name'],
                    order_details[policy_number]['amount']
                )
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.user.supervisor, ]
                send_mail(subject, message, email_from, recipient_list)

                request.user.save()
                try:
                    del order_details[policy_number]
                except:
                    pass

                return redirect('order_placed')

            return render(request, 'branch/confirm_order.html', {'my_order': my_order, 'raw_amount': raw_amount})
        else:
            return redirect('get_kyc')
    return redirect('login')


def order_placed(request):
    if request.user.is_authenticated:
        if request.user.is_kyc:
            if request.user.is_staff:
                return redirect('manager_home')
            return render(request, 'branch/order_placed.html')
        else:
            return redirect('get_kyc')

    return redirect('login')


def nobill(request):
    return render(request, 'branch/no_bill.html')


def branch_home(request):
    # print(order_details)
    if request.user.is_authenticated:
        if request.user.is_kyc:
            # if not request.is_secure():
            #    return HttpResponseRedirect('https://www.premiumcollectionpoint.com')
            if request.user.is_staff:
                return redirect('manager_home')

            if request.POST:
                policy_number = request.POST['policy_number']
                try:
                    del order_details[policy_number]
                except:
                    pass
                fetch_premium(policy_number, request.user, 2)
                if order_details[policy_number] == 'nobill':
                    return redirect('nobill')

                return redirect('confirm_order/{0}'.format(policy_number))

            all_orders = Order.objects.filter(created_by=request.user, date=datetime.date.today()).order_by('time')
            total_amount = 0
            for i in all_orders:
                total_amount += i.amount

            return render(request, 'branch/branch_home.html', {'all_orders': all_orders, 'total_amount': total_amount})
        else:
            return redirect('get_kyc')

    return redirect('login')


def wallet(request):
    if request.user.is_authenticated:
        if request.user.is_kyc:
            if request.user.is_staff:
                return redirect('manager_home')
            if request.POST:
                return redirect('add_money_pre')

            return render(request, 'branch/wallet.html')

        else:
            return redirect('get_kyc')
    return redirect('login')


def money_order_not_success(request):
    if request.user.is_authenticated:
        if request.user.is_kyc:
            if request.user.is_staff:
                return redirect('manager_home')
        else:
            return redirect('get_kyc')

        return render(request, 'branch/wrong_coupon.html')

    return redirect('login')


def add_money(request):
    if request.user.is_authenticated:
        if request.user.is_kyc:
            if request.user.is_staff:
                return redirect('manager_home')
            if request.POST:
                coupon_code = request.POST['coupon_code']
                transaction_id = int(request.POST['transaction_id'])
                # print("fecthedcoupon code: ", coupon_code, 'trndid: ', transaction_id)
                try:
                    moneyorder = Moneyorder.objects.get(id=transaction_id)
                except:
                    return redirect('money_order_not_success')

                # print(dataformoneyorder)
                print(request.user.email, moneyorder.order_created_by, coupon_code, moneyorder.order_coupon_code,
                      moneyorder.order_status, moneyorder.is_approved)

                if request.user.email == moneyorder.order_created_by.email and coupon_code == moneyorder.order_coupon_code \
                        and not moneyorder.order_status and moneyorder.is_approved and moneyorder.order_type == 1:

                    request.user.wallet_balance += moneyorder.order_amount
                    request.user.save()

                    moneyorder.order_status = True
                    moneyorder.order_remark = 'Successfull'
                    moneyorder.save()

                    return redirect('add_money_success')

                else:
                    return redirect('money_order_not_success')
            return render(request, 'branch/add_money.html')
        else:
            return redirect('get_kyc')

    return redirect('login')


def add_money_success(request):
    if request.user.is_authenticated:
        if request.user.is_kyc:
            if request.user.is_staff:
                return redirect('manager_home')
            return render(request, 'branch/add_money_success.html')
        return redirect('get_kyc')
    return redirect('login')


def wrong_coupon_code(request):
    if request.user.is_authenticated:
        if request.user.is_kyc:
            if request.user.is_staff:
                return redirect('manager_home')
            return render(request, 'branch/wrong_coupon.html')
        return redirect('get_kyc')
    return redirect('login')
