from app_donation.models import CustomerService
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse
from django.db.models.query_utils import Q
from .forms import LoginForm

# Create your views here.
def userpage(request):
    #search = Q()

    if request.user.profile_type == 'D':
        calls = CustomerService.objects.filter(requester=request.user.id)
        return render(request, 'userpage.html', {'calls': calls})
    elif request.user.profile_type == 'R':
        calls = CustomerService.objects.filter(recipient=request.user.id)
        return render(request, 'userpage_rc.html', {'calls': calls})

def login_profile(request):
    if request.POST:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(request, username=cd['user'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('users_auth:userpage')
            else:
                return HttpResponse("<h1>Não foi feito login</h1>")
    login_form = LoginForm()
    content = {
        'login_form': login_form
    }
    return render(request, 'login.html', content)


def logout_profile(request):
    logout(request)
    return redirect("users_auth:login")

