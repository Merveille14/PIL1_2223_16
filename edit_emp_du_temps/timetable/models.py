from django.db import models

# Create your models here.
class Etudiant(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_de_naissance = models.DateField()
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    adresse = models.TextField()

    def __str__(self):
        return self.nom

# Gestion de l'edition d'emploie du temps

from django.db import models

class Schedule(models.Model):
    groupe = models.CharField(max_length=100)
    cours = models.CharField(max_length=100)
    professeur = models.CharField(max_length=100)
    lieu = models.CharField(max_length=100)
    duree = models.IntegerField()
    heuresAllouees = models.IntegerField()



#Modifier l'emploi du temps après "validation "
# from django.db import models
class EmploiDuTemps(models.Model):
    # ... autres champs de l'emploi du temps ...
    valide = models.BooleanField(default=False)

from django.contrib import messages
def edit_timetable(request):
    # Effectuer les modifications de l'emploi du temps
    # ...
    # Ajouter un message de notification à la file d'attente des messages flash
    messages.success(request, 'L\'emploi du temps a été modifié avec succès.')
    # Rediriger vers la page d'accueil de l'administration ou une autre page appropriée
    return redirect('home')


#Lister les emails de tous les étudiants inscrits
from .models import Etudiant
etudiants = Etudiant.objects.all()
adresses_email = [etudiant.email for etudiant in etudiants]



from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
class AdminManager(BaseUserManager):
    def create_user(self, email, password=None):
        # Créez un utilisateur en utilisant l'email et le mot de passe
        # ...
    def create_superuser(self, email, password):
        # Créez un superutilisateur en utilisant l'email et le mot de passe
        # ...
class Admin(AbstractBaseUser):
    # Ajoutez les champs supplémentaires nécessaires pour votre modèle d'utilisateur personnalisé
    # ...
    objects = AdminManager()
    USERNAME_FIELD = 'email'
    # Ajoutez d'autres champs requis pour l'authentification (ex: 'password')

