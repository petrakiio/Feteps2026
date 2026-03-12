from django.db import models

class User(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    remedio = models.CharField(max_length=120)
    horario = models.TimeField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name