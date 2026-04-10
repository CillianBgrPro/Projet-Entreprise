from django.contrib import admin
from django.urls import path
from auth_app import views
from django.contrib.auth import views as auth_views

# URL patterns for the Django project
urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # Home page
    path('', views.home, name='home'), 

    # User registration view
    path('inscription/', views.register, name='register'),
    
    # User login view
    path('connexion/', views.login_view, name='login_view'),
    
    # User logout view
    path('deconnexion/', views.logout_view, name='logout_view'),
    
    # Send verification code view
    path('envoyer-code/', views.send_code_view, name='send_code'),
    
    # Verify verification code view
    path('verifier-code/', views.verify_code, name='verify_code'),
    
    # User account management view
    path('compte/', views.account, name='account'),
    
    # Change user avatar view
    path('compte/avatar/', views.change_avatar, name='change_avatar'),
    
    # Redirect to dashboard based on user role
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    
    # Student dashboard view
    path('dashboard/etudiant/', views.student_dashboard, name='student_dashboard'),
    
    # Teacher dashboard view
    path('dashboard/professeur/', views.teacher_dashboard, name='teacher_dashboard'),
    
    # Admin dashboard view
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    
    # Export students data to CSV
    path('export-students-csv/', views.export_students_csv, name='export_students_csv'),
    
    # Password reset views using Django's built-in authentication views
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
    
    # Language selection view
    path('select-lang/<str:lang>/', views.set_language, name='set_language'),
    
    # Admin users management view
    path('administrater/', views.users, name='users'),
    
    # Log management view
    path('administrater/logs/', views.logs, name='logs'),
    
    # Data management view
    path('administrater/donnees/', views.data, name='data'),
    
    # Legal notices page
    path('mentions-legales/', views.legal_notices, name='legal_notices'),
    
    # Privacy policies page
    path('politiques-confidentialite/', views.privacy_policies, name='privacy_policies'),
    
    # Study details view
    path('details-etude/', views.study_details, name='study_details'),
    
    # Contact form view
    path('contact/', views.contact, name='contact'),
    
    # Ticket management view
    path('ticket/', views.ticket, name='ticket'),
    
    # Admin ticket management view
    path('ticket-admin/', views.ticket_admin, name='ticket_admin'),
    
    # Detailed ticket view by ID
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    
    # Change status of a ticket
    path('ticket/<int:ticket_id>/status/', views.ticket_change_status, name='ticket_change_status'),
    
    # List all tickets
    path('all-cases/', views.all_cases, name='all_cases'),
    
    # Admin training management view
    path('administrater/trainings/', views.admin_all_trainings, name='admin_all_trainings'),
    
    # Random case selection view
    path('case/random/', views.random_case, name='random_case'),
    
    # Student's training list
    path('mes-entrainements/', views.student_trainings, name='student_trainings'),
    
    # Detailed case view by ID
    path('case/<int:case_id>/', views.case_detail, name='case_detail'),
    
    # Start a case
    path('case/<int:case_id>/start/', views.start_case, name='start_case'),
    
    # Performance detail view by ID
    path('performance/<int:performance_id>/', views.performance_detail, name='performance_detail'),
    
    # Play performance
    path('performance/<int:performance_id>/play/', views.play_performance, name='play_performance'),
    
    # Dynamic data export to CSV
    path('administrater/export-dynamique/', views.dynamic_export_csv, name='dynamic_export_csv'),
    
    # Create a new case view
    path('create-case/', views.create_case, name='create_case'),
    
    # Teacher's training list
    path('dashboard/professeur/entrainements/', views.teacher_all_trainings, name='teacher_all_trainings'),
]

# a laisser pour que django puisse charger le css
from django.conf import settings
from django.urls import re_path
from django.views.static import serve

# Serve static files if not in debug mode
if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.STATICFILES_DIRS[0] if getattr(settings, 'STATICFILES_DIRS', None) else settings.STATIC_ROOT,
        }),
    ]