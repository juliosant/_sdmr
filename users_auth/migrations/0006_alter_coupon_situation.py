# Generated by Django 3.2.7 on 2021-11-13 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_auth', '0005_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='situation',
            field=models.CharField(choices=[('A', 'DISPONÍVEL'), ('E', 'EXPIRADO'), ('U', 'INDISPONÍVEL')], max_length=1),
        ),
    ]