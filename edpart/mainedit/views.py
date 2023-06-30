
# Create your views here.
from django.shortcuts import render,redirect
from .form import SemesForm
from django.views import View
from .models import EditInfo,Lessons,Professeur,Semes

def submit_form(request):
    if request.method =='POST':
        form=SemesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('succes_v')
    else:
        form=SemesForm()
    return render(request,'type.html',{'form':form})

def succes_v(request):
    return render(request,'succes.html')
        
# Create your views here.

