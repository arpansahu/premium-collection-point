from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.

'''
def home_screen_views(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return render(request, template_name='manager/managerHome.html')

        return render(request, template_name='branch/branchHome.html')

    return render(request, template_name='account/login.html')

'''


def home_view(request):
    #if not request.is_secure():
    #    return HttpResponseRedirect('https://www.premiumcollectionpoint.com')
    return render(request, 'Home.html')


