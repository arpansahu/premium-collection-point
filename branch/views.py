import time

from django.core.mail import send_mail
from selenium import webdriver

#for ubuntu
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import random
import string
from django.shortcuts import render, redirect

from SahuBeemaKendra10 import settings
from order.models import Order, moneyOrder
import datetime
import os
from account.models import Account
from django.http import HttpResponseRedirect

# Create your views here.

orderDetails = {}


def getcopmpleted(completed):
    if completed:
        return 'Successfull'
    return 'InProgress'


def generateCouponCode(amount):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(20))
    return result_str + str(amount)


def referNEarn(request):
    if request.user.is_authenticated:
        if request.user.is_kycied:
            if request.user.is_staff:
                return redirect('managerHome')

            if request.POST:
                fullname = request.POST['fullname']
                emailid = request.POST['emailid']
                mobno = request.POST['mobno']
                adhaar = request.POST['adhaar']
                pan = request.POST['pan']

                subject = 'Money Order Place By {0}'.format(request.user.email)
                message = 'Full Name: {0}\nEmail Id: {1}\nMob No: {2}\nAdhaar: {3}\nPan: {4}\nReferred By: {5}'.format(
                    fullname, emailid,
                    mobno, adhaar, pan,request.user.email
                )
                email_from = settings.EMAIL_HOST_USER
                recipient_list = ['whatsapp.pcpoint@gmail.com', ]
                send_mail(subject, message, email_from, recipient_list)

                return render(request, 'branch/referSuccessfull.html')

            return render(request, 'branch/referNEarn.html')
        else:
            return redirect('getkyc')
    return redirect('login')


def mybranchearnings(request, datefrom, dateto):
    MyEarnings = 0

    ordersOfBranchI0 = Order.objects.filter(createdBy=request.user.email)
    ordersOfBranchI1 = ordersOfBranchI0.filter(completed=True)
    ordersOfBranchI2 = ordersOfBranchI1.filter(
        date__range=[datefrom, dateto])

    for j in ordersOfBranchI2:
        MyEarnings += j.amount
    # print("MYEarnings", MyEarnings)
    return MyEarnings * 0.005


def myreferralearnings(request, datefrom, dateto):
    TotalReferralEarning = 0
    listOFReferralEarnings = []
    allAccountsRefferdBY = Account.objects.filter(referredBy=request.user.email)
    for i in allAccountsRefferdBY:
        ordersOfBranchI0 = Order.objects.filter(createdBy=i.email)
        ordersOfBranchI1 = ordersOfBranchI0.filter(completed=True)
        ordersOfBranchI2 = ordersOfBranchI1.filter(
            date__range=[datefrom, dateto])
        thisbranchEarning = 0
        for j in ordersOfBranchI2:
            thisbranchEarning += j.amount
            # print(j.createdBy, j.amount)
        # print(thisbranchEarning)
        thisbranchEarning *= 0.005
        thisbranchEarning *= 0.1
        listOFReferralEarnings.append([i.email, thisbranchEarning])
        TotalReferralEarning += thisbranchEarning
    # print(listOFReferralEarnings)
    return [listOFReferralEarnings, TotalReferralEarning]


def mybranchEarnings(request):
    if request.user.is_authenticated:
        if request.user.is_kycied:
            if request.user.is_staff:
                return redirect('managerHome')

            if request.POST:
                dateFrom = request.POST['dateFrom']
                dateTo = request.POST['dateTo']

                MyEarnings = mybranchearnings(request, dateFrom, dateTo)
                temp = myreferralearnings(request, dateFrom, dateTo)
                TotalReferralEarning = temp[1]
                listOFReferralEarnings = temp[0]
                return render(request, 'branch/mybranchEarnings.html',
                              {'referrals': listOFReferralEarnings, 'myearnings': MyEarnings,
                               'referralearning': TotalReferralEarning, 'total': MyEarnings + TotalReferralEarning})

            MyEarnings = mybranchearnings(request, datetime.date.today().replace(day=1), datetime.date.today())
            temp = myreferralearnings(request, datetime.date.today().replace(day=1), datetime.date.today())
            TotalReferralEarning = temp[1]
            listOFReferralEarnings = temp[0]

            return render(request, 'branch/mybranchEarnings.html',
                          {'referrals': listOFReferralEarnings, 'myearnings': MyEarnings,
                           'referralearning': TotalReferralEarning, 'total': MyEarnings + TotalReferralEarning})
        else:
            return redirect('getkyc')
    return redirect('login')


def myAllAddMoney(request):
    if request.user.is_authenticated:
        if request.user.is_kycied:
            if request.user.is_staff:
                return redirect('managerHome')

            if request.POST:
                datefrom = request.POST['dateFrom']
                dateto = request.POST['dateTo']
                transType = request.POST['tranType']
                # print(datetime.date.today())
                # print(datefrom, dateto)

                if transType == "ALL":
                    allorderslist = []
                    allordersobjects0 = moneyOrder.objects.filter(orderCreatedBy=request.user.email)

                    allordersobjects1 = allordersobjects0.filter(orderStatus=True).order_by('date', 'time')

                    allordersobjects = allordersobjects1.filter(date__range=[datefrom, dateto])
                    count = 0
                    totalAmount = 0
                    for j in allordersobjects:
                        temporder = {}
                        count += 1
                        temporder['transid'] = count
                        temporder['Amount'] = j.orderAmount
                        temporder['Date'] = j.date
                        temporder['Time'] = j.time
                        temporder['Mode'] = j.orderMode
                        temporder['From'] = j.From
                        temporder['Remark'] = j.orderRemark
                        temporder['Type'] = j.type

                        allorderslist.append(temporder)

                        if j.type == "CREDIT":
                            totalAmount += j.orderAmount
                        if j.type == "DEBIT":
                            totalAmount -= j.orderAmount
                    return render(request, 'branch/myAllAddMoney.html',
                                  {'allorders': allorderslist, 'totalAmount': totalAmount})

                elif transType == "CREDIT":
                    allorderslist = []
                    allordersobjects0 = moneyOrder.objects.filter(orderCreatedBy=request.user.email, type="CREDIT")

                    allordersobjects1 = allordersobjects0.filter(orderStatus=True).order_by('date', 'time')

                    allordersobjects = allordersobjects1.filter(date__range=[datefrom, dateto])
                    count = 0
                    totalAmount = 0
                    for j in allordersobjects:
                        temporder = {}
                        count += 1
                        temporder['transid'] = count
                        temporder['Amount'] = j.orderAmount
                        temporder['Date'] = j.date
                        temporder['Time'] = j.time
                        temporder['Mode'] = j.orderMode
                        temporder['From'] = j.From
                        temporder['Remark'] = j.orderRemark
                        temporder['Type'] = j.type

                        allorderslist.append(temporder)
                        totalAmount += j.orderAmount
                    return render(request, 'branch/myAllAddMoney.html',
                                  {'allorders': allorderslist, 'totalAmount': totalAmount})

                elif transType == "DEBIT":
                    allorderslist = []
                    allordersobjects0 = moneyOrder.objects.filter(orderCreatedBy=request.user.email, type="DEBIT")

                    allordersobjects1 = allordersobjects0.filter(orderStatus=True).order_by('date', 'time')

                    allordersobjects = allordersobjects1.filter(date__range=[datefrom, dateto])
                    count = 0
                    totalAmount = 0
                    for j in allordersobjects:
                        temporder = {}
                        count += 1
                        temporder['transid'] = count
                        temporder['Amount'] = j.orderAmount
                        temporder['Date'] = j.date
                        temporder['Time'] = j.time
                        temporder['Mode'] = j.orderMode
                        temporder['From'] = j.From
                        temporder['Remark'] = j.orderRemark
                        temporder['Type'] = j.type

                        allorderslist.append(temporder)
                        totalAmount += j.orderAmount
                    return render(request, 'branch/myAllAddMoney.html',
                                  {'allorders': allorderslist, 'totalAmount': totalAmount})

            allOrdersOfCurrBranch = []

            ordersOfBranchI0 = moneyOrder.objects.filter(orderCreatedBy=request.user.email)
            ordersOfBranchI1 = ordersOfBranchI0.filter(orderStatus=True)
            ordersOfBranchI = ordersOfBranchI1.filter(date=datetime.date.today()).order_by('time')
            count = 0
            totalAmount = 0
            for j in ordersOfBranchI:
                temporders = {}
                count += 1
                temporders['transid'] = count
                temporders['Amount'] = j.orderAmount
                temporders['Date'] = j.date
                temporders['Time'] = j.time
                temporders['Mode'] = j.orderMode
                temporders['From'] = j.From
                temporders['Remark'] = j.orderRemark
                temporders['Type'] = j.type

                allOrdersOfCurrBranch.append(temporders)
                if j.type == "CREDIT":
                    totalAmount += j.orderAmount
                if j.type == "DEBIT":
                    totalAmount -= j.orderAmount

            return render(request, 'branch/myAllAddMoney.html',
                          {'allorders': allOrdersOfCurrBranch, 'totalAmount': totalAmount})
        else:
            return redirect('getkyc')
    return redirect('login')


def addMoneyPre(request):
    if request.user.is_authenticated:
        if request.user.is_kycied:
            if request.user.is_staff:
                return redirect('managerHome')
            if request.POST:
                tranMode = request.POST['tranMode']
                From = request.POST['from']
                amount = request.POST['amount']

                moneyOrder.create(amount, request.user.email, request.user.supervisor, generateCouponCode(amount),
                                  tranMode,
                                  From, "CREDIT").save()

                subject = 'Money Order Place By {0}'.format(request.user.email)
                message = 'Amount: {0}\nFrom: {1}\nMode: {2}\nBranch: {3}'.format(
                    amount, From,
                    tranMode, request.user.email
                )
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.user.supervisor, ]
                send_mail(subject, message, email_from, recipient_list)
                return redirect('addmoney')

            return render(request, 'branch/addmoneyPre.html')
        else:
            return redirect('getkyc')
    return redirect('login')


def allOrdersBranch(request):
    if request.user.is_authenticated:
        if request.user.is_kycied:
            if request.user.is_staff:
                return redirect('managerHome')

            if request.POST:
                datefrom = request.POST['dateFrom']
                dateto = request.POST['dateTo']
                # print(datetime.date.today())
                # print(datefrom, dateto)

                allorderslist = []

                allordersobjects0 = Order.objects.filter(createdBy=request.user.email)
                allordersobjects = allordersobjects0.filter(date__range=
                                                            [datefrom, dateto]).order_by('date', 'time')
                count = 0
                totalAmount = 0
                for j in allordersobjects:
                    temporder = {}
                    count += 1
                    temporder['id'] = count
                    temporder['policyNumber'] = j.policyNumber
                    temporder['policyHolder'] = j.policyHolderName
                    temporder['amount'] = j.amount
                    temporder['date'] = j.date
                    temporder['time'] = j.time
                    temporder['Due'] = j.dueDate
                    if j.completed:
                        temporder['completed'] = 'Successfull'
                    else:
                        temporder['completed'] = 'InProgress'

                    allorderslist.append(temporder)
                    totalAmount += j.amount

                return render(request, 'branch/allOrdersBranch.html',
                              {'allorders': allorderslist, 'totalAmount': totalAmount})

            allOrdersOfCurrBranch = []

            ordersOfBranchI0 = Order.objects.filter(createdBy=request.user.email)
            ordersOfBranchI = ordersOfBranchI0.filter(date=datetime.date.today()).order_by('time')
            count = 0
            totalAmount = 0
            for j in ordersOfBranchI:
                temporders = {}
                count += 1
                temporders['id'] = count
                temporders['policyNumber'] = j.policyNumber
                temporders['policyHolder'] = j.policyHolderName
                temporders['amount'] = j.amount
                temporders['date'] = j.date
                temporders['time'] = j.time
                temporders['Due'] = j.dueDate

                if j.completed:
                    temporders['completed'] = 'Successfull'
                else:
                    temporders['completed'] = 'InProgress'

                allOrdersOfCurrBranch.append(temporders)
                totalAmount += j.amount

            return render(request, 'branch/allOrdersBranch.html',
                          {'allorders': allOrdersOfCurrBranch, 'totalAmount': totalAmount})
        else:
            return redirect('getkyc')
    return redirect('login')


def fetchPremiumdetails(policyNumber, createdBy, count):
    #driver = webdriver.ChromiumEdge(r"C:\Users\Administrator\Desktop\awspcp\branch\msedgedriver.exe")
    
    #ubuntu
    chromeOptions = Options()
    chromeOptions.headless = False
    driver = webdriver.Chrome(executable_path="/home/arpansahu/Desktop/awspcp/branch/chromedriver", options=chromeOptions)
    #heroku 
    #chrome_options = webdriver.ChromeOptions()
    #chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    #chrome_options.add_argument("--headless")
    #chrome_options.add_argument("--disable-dev-shm-usage")
    #chrome_options.add_argument("--no-sandbox")
    #driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    try:
        driver.get("https://www.amazon.in/hfc/bill/insurance?ref_=apay_deskhome_Insurance")

        elem = driver.find_element_by_id('a-autoid-1-announce')
        elem.click()
        elem = driver.find_element_by_id('INSURANCE_0')
        elem.click()

        time.sleep(1)
        policnumber = driver.find_element_by_xpath('//*[@id="Policy Number"]')
        policnumber.send_keys(str(policyNumber))
        time.sleep(1)

        emailid = driver.find_element_by_xpath('//*[@id="Email id"]')
        emailid.send_keys(str(createdBy))
        time.sleep(1)

        driver.find_element_by_id('fetchBillActionId-announce').click()
        time.sleep(6)

        policyHolderName = driver.find_element_by_xpath("//table/tbody/tr[2]/td[2]").text
        amount = driver.find_element_by_xpath("//table/tbody/tr[3]/td[2]").text
        dueDate = driver.find_element_by_xpath("//table/tbody/tr[4]/td[2]").text

        temp = {}
        temp['policyNumber'] = policyNumber
        temp['policyHolderName'] = policyHolderName
        temp['amount'] = amount
        # print(temp)
        rawamount = ''
        for i in amount:
            if i in '1234567890.':
                rawamount = rawamount + i

        rawamount = float(rawamount)

        temp['rawamount'] = rawamount

        temp['dueDate'] = dueDate
        temp['createdBy'] = createdBy
        temp['status'] = False

        driver.quit()
        # return [policyNumber, policyHolderName, amount, rawamount, dueDate, createdBy, False]
        orderDetails[policyNumber] = temp
        return 1
    except Exception as e:
        # print("Excep: ", e)
        orderDetails[policyNumber] = 'nobill'
        driver.quit()
        if count:
            fetchPremiumdetails(policyNumber, createdBy, count - 1)
        return redirect('branchHome')


def confirmOrder(request, policyNumber=''):
    if request.user.is_authenticated:
        if request.user.is_kycied:
            try:
                myOrder = orderDetails[policyNumber]
            except:
                return redirect('branchHome')

            if request.user.is_staff:
                return redirect('managerHome')
            if request.POST:
                Order.create(myOrder['policyNumber'], myOrder['policyHolderName'],
                             myOrder['rawamount'],
                             myOrder['dueDate'], myOrder['createdBy'], request.user.supervisor,
                             myOrder['status']).save()

                request.user.walletBalance -= myOrder['rawamount']

                # transaction update email
                subject = 'Transaction Alert {0}'.format(request.user.email)
                message = 'Amount: {0} have been deducted for Premium order with Policy Number: {1}\nRemaining balance is: {2}'.format(
                    orderDetails[policyNumber]['amount'], orderDetails[policyNumber]['policyNumber'],
                    request.user.walletBalance
                )
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.user.email, ]
                send_mail(subject, message, email_from, recipient_list)

                # email send
                subject = 'Premium Order Place By {0}'.format(request.user.email)
                message = 'PolicyNumber: {0}\nAccount Holder Name: {1}\nDue Date: {2}'.format(
                    orderDetails[policyNumber]['policyNumber'], orderDetails[policyNumber]['policyHolderName'],
                    orderDetails[policyNumber]['amount']
                )
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.user.supervisor, ]
                send_mail(subject, message, email_from, recipient_list)

                request.user.save()
                try:
                    del orderDetails[policyNumber]
                except:
                    pass

                return redirect('orderPlaced')

            return render(request, 'branch/confirmorder.html', myOrder)
        else:
            return redirect('getkyc')
    return redirect('login')


def orderPlaced(request):
    if request.user.is_authenticated:
        if request.user.is_kycied:
            if request.user.is_staff:
                return redirect('managerHome')
            return render(request, 'branch/orderplaced.html')
        else:
            return redirect('getkyc')

    return redirect('login')


def nobill(request):
    return render(request, 'branch/nobill.html')


def branchHome(request):
    # print(orderDetails)
    if request.user.is_authenticated:
        if request.user.is_kycied:
            #if not request.is_secure():
            #    return HttpResponseRedirect('https://www.premiumcollectionpoint.com')
            if request.user.is_staff:
                return redirect('managerHome')

            if request.POST:
                policyNumber = request.POST['policyNumber']
                try:
                    del orderDetails[policyNumber]
                except:
                    pass
                fetchPremiumdetails(policyNumber, request.user.email, 2)
                if orderDetails[policyNumber] == 'nobill':
                    return redirect('nobill')

                return redirect('confirmOrder/{0}'.format(policyNumber))

            myOrder = Order.objects.filter(createdBy=str(request.user.email))
            myOrder2 = myOrder.filter(date=datetime.date.today()).order_by('time')
            array = []
            count = 1
            totalAmount = 0
            for i in myOrder2:
                # [count, i.policyNumber, i.policyHolderName, i.amount, i.dueDate, i.completed]
                array.append(
                    {'count': count, 'policyNumber': i.policyNumber, 'policyHolderName': i.policyHolderName,
                     'amount': i.amount,
                     'dueDate': i.dueDate, 'time': i.time, 'status': getcopmpleted(i.completed)})
                count = count + 1
                totalAmount += i.amount
            # print(array)

            return render(request, 'branch/branchHome.html', {'myOrders': array, 'totalAmount': totalAmount})

        else:
            return redirect('getkyc')

    return redirect('login')


def wallet(request):
    if request.user.is_authenticated:
        if request.user.is_kycied:
            if request.user.is_staff:
                return redirect('managerHome')
            if request.POST:
                return redirect('addmoneypre')

            return render(request, 'branch/wallet.html')

        else:
            return redirect('getkyc')
    return redirect('login')


def moneyOrderNotSuccessFull(request):
    if request.user.is_authenticated:
        if request.user.is_kycied:
            if request.user.is_staff:
                return redirect('managerHome')
        else:
            return redirect('getkyc')

        return render(request, 'branch/wrongCouponCode.html')

    return redirect('login')


def addmoney(request):
    if request.user.is_authenticated:
        if request.user.is_kycied:
            if request.user.is_staff:
                return redirect('managerHome')
            if request.POST:

                fetchedcouponCode = request.POST['couponCode']
                fetchTransId = request.POST['transId']
                # print("fecthedcoupon code: ", fetchedcouponCode, 'trndid: ', fetchTransId)
                try:
                    moneyorder = moneyOrder.objects.filter(id=fetchTransId).first()
                except:
                    return redirect('moneyordernotsuccessfull')

                if not moneyorder:
                    return redirect('moneyordernotsuccessfull')

                # print(dataformoneyorder)
                print(request.user.email, moneyorder.orderCreatedBy, fetchedcouponCode, moneyorder.orderCouponCode,
                      moneyorder.orderStatus, moneyorder.isApproved)

                if request.user.email == moneyorder.orderCreatedBy and fetchedcouponCode == moneyorder.orderCouponCode \
                        and not moneyorder.orderStatus and moneyorder.isApproved and moneyorder.type == "CREDIT":

                    request.user.walletBalance += moneyorder.orderAmount
                    request.user.save()

                    moneyorder.orderStatus = True
                    moneyorder.orderRemark = 'Successfull'
                    moneyorder.save()

                    return redirect('addmoneysuccessfull')

                else:
                    return redirect('moneyordernotsuccessfull')
            return render(request, 'branch/addmoney.html')
        else:
            return redirect('getkyc')

    return redirect('login')


def addMoneySuccessfull(request):
    if request.user.is_authenticated:
        if request.user.is_kycied:
            if request.user.is_staff:
                return redirect('managerHome')
            return render(request, 'branch/addmoneysuccessfull.html')
        return redirect('getkyc')
    return redirect('login')


def wrongCouponCode(request):
    if request.user.is_authenticated:
        if request.user.is_kycied:
            if request.user.is_staff:
                return redirect('managerHome')
            return render(request, 'branch/wrongCouponCode.html')
        return redirect('getkyc')
    return redirect('login')
