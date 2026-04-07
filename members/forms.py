from django import forms
from .models import Membre

class MembreForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}),
        label="Mot de passe"
    )
    class Meta:
        model = Membre
        fields = ['nom', 'prenom', 'email', 'matricule', 'status']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'matricule': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Matricule'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        
class ContactMessageForm(forms.Form):
    sujet = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))