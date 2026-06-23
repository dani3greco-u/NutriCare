from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard-nutrizionista/', views.dashboard_nutrizionista, name='dashboard_nutrizionista'),
    path('dashboard-paziente/', views.dashboard_paziente, name='dashboard_paziente'),
    path('paziente/<str:email>/', views.dettaglio_paziente, name='dettaglio_paziente'),
    path('logout/', views.logout_view, name='logout'),
    path('gestisci_rilevazioni/<str:email>/', views.gestisci_rilevazioni, name='gestisci_rilevazioni'),
    path('paziente/<str:email>/gestisci-piano/<int:pk>/', views.gestisci_piano, name='gestisci_piano'),
    path('gestisci-pasti/<int:giornata_id>/', views.gestisci_pasti, name='gestisci_pasti'),
    path('gestisci-alimenti/<int:pasto_id>/', views.gestisci_alimenti, name='gestisci_alimenti'),
    path('paziente/<str:email>/crea-piano/', views.crea_piano, name='crea_piano'),
    path('piano/<int:pk>/', views.visualizza_piano, name='visualizza_piano'),
    path('storico/', views.visualizza_storico, name='storico_paziente'),
    path(
        'trova-alternative/<str:id_alimento>/piano/<int:pasto_id>/',
        views.trova_alternative,
        name='trova_alternative'
    ),
    path('scrivi_recensione/', views.scrivi_recensione, name='scrivi_recensione'),
    path('associa_paziente/', views.associa_paziente, name='associa_paziente'),
    path(
        'abbonamenti/',
        views.lista_abbonamenti,
        name='abbonamenti'
    ),

    path(
        'abbonamenti/acquista/<str:id_abbonamento>/',
        views.acquista_abbonamento,
        name='acquista_abbonamento'
    ),

    path('utente-by-email/', views.utente_by_email, name='utente_by_email')
]