from django.db import models


class ContactListBackup(models.Model):
    SL = models.IntegerField()
    Name = models.TextField()
    Number = models.IntegerField()

    def _str_(self):
        return self.SL
