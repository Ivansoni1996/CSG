from django.db import models
from django.contrib.auth.models import User

class Membre(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
    STATUS_ACTIVITE=[
        ('actif', 'Àctif'),
        ('inactif', 'Inactif'),
        ('en_probation', 'En probation'),
        ('default', ''),
    ]
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=False)
    matricule= models.CharField(max_length=6,unique=True)
    status= models.CharField(max_length=20,choices=STATUS_ACTIVITE, default='default')
    cotisation = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.prenom} {self.nom}"
