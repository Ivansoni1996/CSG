from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect,get_object_or_404
from django.core.mail import send_mail
from .forms import ContactMessageForm
from .forms import MembreForm
from .models import Membre
import json

def accueil(request):
    return render(request, 'members/accueil.html')

# cette vue gere l'ajout d'un utilisateur dans la base de donnees par ladmin
def ajouter_membre(request):
    if request.method == 'POST':
        form = MembreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_membres') # On redirigera vers la liste après
    else:
        form = MembreForm()
    form = MembreForm()
    return render(request, 'members/ajouter_membres.html', {'form': form})

# cette vue permet a lutilisateur de sincrire a CSG de lui meme
def inscrire_membre(request):
    if request.method == 'POST':
        form = MembreForm(request.POST)
        if form.is_valid(): 
            mdp = form.cleaned_data.get('password')
            nouveau_user = User.objects.create_user(
                username=form.cleaned_data['matricule'], 
                email=form.cleaned_data['email'],
                password=mdp )
            membre = form.save(commit=False)
            membre.user = nouveau_user
            membre.save()
            return redirect('login')
    else:
        form = MembreForm()
    form = MembreForm()
    return render(request, 'members/inscrire_membre.html', {'form': form})

#cette d´fonction recupere tous les membres de la base de donnees pour lenvoyer au template
@login_required
def liste_membres(request):
    # Récupère tous les membres du plus récent au plus ancien
    membres = Membre.objects.all().order_by('nom')
    return render(request, 'members/liste_membres.html', {'membres': membres})

#cette fonction suprime les un membre de notre list

def supprimer_membre(request, membre_id):
    membre = get_object_or_404(Membre, id=membre_id)
    
    # 1. Préparer et envoyer l'e-mail de notification
    sujet = "Notification du group CSG"
    message = f"Bonjour {membre.prenom},\n\nNous vous informons que vous ne faites plus partie de la liste des membres du Group CSG."
    email_expediteur = 'solidaritecameroun06@gmail.com'
    
    try:
        send_mail(sujet, message, email_expediteur, [membre.email])
    except Exception as e:
        print(f"Erreur d'envoi d'email : {e}")

    # 2. Supprimer le membre de la base de données
    membre.delete()
    
    return redirect('liste_membres')

def modifier_membre(request, membre_id):
    # On récupère le membre existant
    membre = get_object_or_404(Membre, id=membre_id)
    
    if request.method == 'POST':
        # On lie le formulaire à l'instance existante avec les nouvelles données du POST
        form = MembreForm(request.POST, instance=membre)
        if form.is_valid():
            form.save()
            return redirect('liste_membres')
    else:
        # On affiche le formulaire pré-rempli avec les infos du membre
        form = MembreForm(instance=membre)
    
    return render(request, 'members/modifier_membre.html', {'form': form, 'membre': membre})


def contacter_membre(request, membre_id):
    membre = get_object_or_404(Membre, id=membre_id)
    
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            sujet = form.cleaned_data['sujet']
            corps = form.cleaned_data['message']
            expediteur = 'solidaritecameroun06@gmail.com'
            
            try:
                send_mail(sujet, corps, expediteur, [membre.email])
                messages.success(request, f"Message envoyé à {membre.prenom} !")
                return redirect('liste_membres')
            except Exception as e:
                messages.error(request, f"Erreur d'envoi : {e}")
    else:
        # On pré-remplit le sujet pour gagner du temps
        form = ContactMessageForm(initial={'sujet': ''})

    return render(request, 'members/contacter_membre.html', {'form': form, 'membre': membre})
# cette fonction recoit les notifications de payspal et met ajour la fiche du membre
@csrf_exempt
def paypal_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # On vérifie si c'est un événement de paiement réussi
        if data['event_type'] == 'PAYMENT.CAPTURE.COMPLETED':
            # On récupère le matricule qu'on a mis dans 'custom_id'
            resource = data['resource']
            matricule = resource.get('custom_id')
            montant = resource['amount']['value']
            
            # On cherche le membre et on met à jour sa fiche
            try:
                membre = Membre.objects.get(matricule=matricule)
                membre.cotisation = float(montant)
                membre.status = 'Actif' # Par exemple
                membre.save()
                
                # Optionnel : Tu peux ici envoyer un mail de confirmation à l'admin
            except Membre.DoesNotExist:
                pass 

        return HttpResponse(status=200)
    return HttpResponse(status=400)


@login_required
def profil_membre(request):
    try:
        # On essaie de récupérer le membre lié à celui qui est connecté
        membre = Membre.objects.get(user=request.user)
        return render(request, 'members/profil_membre.html', {'membre': membre})
    except Membre.DoesNotExist:
        # Si l'utilisateur connecté n'est pas encore un "Membre" dans ta base
        return render(request, 'members/erreur.html')
@login_required
def profil_admin(request):
    try:
        # On essaie de récupérer le membre lié à celui qui est connecté
        membre = Membre.objects.get(user=request.user)
        return render(request, 'members/profil_admin.html', {'membre': membre})
    except Membre.DoesNotExist:
        # Si l'utilisateur connecté n'est pas encore un "Membre" dans ta base
        return render(request, 'members/erreur.html')


@login_required
def verifier_role(request):
    if request.user.is_staff:
        return redirect('profil_admin')
    else:
        return redirect('profil_membre')
    