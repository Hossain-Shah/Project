from django.contrib.gis.db import models


class Points(models.Model):
    name = models.CharField(max_length=20)
    location = models.PointField()
    description = models.CharField(max_length=200,blank=True)
