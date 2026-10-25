from django.db import models
from django.conf import settings

# Classe tarefas
class Tarefa(models.Model):
    utilizador = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tarefas"
    )
    titulo = models.CharField(max_length=200)
    concluida = models.BooleanField(default=False)
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["concluida", "-criada_em"]

    def __str__(self):
        return self.titulo