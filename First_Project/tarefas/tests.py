from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Tarefa

User = get_user_model()


class TarefasTests(TestCase):
    def setUp(self):
        self.ana = User.objects.create_user("ana", password="pass12345!")
        self.rui = User.objects.create_user("rui", password="pass12345!")

    def test_lista_exige_login(self):
        resposta = self.client.get(reverse("lista"))
        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/contas/login/", resposta.url)

    def test_criar_tarefa(self):
        self.client.login(username="ana", password="pass12345!")
        self.client.post(reverse("lista"), {"titulo": "Estudar Django"})
        tarefa = Tarefa.objects.get()
        self.assertEqual(tarefa.utilizador, self.ana)

    def test_alternar_e_apagar(self):
        tarefa = Tarefa.objects.create(utilizador=self.ana, titulo="Teste")
        self.client.login(username="ana", password="pass12345!")
        self.client.post(reverse("alternar", args=[tarefa.pk]))
        tarefa.refresh_from_db()
        self.assertTrue(tarefa.concluida)
        self.client.post(reverse("apagar", args=[tarefa.pk]))
        self.assertEqual(Tarefa.objects.count(), 0)

    def test_nao_ve_tarefas_de_outros(self):
        tarefa = Tarefa.objects.create(utilizador=self.ana, titulo="Privada")
        self.client.login(username="rui", password="pass12345!")
        resposta = self.client.post(reverse("apagar", args=[tarefa.pk]))
        self.assertEqual(resposta.status_code, 404)
        self.assertEqual(Tarefa.objects.count(), 1)

    def test_registo_cria_conta_e_entra(self):
        resposta = self.client.post(
            reverse("registo"),
            {"username": "novo", "password1": "pass12345!xyz", "password2": "pass12345!xyz"},
        )
        self.assertRedirects(resposta, reverse("lista"))
        self.assertTrue(User.objects.filter(username="novo").exists())