from django.contrib import admin
from .models import Membre

@admin.register(Membre)
class MembreAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email','matricule','status', 'cotisation')
    list_filter = ('cotisation','status')
    search_fields = ('nom', 'email','matricule')
