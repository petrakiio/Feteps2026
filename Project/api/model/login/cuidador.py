from django.db import models

class Cuidador(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    cpf = models.CharField(max_length=11)
    id_idoso = models.IntegerField(default=0,unique=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome