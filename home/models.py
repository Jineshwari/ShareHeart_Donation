from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import random

class NGO(models.Model):
    ngo_id = models.CharField(max_length=10, primary_key=True)
    ngo_name = models.CharField(max_length=100)
    ngo_email = models.CharField(max_length=100)  # Changed to EmailField for validation
    phone1 = models.BigIntegerField(null=True, blank=True)
    phone2 = models.BigIntegerField(null=True, blank=True)
    building_house_no = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    pin = models.CharField(max_length=10, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'ngo'  # Matches your existing MySQL table name
        managed = False     # Prevent Django from trying to create or modify this table

# home/models.py
from django.db import models

class User(models.Model):
    user_id = models.CharField(max_length=8, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone1 = models.BigIntegerField(blank=True, null=True)
    phone2 = models.BigIntegerField(blank=True, null=True)
    house_no = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pin = models.CharField(max_length=10, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'user'  # Matches your existing MySQL table name
        managed = False     # Prevent Django from trying to create or modify this table


class Donor(models.Model):
    donor_id = models.CharField(max_length=100, primary_key=True)
    donor_name = models.CharField(max_length=255)
    # other fields

class DonorInfo(models.Model):
    books = models.IntegerField(default=0)
    shoes = models.IntegerField(default=0)
    stationary = models.IntegerField(default=0)
    clothes = models.IntegerField(default=0)
    food = models.IntegerField(default=0)
    toys = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donor_info')
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    pin = models.IntegerField(null=True, blank=True)
    pick_up = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Donor Info for {self.name}"
    
class Voucher(models.Model):
    voucher_id = models.AutoField(primary_key=True)
    voucher_name = models.CharField(max_length=255)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    T_and_C = models.TextField(blank=True, null=True)
    expiry_date = models.DateField()
    points_needed = models.IntegerField()

    def __str__(self):
        return self.voucher_name