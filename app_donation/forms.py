from .models import CustomerService, Donation, Material
from django import forms

class SearchRCForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Buscar por endereço, nome ou código'}))


class CustomerServiceForm(forms.ModelForm):
    STATUS_CONFIRMED = [
        (True, 'Sim'),
        (False, 'Não')        
    ]
    confirmed = forms.ChoiceField(choices=STATUS_CONFIRMED, widget = forms.Select(attrs={'onclick': "change_textearea();"}))

    TIME_CHOICES = [
        (None, 'hh:mm'),
        ('08:00', '08:00'), ('08:30', '08:30'),
        ('09:00', '09:00'), ('09:30', '09:30'),
        ('18:00', '18:00'), ('18:30', '18:30'),
        ('11:00', '11:00'), ('11:30', '11:30'),
        ('12:00', '12:00'), ('12:30', '12:30'),
        ('13:00', '13:00'), ('13:30', '03:30'),
        ('14:00', '14:00'), ('14:30', '14:30'),
        ('15:00', '15:00'), ('15:30', '15:30'),
        ('16:00', '16:00'), ('16:30', '16:30'),
        ('17:00', '17:00'), ('17:30', '17:30'),
    ]
    time = forms.ChoiceField(choices = TIME_CHOICES)

    class Meta:
        model = CustomerService
        fields = '__all__'
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date'}),
            'return_recipient': forms.Textarea(attrs={'placeholder': 'Justificar para o doador'}),
            #'return_recipient': forms.Textarea(attrs={'style':'display:none;'}),
            #'confirmed': forms.Select(attrs={'onchange': "change_textearea();"})
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
