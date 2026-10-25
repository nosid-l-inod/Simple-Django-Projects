from django.contrib import admin
from .models import Tarefa

@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ["titulo", "utilizador", "concluida", "criada_em"]
    list_filter = ["concluida"]