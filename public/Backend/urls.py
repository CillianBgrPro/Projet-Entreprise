from django.contrib import admin
from django.urls import path
from auth_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accueil, name='accueil'), 
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('envoyer-code/', views.envoyer_code_view, name='envoyer_code'),
    path('verifier-code/', views.verifier_code, name='verifier_code'),
    path('compte/', views.compte, name='compte'),
    path('dashboard/etudiant/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/professeur/', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
]