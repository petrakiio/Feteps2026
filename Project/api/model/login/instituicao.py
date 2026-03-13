from django.db import models

class Instituicao(models.Model):
    id_doctor = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14,unique=True)
    bairro = models.CharField(max_length=100)
    rua = models.CharField(max_length=200)
    cep = models.CharField(max_length=8)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name