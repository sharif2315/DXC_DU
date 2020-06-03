from django.shortcuts import render, redirect
from .models import *
from .forms import *
import subprocess
# Create your views here.
def home(request):
    drives = RepoStatus.objects.all()
    form = DriveForm()
    print(drives)
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

def service(request, id=0):
    if id == '1':
        pspath = r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
        subprocess.getoutput(pspath + ' Start-Service -Name PythonDU')
        output = subprocess.getoutput(pspath + ' Get-Service PythonDU').split()[6]
        mylist = []
        mydict = {}
        mydict['status'] = output
        mylist.append(mydict)
        context = {'mylist': mylist}
        return render(request, 'diskUsage/service.html', context)

    elif id == '2':
        pspath = r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
        subprocess.getoutput(pspath + ' Stop-Service -Name PythonDU')
        output = subprocess.getoutput(pspath + ' Get-Service PythonDU').split()[6]
        mylist = []
        mydict = {}
        mydict['status'] = output
        mylist.append(mydict)
        context = {'mylist': mylist}
        return render(request, 'diskUsage/service.html', context)

    else:
        pspath = r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
        output = subprocess.getoutput(pspath + ' Get-Service PythonDU').split()[6]
        mylist = []
        mydict = {}
        mydict['status'] = output
        mylist.append(mydict)
        context = {'mylist': mylist}
        return render(request, 'diskUsage/service.html', context)
