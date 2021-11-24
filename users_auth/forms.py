from django import forms
from .models import Address, Coupon, Donor, Profile, RecyclingCenter
from django.contrib.auth import forms as forms_user
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    user = forms.CharField(label="Usuário", widget=forms.TextInput(attrs={'placeholder': "Email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Senha"}))
      

class ProfileChangeForm(forms_user.UserChangeForm):
    class Meta(forms_user.UserChangeForm.Meta):
        model = Profile


class ProfileCreationForm(forms_user.UserCreationForm):
    class Meta(forms_user.UserCreationForm.Meta):
        model = Profile


class ProfileForm(UserCreationForm):
    code = forms.CharField(label='código', max_length=11)
    first_name = forms.CharField(label="Nome")
    last_name = forms.CharField(label='Sobrenome')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='Telefone')
    profile_type = forms.ChoiceField(choices=Profile.PROFILE_TYPE_CHOICES)
    about = forms.CharField(max_length=300, widget=forms.Textarea(attrs={'placeholder': 'Digite algo sobre você'}))

    class Meta:
        model = Profile
        fields = ['code', 'first_name', 'last_name', 'email', 'phone', 'profile_type', 'about', 'username', 'password1', 'password2',]
    
    

# DN
class DNCreationForm(forms_user.UserCreationForm):
    class Meta:
        model = Donor
        fields = ['code', 'first_name', 'last_name', 'email', 'phone', 'about', 'username', 'password1', 'password2', 'profile_type',]
        widgets = {
            'first_name': forms.TextInput(attrs={"oninput":"upperWord(event);"}),
            'last_name': forms.TextInput(attrs={"oninput":"upperWord(event);"}),
            #'email': forms.TextInput(attrs={"oninput":"upperWord(event);"}),
            'about': forms.Textarea(attrs={"oninput":"upperWord(event);"}),
        }


# RC
class RCCreationForm(forms_user.UserCreationForm):
    class Meta(forms_user.UserCreationForm.Meta):
        model = RecyclingCenter
        fields = ['code', 'corporate_name','email', 'phone', 'address', 'about', 'profile_type', 'materials', 'first_name', 'last_name', 'username', 'password1', 'password2',]
        widgets = {
            'corporate_name': forms.TextInput(attrs={"oninput":"upperWord(event);", "id": 'corporate_name'}),
            'about': forms.Textarea(attrs={"oninput":"upperWord(event);", "id": 'id_about'}),
            'email': forms.TextInput(attrs={"id": 'id_email'}),
        }



class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        widgets = {
            'branch': forms.TextInput(attrs={"oninput":"upperWord(event);", "id": 'branch'}),
            'number': forms.TextInput(attrs={"oninput":"upperWord(event);"}),
            'public_place': forms.TextInput(attrs={"oninput":"upperWord(event);", "id": 'public_place'}),
            'district': forms.TextInput(attrs={"oninput":"upperWord(event);", "id": 'district'}),
            'city': forms.TextInput(attrs={"oninput":"upperWord(event);", "id": 'city'}),
            'state': forms.TextInput(attrs={"oninput":"upperWord(event);", "id": 'state'}),
            'complement': forms.TextInput(attrs={"oninput":"upperWord(event);", "id": 'complement'}),
        }


class RCChangeForm(forms_user.UserChangeForm):
    class Meta(forms_user.UserChangeForm.Meta):
        model = Profile
        fields = '__all__'


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = '__all__'
        widgets = {
            'value': forms.NumberInput(attrs={'type':"text", 'id': "generated_coupon", 'max':'2000', "onkeyup":"calc_removed_points();"})
        }