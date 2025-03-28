from django.db import models


class University(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "University"
        verbose_name_plural = "Universities"

    def __unicode__(self):
        return self.name


class Result(models.Model):
    grade = models.CharField(max_length=50)

    def __unicode__(self):
        return self.grade


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    university = models.ForeignKey(University,on_delete=models.CASCADE)
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)


