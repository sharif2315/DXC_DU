from django.db import models

# Create your models here.
class CurrentJobs(models.Model):
    path = models.CharField(max_length=200)

class RepoStatus(models.Model):
    drivePath = models.CharField(max_length=200)
    numOfFiles = models.IntegerField()
    sizeOfFiles = models.IntegerField()
