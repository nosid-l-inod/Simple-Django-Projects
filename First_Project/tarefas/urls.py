from django.urls import path

from . import views

urlpatterns = [
    path("", views.lista, name="lista"),
    path("<int:pk>/alternar/", views.alternar, name="alternar"),
    path("<int:pk>/apagar/", views.apagar, name="apagar"),
    path("registo/", views.registo, name="registo"),
]