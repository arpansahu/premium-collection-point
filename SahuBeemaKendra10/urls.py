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
    get_kyc,

)

from branch.views import (
    branch_home,
    confirm_order,
    order_placed,
    wallet,
    add_money,
    add_money_success,
    money_order_not_success,
    wrong_coupon_code,
    all_orders_branch,
    add_money_pre,
    my_all_add_money,
    my_branch_earnings,
    nobill,
    refer_n_earn,
)

from manager.views import (
    manager_home,
    money_orders,
    invalid_money_order_details,
    all_orders_manager,
    invalid_premium_order_details,
    all_money_orders_manager,

)

urlpatterns = [
    # Admin Url's
    path('admin/', admin.site.urls),

    # Branch Url's
    path('branch-home', branch_home, name='branch_home'),
    path('order-placed', order_placed, name='order_placed'),
    path('wallet', wallet, name='wallet'),
    path('add_money', add_money, name='add_money'),
    path('add-money-success', add_money_success, name='add_money_success'),
    path('money-order-not-success', money_order_not_success, name='money_order_not_success'),
    path('wrong-coupon-code', wrong_coupon_code, name='wrong_coupon_code'),
    path('all-orders-branch', all_orders_branch, name='all_orders_branch'),
    path('add-money-pre', add_money_pre, name='add_money_pre'),
    path('transactions', my_all_add_money, name='myalladddmoney'),
    path('my-branch-earnings', my_branch_earnings, name='my_branch_earnings'),
    path('nobill', nobill, name='nobill'),
    path('refer-n-earn', refer_n_earn, name='refer_n_earn'),


    # Manager Url's
    path('manager_home', manager_home, name='manager_home'),
    path('all_money_orders_manager', all_money_orders_manager, name='all_money_orders_manager'),
    path('all_orders_manager', all_orders_manager, name='all_orders_manager'),
    path('money-orders', money_orders, name='money_orders'),
    path('invalid-money-order-details', invalid_money_order_details, name='invalid_money_order_details'),
    path('invalid-premium-order-details', invalid_premium_order_details, name='invalid_premium_order_details'),

    # Common Url's
    path('get-kyc', get_kyc, name='get_kyc'),
    path('', home_view, name='home'),
    path('contactus', contactus, name='contactus'),
    path('termandconditions', termsandconditions, name='termandconditions'),
    path('privacypolicy', privacypolicy, name='privacypolicy'),


    # Django Accounts Url's
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),

    path('account/', account_view, name='account'),
    path('confirm_order/<slug:policy_number>', confirm_order, name='confirm_order'),

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
