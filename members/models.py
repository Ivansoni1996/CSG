from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class Members(models.Model):
    STATUS_ACTIVITE=[
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('en_probation', 'En probation'),]
    member_id = models.CharField(max_length=30,primary_key=True,default="")
    email = models.EmailField(max_length=30,default="")
    name = models.CharField(max_length=30,default="")
    family_name=models.CharField(max_length=40,default="")
    status=models.CharField(max_length=15, choices=STATUS_ACTIVITE, default="inactif")
    password=models.CharField(max_length=20, choices=STATUS_ACTIVITE, default="")
    amount= models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name
