from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("registrar/", views.registrar, name="registrar"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    
    path('viajes/', views.viajes, name="viajes"),
    path('viajes/viaje1/', views.viaje1, name="viaje1"),
    path('viajes/viaje2/', views.viaje2, name="viaje2"),
    path('viajes/viaje3/', views.viaje3, name="viaje3"),

    path('destinos/', views.destinos, name="destinos"),
    path('destinos/destinos1/', views.destinos1, name="destinos1"),
    path('destinos/destinos2/', views.destinos2, name="destinos2"),
    path('destinos/destinos3/', views.destinos3, name="destinos3"),
    path('destinos/destinos4/', views.destinos4, name="destinos4"),

    path('reserva1/', views.reserva1, name='reserva1'),
    path('reserva2/', views.reserva2, name='reserva2'),
    path('reserva3/', views.reserva3, name='reserva3'),
    path('reserva4/', views.reserva4, name='reserva4'),

    path('guia/', views.guia, name='guia'),
    path('guia1/', views.guia1, name='guia1'),
    path('guia2/', views.guia2, name='guia2'),
    path('guia3/', views.guia3, name='guia3'),
    path('guia4/', views.guia4, name='guia4'),
    path('guia5/', views.guia5, name='guia5'),
    path('guia6/', views.guia6, name='guia6'),

    path('via_reserva1/', views.via_reserva1, name='via_reserva1'),
    path('via_reserva2/', views.via_reserva2, name='via_reserva2'),
    path('via_reserva3/', views.via_reserva3, name='via_reserva3'),

    path("validar-correo/", views.validar_correo, name="validar_correo"),
    
    path('recuperar/', views.recuperar, name='recuperar'),
    path('recuperar/confirm/', views.recuperar_si, name='recuperar_si'),
]