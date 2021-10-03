from users_auth.models import Profile
from app_donation.models import CustomerService, Donation
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from ..forms import AddressForm, LoginForm, RCCreationForm
from django.contrib import messages
from datetime import datetime


# RC
def user_type(login_url=None):
    return user_passes_test(lambda u: u.profile_type == 'R', login_url=login_url)


@login_required(login_url='users_auth:login_rc')
@user_type(login_url="users_auth:login_rc")
def userpage(request):
    cs = CustomerService.objects.filter(recipient=request.user.id).order_by("-id")
    
    calls = []
    for call in cs:
        try:
            donation = Donation.objects.get(customerService=call)
            calls.append({'call': call, 'donation': donation})
        except:
            calls.append({'call': call, 'donation': None})
    
    content = {
        'calls': calls
    }
    print(calls)
    return render(request, 'authenticated_user/recyclingcenter/userpage.html', content)


def login_rc(request):
    if request.POST:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(request, username=cd['user'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('users_auth:userpage_rc')
            else:
                messages.info(request, 'Usuário ou senha inválido')
                return redirect('users_auth:login_rc')
                #return HttpResponse("<h1>Não foi feito login</h1>")
    login_form = LoginForm()
    content = {
        'login_form': login_form
    }
    return render(request, 'management_user/login/login_rc.html', content)


@login_required(login_url='users_auth:login_rc')
@user_type(login_url="users_auth:login_rc")
def logout_rc(request):
    logout(request)
    return redirect('users_auth:login_rc')


def register(request):
    if request.POST:
        
        post = request.POST.copy()
        prefix = 'R' + str(datetime.today().strftime('%Y%m%d'))[2:]
        sufix = str(Profile.objects.filter(code__contains=prefix).count()+1)
        while True:
            if len(sufix) == 4:
                break
            sufix = '0'+sufix
        post['code'] = prefix + sufix
        print(post['code']) #Teste

        post['address'] = None
        post['username'] = post['code']
        post['first_name'] = None
        post['last_name'] = None
        post['profile_type'] = Profile.PROFILE_TYPE_CHOICES[1][0]
        request.POST = post

        rc_form = RCCreationForm(request.POST)
        address_form = AddressForm(request.POST)

        print(rc_form.is_valid(), address_form.is_valid()) #Teste

        if rc_form.is_valid() and address_form.is_valid():
            address = address_form.save()
            rc = rc_form.save(commit=False)
            rc.address = address
            rc.save()
                        
            return redirect('users_auth:login_rc')
                
    rc_form = RCCreationForm()
    address_form = AddressForm()
    content = {
        'rc_form': rc_form,
        'address_form': address_form
    }
    return render(request, 'management_user/register/register_rc.html', content)