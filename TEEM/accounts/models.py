
from django.db import models
from django.contrib.auth.models import User
import geocoder

# Create your models here.

token = 'pk.eyJ1IjoidGVlbTEiLCJhIjoiY21jOW00eWgyMDQ1cjJzc2x2NnloZDI4MiJ9.RsKX8bG-FaDg7loiIJ5wgg'

class Address(models.Model):
    title = models.TextField()
    date = models.TextField()
    address = models.TextField()
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    description = models.TextField()

    def save(self, *args, **kwargs):
        g = geocoder.mapbox(self.address, key=token)
        g = g.latlng
        self.lat = g[0]
        self.long = g[1]
        return super(Address, self).save(*args, **kwargs)

'''  
class Event(models.Model):
    title = models.CharField(max_length=200, default='Neues Event')
    max_participants = models.IntegerField(default=20)
    teilnehmer = models.ManyToManyField(User, blank=True)

    def _str_(self):
        return self.title

'''