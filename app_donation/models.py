from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from users_auth.models import Profile

# Create your models here.
class CustomerService(models.Model):
    STATUS_SERVICE_CHOICES = [
        ("0", "Aguardando Confirmação de Atendimento"),
        ("1", "Confirmado Atendimento"),
        ("2", "Aguardando Confirmação de Doação"),
        ("3", "Cancelado"),
        ("4", "Concluído")
    ]
    requester = models.ForeignKey(Profile, on_delete=CASCADE, related_name="requester")
    recipient = models.ForeignKey(Profile, on_delete=CASCADE, related_name="recipient")
    address = models.CharField(max_length=200)
    date = models.DateField() 
    time = models.TimeField()
    confirmed = models.BooleanField(blank=True)
    status_service = models.CharField(max_length=1, choices=STATUS_SERVICE_CHOICES)
    return_recipient = models.TextField(max_length=300, blank=True)
    points_service = models.FloatField()
    joined_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(null=True, blank=True)
    tagged = models.BooleanField(blank=True) # Atendimento marcado ou avuslso?


class Donation(models.Model):
    STATUS_DONATION_CHOICES = [
        ("0", "Confirmada"),
        ("1", "Precisa Revisar"),
        ("2", "Cancelada"),
        ("3", "Aguardando Materiais")
    ]
    customerService = models.ForeignKey(CustomerService, on_delete=CASCADE)
    joined_date = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(blank=True)
    status_donation = models.CharField(max_length=1, choices=STATUS_DONATION_CHOICES)


class Material(models.Model):
    donation = ForeignKey(Donation, on_delete=CASCADE)
    material_name = models.CharField(max_length=100)
    material_type = models.CharField(max_length=100)
    amount = models.FloatField()
    points = models.FloatField()