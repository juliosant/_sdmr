from django.contrib import messages
from django.forms.models import inlineformset_factory
from users_auth.models import Donor, Profile
from django.shortcuts import redirect, render
from django.db.models.query_utils import Q
from .forms import DonationForm, MaterialForm, SearchRCForm, CustomerServiceForm
from .models import CustomerService, Donation, Material

# Create your views here.
def search_rc(request):
    result = None
    count_result = None

    if request.method == "POST":
        if len(request.POST['search']) >= 3:
            search = Q(
                Q(profile_type__exact='R') &
                Q(code__contains=request.POST['search'])|
                Q(recyclingcenter__corporate_name__contains=request.POST['search'])
                # Falta razao social. Criar entidade RecycleCenter
            )
            result = Profile.objects.filter(search)
            count_result = result.count()

        else:
            messages.info(request, "Digite no mínimo 3 caracteres")

    search_rc_form = SearchRCForm()
    
    content = {
        'search_rc_form': search_rc_form,
        'result': result,
        'count_result': count_result
    }
    return render(request, 'donation_service/donor/search_rc.html', content)


def customer_service(request, id):
    profile = Profile.objects.get(id=id)
    
    if request.POST:
        post = request.POST.copy()
        post['requester'] = request.user
        post['recipient'] = profile

        public_place = profile.recyclingcenter.address.public_place+', '
        number = profile.recyclingcenter.address.number+', '
        district = profile.recyclingcenter.address.district+' - '
        city = profile.recyclingcenter.address.city+', '
        state = profile.recyclingcenter.address.state
        address = public_place + number + district + city + state
        post['address'] = address
        #print(address) #teste

        post['status_service'] = CustomerService.STATUS_SERVICE_CHOICES[0][0]
        post['confirmed'] = False
        post['return_recipient'] = ''
        post['points_service'] = 0
        post['modification_date'] = None
        post['tagged'] = True
        request.POST = post

        ca_form = CustomerServiceForm(request.POST)
        #print(ca_form)
        #print(ca_form.is_valid()) # teste
        if ca_form.is_valid():
            ca_form.save()
            return redirect('users_auth:userpage_dn')

    ca_form = CustomerServiceForm()
    content = {
        'ca_form': ca_form,
        'profile': profile,
    }
    return render(request, 'donation_service/donor/customer_service.html', content)


def confirm_ca(request, id):
    ca = CustomerService.objects.get(id=id)
    ca_form = CustomerServiceForm(request.POST or None, instance=ca)

    if request.POST:
        #print(request.POST['confirmed'], type(request.POST['confirmed']))

        if request.POST['confirmed'] == 'True':
       
            ca.confirmed = True
            ca.status_service = CustomerService.STATUS_SERVICE_CHOICES[1][0]
        
        elif request.POST['confirmed'] == 'False':

            ca.confirmed = False
            ca.status_service = CustomerService.STATUS_SERVICE_CHOICES[3][0]
        
        ca.save(force_update=True)

        return redirect("users_auth:userpage_rc")

    content = {
        'ca': ca, 
        'ca_form': ca_form
    }

    return render(request, 'donation_service/recyclingcenter/confirm_ca.html', content)


def donation(request, id):
    ca = CustomerService.objects.get(id=id)

    if request.POST:
        post = request.POST.copy()
        post['customerService'] = ca
        post['confirmed'] = False
        post['status_donation'] = Donation.STATUS_DONATION_CHOICES[3][0]
        request.POST = post

        donation_form = DonationForm(request.POST)
        #print(request.POST)
        materials_form_factory = inlineformset_factory(Donation, Material, form=MaterialForm)
        materials_form = materials_form_factory(request.POST)
        
        #print(donation_form.is_valid(), materials_form.is_valid())
        if donation_form.is_valid() and materials_form.is_valid():

            ca.status_service = CustomerService.STATUS_SERVICE_CHOICES[2][0]
            ca.save(force_update=True)

            donation = donation_form.save()
            materials_form.instance = donation
            materials_form.save()

            return redirect('users_auth:userpage_rc')

    donation_form = DonationForm()
    materials_form_factory = inlineformset_factory(Donation, Material, form=MaterialForm, extra=1)
    materials_form = materials_form_factory()

    content = {
        'ca': ca,
        'donation_form': donation_form,
        'materials_form': materials_form,
    }
    return render(request, 'donation_service/recyclingcenter/donation.html', content)


def confirm_donation(request, id):
    ca = CustomerService.objects.get(id=id)
    donation = Donation.objects.get(customerService=ca.id)
    materials = Material.objects.filter(donation=donation.id)
   
    donation_form = DonationForm(request.POST or None, instance=donation)
    if request.POST:
        if request.POST['status_donation'] == '0':
            donation.confirmed = True
            donation.status_donation = Donation.STATUS_DONATION_CHOICES[0][0]
            ca.status_service = CustomerService.STATUS_SERVICE_CHOICES[4][0]

            requester = Donor.objects.get(profile_ptr=ca.requester.id)
            for m in materials:
                ca.points_service = ca.points_service + m.points
    
            #print(ca.points_service)

            requester.ranking_points = requester.ranking_points + ca.points_service
            requester.save()
        
        elif request.POST['status_donation'] == '1':
            #print('a')
            donation.status_donation = Donation.STATUS_DONATION_CHOICES[1][0] # Doação recusada
            #ca.status_service = CustomerService.STATUS_SERVICE_CHOICES[3][0]
            #return redirect('users_auth:userpage_dn')

        elif request.POST['status_donation'] == '2':
            donation.confirmed = False
            donation.status_donation = Donation.STATUS_DONATION_CHOICES[2][0] # Doação recusada
            ca.status_service = CustomerService.STATUS_SERVICE_CHOICES[3][0] # Atendimento recusado

        '''
        if request.POST['confirmed'] == 'True':

            donation.confirmed = True
            donation.status_donation = Donation.STATUS_DONATION_CHOICES[0][0]
            ca.status_service = CustomerService.STATUS_SERVICE_CHOICES[4][0]

            requester = Donor.objects.get(profile_ptr=ca.requester.id)
            for m in materials:
                ca.points_service = ca.points_service + m.points
    
            print(ca.points_service)

            requester.ranking_points = requester.ranking_points + ca.points_service
            requester.save()
        
        elif request.POST['confirmed'] == 'False':

            donation.confirmed = False
            donation.status_donation = Donation.STATUS_DONATION_CHOICES[2][0] # Doação recusada
            ca.status_service = CustomerService.STATUS_SERVICE_CHOICES[3][0] # Atendimento recusado
        '''
        donation.save()
        ca.save()
        return redirect('users_auth:userpage_dn')


    content = {
        'ca': ca,
        'materials': materials,
        'donation_form': donation_form,
    }

    return render(request, 'donation_service/donor/confirm_donation.html', content)


def edit_donation(request, id):
    ca = CustomerService.objects.get(id=id)
    donation = Donation.objects.get(customerService=ca)
    

    if request.POST:
        post = request.POST.copy()
        post['customerService'] = donation.customerService
        post['status_donation'] = Donation.STATUS_DONATION_CHOICES[3][0]
        post['confirmed'] = donation.confirmed

        post['material_set-INITIAL_FORMS'] = '0'

        request.POST = post

        #print(request.POST)

        donation_form = DonationForm(request.POST, instance=ca)
        materials_form_factory = inlineformset_factory(Donation, Material, form=MaterialForm)
        materials_form = materials_form_factory(request.POST, instance=donation)

        print(donation_form.is_valid(), materials_form.is_valid())
        if donation_form.is_valid() and materials_form.is_valid():
            
            donation_id = donation
            materials_delete = Material.objects.filter(donation=donation_id)
            for mat in materials_delete:
                #print(f'{mat.material_name} {mat.material_type} {mat.amount} {mat.points}')
                mat.delete()

            ca.status_service = CustomerService.STATUS_SERVICE_CHOICES[2][0]
            donation.status_donation = Donation.STATUS_DONATION_CHOICES[3][0]
            ca.save(force_update=True)
            donation.save(force_update=True)

            donation = donation_form.save(commit=False)
            #materials_form.instance = donation
            materials_form.save()

            return redirect('users_auth:userpage_rc')

    donation_form = DonationForm(instance=ca)
    materials_form_factory = inlineformset_factory(Donation, Material, form=MaterialForm, extra=0)
    materials_form = materials_form_factory(instance=donation)

    content = {
        'ca': ca,
        'donation_form': donation_form,
        'materials_form': materials_form,
        'is_edit': True
    }
    return render(request, 'donation_service/recyclingcenter/edit_donation.html', content)
