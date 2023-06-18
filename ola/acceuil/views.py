from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def status(request):
    return render(request, 'acceuil/status.html')
def student(request):
    return render(request, 'acceuil/student.html')
def teacher(request):
    return render(request, 'acceuil/teacher.html')
def school(request):
    return render(request, 'acceuil/school.html')