from django.db import models
from django.utils import timezone


class FileNumber(models.Model):
    number = models.PositiveIntegerField()

    class Meta:
        verbose_name = ("FileNumber")

    def __int__(self):
        return self.number


class DocumentListing(models.Model):
    agreement_title = models.CharField(max_length=250)
    file_number = models.ForeignKey(FileNumber, default="general", on_delete="models.CASCADE")
    latest_revision = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    name_of_companies = models.TextField(blank=True)
    first_party = models.TextField(blank=True)
    second_party = models.TextField(blank=True)
    other_party = models.TextField(blank=True)
    type_of_agreement = models.CharField(max_length=250)
    signing_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    effective_from = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    tenure = models.CharField(max_length=250)
    expires_on = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))
    renewal_provision = models.CharField(max_length=250)
    notice_for_termination = models.CharField(max_length=250)
    executed_by = models.TextField(blank=True)
    name_of_product = models.TextField(blank=True)
    custodian_type = models.CharField(max_length=250)
    original = models.CharField(max_length=250)
    duplicate = models.CharField(max_length=250)
    concerned_person = models.TextField(blank=True)
    contact_reference = models.TextField(blank=True)
    remarks = models.CharField(max_length=250)

    class Meta:
        ordering = ["-signing_date"]

    def __int__(self):
        return self.file_number
