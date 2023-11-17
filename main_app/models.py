from django.db import models
from django.contrib.auth.models import User

class Band(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=100)
    members = models.ManyToManyField(User)
    year_formed = models.IntegerField()



class Song(models.Model):
    title = models.CharField(max_length=50)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    genre = models.CharField(max_length=50)  
    is_demo = models.BooleanField()


class Rehearsal(models.Model):
    date = models.DateField('Rehearsal date')
    notes = models.TextField(max_length=250)
    location = models.CharField(max_length=50)
    attendees = models.ManyToManyField(
        User, 
        related_name='attended_rehearsals'
    )        