# Generated by Django 5.0.7 on 2024-12-20 19:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Smart', '0004_hotel_loction_place_loction'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelOffre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_base', models.BooleanField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('prix', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotel_offre', to='Smart.hotel')),
            ],
        ),
    ]