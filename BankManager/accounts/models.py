from django.db import models


class Post(models.Model):
    name = models.TextField()
    balance = models.IntegerField()

    def __str__(self):
        return self.name
