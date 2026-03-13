from django.db import models

class Doctor(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField(default=0)
    token = models.CharField(max_length=250)
    paciente_ids = models.JSONField(default=list)
    
