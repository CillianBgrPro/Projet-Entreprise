from django.contrib import admin
from django.urls import path
from auth_app import views
from django.contrib.auth import views as auth_views


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
    path('export-students-csv/', views.export_students_csv, name='export_students_csv'),
    path('reinitialisation-mot-de-passe/',
         auth_views.PasswordResetView.as_view(template_name='connexion/password_reset_form.html'),
         name='password_reset'),
    path('reinitialisation-mot-de-passe/envoye/',
         auth_views.PasswordResetDoneView.as_view(template_name='connexion/password_reset_done.html'),
         name='password_reset_done'),
    path('reinitialisation-mot-de-passe/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='connexion/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reinitialisation-mot-de-passe/termine/',
         auth_views.PasswordResetCompleteView.as_view(template_name='connexion/password_reset_complete.html'),
         name='password_reset_complete'),
]