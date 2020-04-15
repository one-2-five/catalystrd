from django.db import models

# Create your models here.

class Document(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    creator = models.CharField(max_length=60, blank=False, default='admin')
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/',blank=True)
    document1 = models.FileField(upload_to='documents/',blank=True)
    document2 = models.FileField(upload_to='documents/',blank=True)
    training_status = models.BooleanField(default=False)
    covidstate = models.CharField(max_length=255, blank=True,default='Not Processed')
    filetype = models.CharField(max_length=10, blank=False, default='jpg')
    predictstate = models.BooleanField(default=False)
    def __str__(self):
        return self.description + ": " + self.creator