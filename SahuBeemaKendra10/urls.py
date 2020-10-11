from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

# from .views import home_screen_views
from SahuBeemaKendra10.views import (
    home_view,
    contactus,
    termsandconditions,
    privacypolicy,
)
from account.views import (
    registration_view,
    logout_view,
    login_view,
    account_view,
    getKycied,

)

from branch.views import (
    branchHome,
    confirmOrder,
    orderPlaced,
    wallet,
    addmoney,
    addMoneySuccessfull,
    moneyOrderNotSuccessFull,
    wrongCouponCode,
    allOrdersBranch,
    addMoneyPre,
    myAllAddMoney,
    mybranchEarnings,
    nobill,
    referNEarn,
)

from manager.views import (
    managerHome,
    moneyOrdersView,
    invalidMoneyOrderDetails,
    allOrdersManager,
    invalidpremiumOrderDetails,
    allMoneyOrdersManager,

)

urlpatterns = [
    # Admin Url's
    path('admin/', admin.site.urls),

    # Branch Url's
    path('branchHome', branchHome, name='branchHome'),
    path('orderPlaced', orderPlaced, name='orderPlaced'),
    path('wallet', wallet, name='wallet'),
    path('addmoney', addmoney, name='addmoney'),
    path('addmoneysuccessfull', addMoneySuccessfull, name='addmoneysuccessfull'),
    path('moneyodernotsuccess', moneyOrderNotSuccessFull, name='moneyordernotsuccessfull'),
    path('wrongcouponcode', wrongCouponCode, name='wrongcouponcode'),
    path('allordersbranch', allOrdersBranch, name='allordersbranch'),
    path('addmoneypre', addMoneyPre, name='addmoneypre'),
    path('transactions', myAllAddMoney, name='myalladddmoney'),
    path('mybranchearnings', mybranchEarnings, name='mybranchearnings'),
    path('nobill', nobill, name='nobill'),
    path('refernearn', referNEarn, name='refernearn'),


    # Manager Url's
    path('managerHome', managerHome, name='managerHome'),
    path('allmoneyordersmanager', allMoneyOrdersManager, name='allmoneyordersmanager'),
    path('allordersmanager', allOrdersManager, name='allordersmanager'),
    path('moneyorders', moneyOrdersView, name='moneyorders'),
    path('invalidmoneyorderdetails', invalidMoneyOrderDetails, name='invalidmoneyorderdetails'),
    path('invalidpremiumorderdetails', invalidpremiumOrderDetails, name='invalidpremiumorderdetails'),

    # Common Url's
    path('getkyc', getKycied, name='getkyc'),
    path('', home_view, name='home'),
    path('contactus', contactus, name='contactus'),
    path('termandconditions', termsandconditions, name='termandconditions'),
    path('privacypolicy', privacypolicy, name='privacypolicy'),


    # Django Accounts Url's
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),

    path('account/', account_view, name='account'),
    path('confirmOrder/<slug:policyNumber>', confirmOrder, name='confirmOrder'),

    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
         name='password_change'),

    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_change.html'),
         name='password_reset_confirm'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
]
