from django.db import models

class Doctor(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField(default=0)
    cpf = models.CharField(max_length=11)
    password = models.CharField(max_length=128)
    # Token numerico com 250 digitos, gerado via secrets.
    token = models.CharField(max_length=250,unique=True)
    # Lista simples de ids de pacientes (sem relacionamento).
    paciente_ids = models.JSONField(default=list)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
