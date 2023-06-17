"""
URL configuration for Accueil1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path
from .views import inscription_etudiant

urlpatterns = [
    path('inscription-etudiant', inscription_etudiant, name='inscription_etudiant'),
]

from .views import edit_emploi_du_temps
def edit_emploi_du_temps(request):
    if request.method == 'POST':
        form = EmploiDuTempsForm(request.POST)
        if form.is_valid():
            emploi_du_temps = form.save()
            # Effectuez des opérations supplémentaires si nécessaire
            return redirect('accueil')  # Redirigez vers la page d'accueil ou une autre page appropriée
    else:
        form = EmploiDuTempsForm()
    return render(request, 'edit_emploi_du_temps.html', {'form': form})
urlpatterns = [
    # Autres URL de l' application
    path('edit-emploi-du-temps/', edit_emploi_du_temps, name='edit_emploi_du_temps'),
]

from django.urls import include, path
urlpatterns = [
    # Autres URLs du projet
    path('timetable/', include('timetable.urls')),



from django.urls import path
from .views import ModifierEmploiDuTempsView
urlpatterns = [
    # ... autres URLs de votre application ...
    path('emploi-du-temps/<int:pk>/modifier/', ModifierEmploiDuTempsView.as_view(), name='modifier_emploi_du_temps'),
]
