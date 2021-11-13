from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE

# Create your models here.
class Profile(AbstractUser):
    PROFILE_TYPE_CHOICES = [
        ("D", "Doador"),
        ("R", "Ponto de Coleta")
    ]
    code = models.CharField(max_length=11)
    email = models.EmailField(unique=True, 
            error_messages={'unique': "Já existe um usuário com este email", 'required': 'Por favor dgite um email'})
    phone = models.CharField(max_length=11)
    profile_type = models.CharField(max_length=1, choices=PROFILE_TYPE_CHOICES)
    about = models.TextField(max_length=300)
    #img_profile = models.ImageField(upload_to='img_profile', null=True, blank=True)

class Donor(Profile):
    general_points = models.FloatField(default=0)
    ranking_points = models.FloatField(default=0)

class Address(models.Model):
    branch = models.CharField(max_length=100)
    public_place = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    complement = models.CharField(max_length=200)

class RecyclingCenter(Profile):
    corporate_name = models.CharField(max_length=200)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)


class Coupon(models.Model):
    SITUATION_CHOICE = [
        ('A', 'DISPONÍVEL'),
        ('E', "EXPIRADO"),
        ('U', 'INDISPONÍVEL'),
    ]

    donor_id = models.ForeignKey(Donor, on_delete=CASCADE)
    value = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    pass_key = models.CharField(max_length=200, null=False, blank=False)
    used = models.BooleanField(default=False)
    expiration_date = models.DateTimeField()
    situation = models.CharField(max_length=1, choices=SITUATION_CHOICE)
    #creation_date = models.DateTimeField(auto_now_add=True)
