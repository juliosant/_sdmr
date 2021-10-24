from .models import CustomerService, Donation, Material
from django import forms

class SearchRCForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Buscar por endereço, nome ou código'}))


class CustomerServiceForm(forms.ModelForm):
    STATUS_CONFIRMED = [
        (True, 'Sim'),
        (False, 'Não')        
    ]
    confirmed = forms.ChoiceField(choices=STATUS_CONFIRMED)
    class Meta:
        model = CustomerService
        fields = '__all__'
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date'}),
        }


class DonationForm(forms.ModelForm):
    STATUS_CONFIRMED = [
        (True, 'Sim'),
        (False, 'Não')        
    ]
    STATUS_DONATION_CHOICE = [
        ("3", ""),
        ("0", "Confirmar"),
        ("1", "Pedir Revisão"),
        ("2", "Recusar"),
    ]
    status_donation = forms.ChoiceField(choices=STATUS_DONATION_CHOICE)
    confirmed = forms.ChoiceField(choices=STATUS_CONFIRMED)
    class Meta:
        model = Donation
        fields = '__all__'


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = '__all__'
        widgets = {
            'amount': forms.TextInput(attrs={'onkeyup': "calc_points('0');"}),
            'points': forms.TextInput(attrs={'readonly':'', 'onclick': 'calc_points'+'({'+'{forloop.counter0'+'}'+'});'})
        }
