from users_auth.models import Donor, Profile
from app_donation.models import CustomerService, Donation
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http.response import HttpResponse
from ..forms import DNCreationForm, LoginForm
from datetime import datetime


# DN
def user_type(login_url=None):
    return user_passes_test(lambda u: u.profile_type == 'D', login_url=login_url)


@login_required(login_url='users_auth:login_dn')
@user_type(login_url="users_auth:login_dn")
def userpage(request):
    cs = CustomerService.objects.filter(requester=request.user.id).order_by("-id")
    calls = []
    for call in cs:
        try:
            donation = Donation.objects.get(customerService=call)
            calls.append({'call': call, 'donation': donation})
        except:
            calls.append({'call': call, 'donation': None})
            
    return render(request, 'authenticated_user/donor/userpage.html', {'calls': calls})


def login_dn(request):
    if request.POST:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(request, username=cd['user'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('users_auth:userpage_dn')
            else:
                messages.info(request, 'Usuário ou senha inválido')
                return redirect('users_auth:login_dn')
                #return HttpResponse("<h1>Não foi feito login</h1>")
    login_form = LoginForm()
    content = {
        'login_form': login_form
    }
    return render(request, 'management_user/login/login_dn.html', content)


@login_required(login_url='users_auth:login_dn')
@user_type(login_url="users_auth:login_dn")
def logout_dn(request):
    logout(request)
    return redirect('users_auth:login_dn')


def register(request):
    if request.POST:
        
        post = request.POST.copy()
        prefix = 'D' + str(datetime.today().strftime('%Y%m%d'))[2:]
        sufix = str(Profile.objects.filter(code__contains=prefix).count()+1)
        while True:
            if len(sufix) == 4:
                break
            sufix = '0'+sufix
        post['code'] = prefix + sufix
        print(post['code']) #Teste

        post['username'] = post['code']
        #post['first_name'] = None
        #post['last_name'] = None
        post['profile_type'] = Profile.PROFILE_TYPE_CHOICES[0][0]
        request.POST = post

        dn_form = DNCreationForm(request.POST)

        print(dn_form.is_valid()) #Teste
        if dn_form.is_valid():
            dn_form.save()          
            return redirect('users_auth:login_dn')
                
    dn_form = DNCreationForm()
    content = {
        'dn_form': dn_form
    }
    return render(request, 'management_user/register/register_dn.html', content)


@login_required(login_url='users_auth:login_dn')
@user_type(login_url="users_auth:login_dn")
def ranking(request):

    if request.user.donor.ranking_points == 0:
        return HttpResponse('<h1>Faça uma doação para participar do ranking</h1>') # page temporária
    
    ranking = Donor.objects.filter().order_by('-ranking_points').exclude(ranking_points=0)
    
    amount = list(range(1,len(ranking)+1))

    r = []
    
    for p, donor in zip(amount, ranking):
        #print(f'#{p} {donor.first_name} {donor.last_name} - {donor.ranking_points}')
        r.append([str(p), donor])
    
    for donor in r:
        print(donor[0], donor[1].first_name)
    content = {
        'ranking': ranking,
        'amount': amount,
        'r': r
    } 
    
    return render(request, 'authenticated_user/donor/ranking.html', content)