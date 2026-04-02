from django.contrib import admin
from .models import (
    User, Student, Professor, Group, 
    ClinicalCase, Training, StudentPerformance,
    Ticket, StartingSituation
)

#pour l'afffichage sur le webbb
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Group)
admin.site.register(ClinicalCase)
admin.site.register(Training)
admin.site.register(StudentPerformance)
admin.site.register(Ticket)
admin.site.register(StartingSituation)