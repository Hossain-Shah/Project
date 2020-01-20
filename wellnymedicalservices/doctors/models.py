from django.db import models


class Diagnosis(models.Model):
    name = models.CharField(max_length=255, blank=True)
    Rostered_physician = models.CharField(max_length=255, blank=True)
    condition = models.CharField(max_length=255, blank=True)
    details = models.CharField(max_length=255, blank=True)
    date_of_diagnosis = models.DateField(blank=True, null=True)
    content = models.TextField(blank=True)

    def _tuple_(self):
        return self.name, self.Rostered_physician, self.condition, self.details, self.date_of_diagnosis, self.content


class TODOItem(models.Model):
    job = models.CharField(max_length=200)
    due_date = models.DateField(blank=True, null=True)
    medication_details = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def _tuple_(self):
        return self.job, self.due_date, self.medication_details, self.completed



