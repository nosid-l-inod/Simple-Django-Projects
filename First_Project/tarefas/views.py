from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import TarefaForm
from .models import Tarefa


@login_required
def lista(request):
    if request.method == "POST":
        form = TarefaForm(request.POST)
        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.utilizador = request.user
            tarefa.save()
            return redirect("lista")
    else:
        form = TarefaForm()
    tarefas = Tarefa.objects.filter(utilizador=request.user)
    return render(request, "tarefas/lista.html", {"tarefas": tarefas, "form": form})


@login_required
@require_POST
def alternar(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk, utilizador=request.user)
    tarefa.concluida = not tarefa.concluida
    tarefa.save()
    return redirect("lista")


@login_required
@require_POST
def apagar(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk, utilizador=request.user)
    tarefa.delete()
    return redirect("lista")


def registo(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            utilizador = form.save()
            login(request, utilizador)
            return redirect("lista")
    else:
        form = UserCreationForm()
    return render(request, "registration/registo.html", {"form": form})