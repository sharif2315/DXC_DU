from django.shortcuts import render, redirect
from .models import *
from .forms import *
# Create your views here.
def home(request):
    drives = RepoStatus.objects.all()
    form = DriveForm()

    if request.method == 'POST':
        form = DriveForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')

    context = { 'drives': drives, 'form': form }
    return render(request, 'diskUsage/home.html', context)
    # return render(request, 'diskUsage/home2.html', context)

def create(request):
    form = DriveForm()
    context = { 'form': form }
    return render(request, 'diskUsage/create.html', context)
