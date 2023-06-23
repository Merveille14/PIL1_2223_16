from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth import authenticate, login

def home(request):
    return  render(request,"infos.html")
    
def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        
        user = User(name=name, email=email, password=password)
        user.save()
        return redirect('login')
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Vérifiez les informations de connexion
        User = authenticate(request, email=email, password=password)
        
        if User is not None:
            # Les informations de connexion sont valides, connectez l'utilisateur
            login(request, User)
            return redirect('home')  # Redirigez vers la page de tableau de bord après la connexion réussie
        else:
            # Les informations de connexion sont invalides, affichez un message d'erreur
            error_message = "Nom d'utilisateur ou mot de passe incorrect."
            return render(request, 'login.html', {'error_message': error_message})
    
    return render(request, 'login.html')