from django.db import models

class User(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    cpf = models.CharField(max_length=11,unique=True)
    # Remedio/horario unico (mantido para compatibilidade).
    remedio = models.CharField(max_length=120)
    horario = models.TimeField()
    # Listas de remedios/horarios do paciente.
    remedios = models.JSONField(default=list)
    horarios = models.JSONField(default=list)
    # Quando for paciente de um medico, guarda o id do Doctor.
    id_doctor = models.IntegerField(null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
