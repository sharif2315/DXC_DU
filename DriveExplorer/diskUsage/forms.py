from django import forms
from django.forms import ModelForm

# used for YT csv upload
import csv
import io


from .models import *

class DriveForm(forms.ModelForm):

    class Meta:
        model = CurrentJobs
        fields = '__all__'

# class DataForm(forms.Form):
#     data_file = forms.FileField()
#
#     def process_data(self):
#         f = io.TextIOWrapper(self.cleaned_data['data_file'].file)
#         reader = csv.DictReader(f)
#
#         for record in reader:
#             Car.objects.create_car(name['name'],
#                                         price['price'], vehicleType['vehicleType'],
#                                         yearOfRegistration['yearOfRegistration'],
#                                         gearBox['gearBox'],
#                                         power['power'],
#                                         model['model'],
#                                         mileage['mileage'],
#                                         fuelType['fuelType'],
#                                         brand['brand'],
#                                         notRepairedDamage['notRepairedDamage'],
#                                         dateCreated['dateCreated'],
#                                         city['city'],
#                                         country['country'])
