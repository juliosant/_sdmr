# Generated by Django 3.2.7 on 2021-09-20 22:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_donation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerservice',
            name='requester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requester', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customerservice',
            name='return_recipient',
            field=models.TextField(blank=True, max_length=300),
        ),
    ]
