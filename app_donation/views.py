from django.contrib import messages
from django.forms.models import inlineformset_factory
from users_auth.models import Profile
from django.shortcuts import redirect, render
from django.db.models.query_utils import Q
from .forms import DonationForm, MaterialForm, SearchRCForm, CustomerServiceForm
from .models import CustomerService, Donation, Material

# Create your views here.
def search_rc(request):
    result = None

    if request.method == "POST":
        if len(request.POST['search']) >= 3:
            search = Q(
                Q(profile_type__exact='R') &
                Q(code__exact=request.POST['search'])
                # Falta razao social. Criar entidade RecycleCenter
            )
            result = Profile.objects.filter(search)

        else:
            messages.info(request, "Digite no mínimo 3 caracteres")

    search_rc_form = SearchRCForm()
    
    content = {
        'search_rc_form': search_rc_form,
        'result': result
    }
    return render(request, 'search_rc.html', content)


def customer_service(request, id):
    profile = Profile.objects.get(id=id)
    
    if request.POST:
        post = request.POST.copy()
        post['requester'] = request.user
        post['recipient'] = profile
        post['address'] = 'Rua das Estrelas, nº 3131 - Centro, Fortaleza-CE'
        post['status_service'] = CustomerService.STATUS_SERVICE_CHOICES[0][0]
        post['confirmed'] = False
        post['return_recipient'] = ''
        post['points_service'] = 0
        post['modification_date'] = None
        post['tagged'] = True
        request.POST = post

        ca_form = CustomerServiceForm(request.POST)
        print(ca_form)
        print(ca_form.is_valid())
        if ca_form.is_valid():
            ca_form.save()
            return redirect('app_donation:search_rc')

    ca_form = CustomerServiceForm()
    content = {
        'ca_form': ca_form,
        'profile': profile,
    }
    return render(request, 'customer_service.html', content)


def confirm_ca(request, id):
    ca = CustomerService.objects.get(id=id)
    ca_form = CustomerServiceForm(request.POST or None, instance=ca)

    if request.POST:
        print(request.POST['confirmed'], type(request.POST['confirmed']))
        
        if bool(request.POST['confirmed']) == True:
            ca.confirmed = True
            ca.status_service = CustomerService.STATUS_SERVICE_CHOICES[1][0]
        
        elif bool(request.POST['confirmed']) == False:
            ca.confirmed = True
            ca.status_service = CustomerService.STATUS_SERVICE_CHOICES[3][0]
        
        ca.save(force_update=True)

        return redirect("users_auth:userpage")

    return render(request, 'confirm_ca.html', {'ca': ca, 'ca_form': ca_form})


def donation(request, id):
    ca = CustomerService.objects.get(id=id)

    if request.POST:
        post = request.POST.copy()
        post['customerService'] = ca
        post['confirmed'] = False
        post['status_donation'] = Donation.STATUS_DONATION_CHOICES[1][0]
        request.POST = post

        donation_form = DonationForm(request.POST)
        materials_form_factory = inlineformset_factory(Donation, Material, form=MaterialForm)
        materials_form = materials_form_factory(request.POST)
        print(donation_form.is_valid(), materials_form.is_valid())
        if donation_form.is_valid() and materials_form.is_valid():

            ca.status_service = CustomerService.STATUS_SERVICE_CHOICES[2][0]
            ca.save(force_update=True)

            donation = donation_form.save()
            materials_form.instance = donation
            materials_form.save()

            return redirect('users_auth:userpage')

    donation_form = DonationForm()
    materials_form_factory = inlineformset_factory(Donation, Material, form=MaterialForm, extra=3)
    materials_form = materials_form_factory()

    content = {
        'ca': ca,
        'donation_form': donation_form,
        'materials_form': materials_form
    }
    return render(request, 'donation.html', content)


def confirm_donation(request, id):
    ca = CustomerService.objects.get(id=id)
    donation = Donation.objects.get(customerService=ca.id)
    materials = Material.objects.filter(donation=donation.id)

    donation_form = DonationForm(request.POST or None, instance=donation)

    if request.POST:
        if bool(request.POST['confirmed']) == True:
            donation.confirmed = True
            donation.status_donation = Donation.STATUS_DONATION_CHOICES[0][0]
            ca.status_service = CustomerService.STATUS_SERVICE_CHOICES[4][0]
        
        elif bool(request.POST['confirmed']) == False:
            donation.confirmed = False
            donation.status_donation = Donation.STATUS_DONATION_CHOICES[2][0]
            ca.status_service = CustomerService.STATUS_SERVICE_CHOICES[3][0]

        donation.save()
        ca.save()
        return redirect('users_auth:userpage')

        

    content = {
        'ca': ca,
        'materials': materials,
        'donation_form': donation_form
    }

    return render(request, 'confirm_donation.html', content)
