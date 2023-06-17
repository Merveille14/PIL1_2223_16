from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import InscriptionEtudiantForm

def inscription_etudiant(request):
    if request.method == 'POST':
        form = InscriptionEtudiantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accueil')
    else:
        form = InscriptionEtudiantForm()
    return render(request, 'inscription_etudiant.html', {'form': form})



from django.core.mail import send_mail

def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            utilisateur = form.save()
            # Envoi de l'e-mail de confirmation
            sujet = 'Confirmation d\'inscription'
            message = 'Merci de vous être inscrit à notre site.'
            destinataires = [utilisateur.email]
            send_mail(sujet, message, 'votre_adresse_email@gmail.com', destinataires)
            return redirect('connexion')
    else:
        form = InscriptionForm()
    return render(request, 'inscription.html', {'form': form})
""""
 from django.shortcuts import render
from .models import Cours

def emploi_du_temps(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('groupe'):
                groupe = value
                cours = request.POST['cours' + key[6:]]
                professeur = request.POST['professeur' + key[6:]]
                lieu = request.POST['lieu' + key[6:]]
                duree = request.POST['duree' + key[6:]]
                heures_allouees = request.POST['heuresAllouees' + key[6:]]
                Cours.objects.create(groupe=groupe, nom_cours=cours, nom_professeur=professeur, lieu_cours=lieu, duree=duree, heures_allouees=heures_allouees)
        return render(request, 'emploi/success.html')
    return render(request, 'emploi/emploi_du_temps.html')
"""
from django.shortcuts import render, redirect
from .models import Schedule

def edit_schedule(request):
    if request.method == 'POST':
        # Récupérer les données soumises
        groupe = request.POST.get('groupe')
        cours = request.POST.get('cours')
        professeur = request.POST.get('professeur')
        lieu = request.POST.get('lieu')
        duree = request.POST.get('duree')
        heuresAllouees = request.POST.get('heuresAllouees')
        # ... récupérez les autres données soumises ...

        # Créer une instance du modèle et enregistrer les données dans la base de données
        schedule = Schedule(groupe=groupe, cours=cours, professeur=professeur, lieu=lieu, duree=duree, heuresAllouees=heuresAllouees)
        schedule.save()

        return redirect('success_url')  # Rediriger vers une page de succès

    return render(request, 'timetable.html')


"""
from django.shortcuts import render

def edit_schedule(request):
    return render(request, 'timetable.html') 
"""


#Modification ou mise à jour des données apès validation avec "Updateview"
from django.views.generic import UpdateView
from .models import EmploiDuTemps
from .forms import EmploiDuTempsForm

class ModifierEmploiDuTempsView(UpdateView):
    model = EmploiDuTemps
    form_class = EmploiDuTempsForm
    template_name = 'modifier_emploi_du_temps.html'
    success_url = '/emploi-du-temps/'  # URL de redirection après la modification

    def get_queryset(self):
        # Limitez la requête aux emplois du temps non validés(filtrer les emplois non validés avec "get_queryset)
        queryset = super().get_queryset()
        return queryset.filter(valide=False)

#envoie de notification aux étudiants après modification
from django.core.mail import send_mail
def edit_emploi_du_temps(request):
    # ...
    # ici, édition ou la modification de l'emploi du temps
    # ...
    # Ensuite récupération des adresses e-mail des étudiants inscrits
    etudiants = Etudiant.objects.all()
    adresses_email = [etudiant.email for etudiant in etudiants]

    # Envoi de l'e-mail de notification à tous les étudiants
    sujet = "Nouvelle édition de l'emploi du temps"
    message = "Cher étudiant, une nouvelle édition de l'emploi du temps a été publiée. Veuillez consulter les modifications sur notre site."
    send_mail(sujet, message, 'votre_adresse_email@gmail.com', adresses_email)
    # ...
    # Redirection ou autre logique supplémentaire
    # ...

#S'assurer que seule l'administration édite l'emploi du temps
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from .models import EmploiDuTemps
from .forms import EmploiDuTempsForm
@login_required
def ModifierEmploiDuTempsView(UpdateView):
    model = EmploiDuTemps
    form_class = EmploiDuTempsForm
    template_name = 'modifier_emploi_du_temps.html'
    success_url = '/emploi-du-temps/'  # URL de redirection après la modification
    def get_queryset(self):
        # Limitez la requête aux emplois du temps non validés
        queryset = super().get_queryset()
        return queryset.filter(valide=False)
