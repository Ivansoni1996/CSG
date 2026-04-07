from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('accueil/', views.accueil, name='accueil'),
    path('ajouter/', views.ajouter_membre, name='ajouter_membre'),
    path('inscrire/', views.inscrire_membre, name='inscrire_membre'),
    path('liste/', views.liste_membres, name='liste_membres'),
    path('login/', auth_views.LoginView.as_view(template_name='members/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('modifier/<int:membre_id>/', views.modifier_membre, name='modifier_membre'),
    path('supprimer/<int:membre_id>/', views.supprimer_membre, name='supprimer_membre'),
    path('contacter/<int:membre_id>/', views.contacter_membre, name='contacter_membre'),
    path('paypal-webhook/', views.paypal_webhook, name='paypal_webhook'),
    path('verif_role/', views.verifier_role, name='verifier_role'),
    path('profil_membre/', views.profil_membre, name='profil_membre'),
    path('profil_admin/', views.profil_admin, name='profil_admin'),
]