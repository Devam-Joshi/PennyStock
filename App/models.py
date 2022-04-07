from django.db import models

class Contactform(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    message = models.CharField(max_length=255)
