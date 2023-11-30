from django.db import models
from django.contrib.auth.models import User

class Band(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    members = models.ManyToManyField(User)
    year_formed = models.IntegerField()

    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=50)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    genre = models.CharField(max_length=50)  
    is_demo = models.BooleanField()

    def __str__(self):
        return self.title


class Rehearsal(models.Model):
    date = models.DateField('Rehearsal date')
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    notes = models.TextField(max_length=2000)
    location = models.CharField(max_length=50)
    attendees = models.ManyToManyField(
        User, 
        related_name='attended_rehearsals'
    )

    def __str__(self):
        return str(self.date)        