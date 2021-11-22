from users_auth.models import Coupon, Donor, Profile
from app_donation.models import CustomerService, Donation
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from ..forms import CouponForm, DNCreationForm, LoginForm
from datetime import datetime
from django.db.models.query_utils import Q
from threading import Thread
from time import sleep
from datetime import date, datetime, timedelta
import random
import string

global hh
hh = None

# DN
def user_type(login_url=None):
    return user_passes_test(lambda u: u.profile_type == 'D', login_url=login_url)


@login_required(login_url='users_auth:login_dn')
@user_type(login_url="users_auth:login_dn")
def userpage(request):
    cs = CustomerService.objects.filter(requester=request.user.id).order_by("-id")
    if cs.count() == 0:
        content = {
            'success_donation': 0, 
            'all_donations': 0
        }
        return render(request, 'authenticated_user/donor/userpage.html', content)

    calls = []
    for call in cs:
        try:
            donation = Donation.objects.get(customerService=call)
            calls.append({'call': call, 'donation': donation})
        except:
            calls.append({'call': call, 'donation': None})
        
        search = Q(
            Q(requester=request.user.id)&
            Q(status_service = '4')
        )
        success_donation = CustomerService.objects.filter(search).count()

        search =  Q(requester=request.user.id)
        all_donations = CustomerService.objects.filter(search).count()

        content = {
            'calls': calls,
            'success_donation': success_donation, 
            'all_donations': all_donations
        }
        
    return render(request, 'authenticated_user/donor/userpage.html', content)


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
        #print(post['code']) #Teste

        post['username'] = post['code']
        #post['first_name'] = None
        #post['last_name'] = None
        post['profile_type'] = Profile.PROFILE_TYPE_CHOICES[0][0]
        request.POST = post

        dn_form = DNCreationForm(request.POST)

        #print(dn_form.is_valid()) #Teste
        if dn_form.is_valid():
            dn_form.save()          
            return redirect('users_auth:login_dn')
                
    dn_form = DNCreationForm()
    content = {
        'dn_form': dn_form
    }
    return render(request, 'management_user/register/register_dn.html', content)


def my_donations(request):
    cs = CustomerService.objects.filter(requester=request.user.id).order_by("-id")
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

    return render(request, 'authenticated_user/donor/my_donations.html', content)


@login_required(login_url='users_auth:login_dn')
@user_type(login_url="users_auth:login_dn")
def ranking(request):

    if request.user.donor.ranking_points == 0:
        messages.info(request, 'Faça uma doação para participar do ranking')
        return redirect('users_auth:userpage_dn')
        #return HttpResponse('<h1>Faça uma doação para participar do ranking</h1>') # page temporária
    
    ranking = Donor.objects.filter().order_by('-ranking_points').exclude(ranking_points=0)
    
    amount = list(range(1,len(ranking)+1))

    r = []
    
    for p, donor in zip(amount, ranking):
        #print(f'#{p} {donor.first_name} {donor.last_name} - {donor.ranking_points}')
        r.append([str(p), donor])
    
    #for donor in r:
    #    print(donor[0], donor[1].first_name)
    content = {
        'ranking': ranking,
        'amount': amount,
        'r': r,
        'hh': hh
    } 
    
    return render(request, 'authenticated_user/donor/ranking.html', content)


def encerrar_ranking():
    global hh
    while True:
        hh = datetime.now().time().strftime('%H:%M')
        if date.today().weekday() == 0 and hh >= '19:30':
            donors = Donor.objects.all()
            for donor in donors:
                hh += ' a'
                if donor.ranking_points != 0:
                    donor.general_points += donor.ranking_points
                    donor.ranking_points = 0
                    donor.save()
        sleep(1) 

"""-------------------"""

func = Thread(target=encerrar_ranking)
func.daemon = True
func.start()


@login_required(login_url='users_auth:login_dn')
@user_type(login_url="users_auth:login_dn")
def coupons_page(request):
    donor = Donor.objects.get(profile_ptr=request.user)

    coupon_form = CouponForm()
     #print(type(donor.general_points))
    
    if request.POST:
        if float(request.POST['value'])*10 <= donor.general_points:     
        
            post = request.POST.copy()
            post['donor_id'] = donor

            post['pass_key'] = ''
            for x in range(0,3):
                post['pass_key'] += random.choice(string.ascii_letters)
            post['pass_key'] += '-'+str(post['value'])
            post['expiration_date'] = str(date.today() + timedelta(days=3)) + ' ' + str(datetime.now().time())
            post['situation'] = 'A'
            request.POST = post
            

            coupon_form = CouponForm(request.POST)
            if coupon_form.is_valid():
                coupon_form.save()
                donor.general_points = donor.general_points - float(request.POST['value'])*10
                print(float(request.POST['value'])*10)
                donor.save()
                messages.info(request, "Cupom criado!")
                return redirect('users_auth:coupons')
        else:
            messages.info(request, "Pontos necesário para criar cupom maior que pontuação geral!")
            return redirect('users_auth:coupons')

    # Buscar disponíveis
    search = Q(
            Q(donor_id = donor)&
            Q(situation = 'A')&
            Q(used = False)
        )
    available_coupons = Coupon.objects.filter(search).order_by('-id')
    if available_coupons.count() == 0:
        available_coupons = None 
    
    # Buscar já utilizados
    search = Q(
            Q(donor_id = donor)&
            Q(situation = 'U')&
            Q(used = True)
        )
        
    used_coupons = Coupon.objects.filter(search)
    if used_coupons.count() == 0:
        used_coupons = None 

    # Buscar expirados
    search = Q(
            Q(donor_id = donor)&
            Q(situation = 'E')
        )
    expired_coupons = Coupon.objects.filter(search)
    if expired_coupons.count() == 0:
        expired_coupons = None 

    coupons = Coupon.objects.filter(search).order_by('-id')
    if coupons.count() == 0:
        coupons = None 
    
    content ={
        'current_points': donor.general_points,
        'coupon_form': coupon_form,
        'available_coupons': available_coupons,
        'used_coupons': used_coupons,
        'expired_coupons': expired_coupons,
    }
    
    return render(request, 'authenticated_user/donor/coupons.html', content)


def remove_coupon(request, id):
    coupon = Coupon.objects.get(id=id)
    donor = Donor.objects.get(profile_ptr=request.user)
    donor.general_points = donor.general_points + float(coupon.value * 10)
    donor.save()
    coupon.delete()
    messages.info(request, f"Cupom removido! {coupon.value*10} pontos recuperados")
    return redirect('users_auth:coupons')

