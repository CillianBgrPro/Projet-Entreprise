from django.db import models

class StudentManager(models.Manager):

    # getter return 1 element

    def get_by_id(self, student_id):
        #Get a single student by their ID.
        return self.get(id=student_id)

    def get_by_ine(self, ine):
        #Get a single student by their INE (unique identifier).
        return self.get(ine=ine)

    # getter return a list

    def get_by_university(self, university_name):
        #Get students from a specific university.
        return self.filter(university__icontains=university_name)

    def get_by_speciality(self, speciality):
        #Get students matching a speciality.
        return self.filter(speciality__icontains=speciality)

    def get_by_gender(self, gender):
        #Get students by gender.
        return self.filter(gender__iexact=gender)

    def get_by_degree_level(self, degree_level):
        #Get students by degree level
        return self.filter(degree_level__iexact=degree_level)

    def get_by_year_of_study(self, year):
        #Get students in a specific year of study.
        return self.filter(year_of_study=year)

    def get_by_age(self, age):
        #Get students of a specific age.
        return self.filter(age=age)

    def get_by_rgpd_consent(self, has_consent: bool):
        #Get students filtered by RGPD consent status.
        return self.filter(rgpd_consent=bool(has_consent))

    def get_consented(self):
        #Get all students who have accepted the RGPD.
        return self.filter(rgpd_consent=True)

    # dynamic search

    def search(self, university=None, speciality=None, degree_level=None, year_of_study=None, rgpd_consent=None):
        #Dynamic search with optional filters.
        search = self.all()
        if university:
            search = search.filter(university__icontains=university)
        if speciality:
            search = search.filter(speciality__icontains=speciality)
        if degree_level:
            search = search.filter(degree_level__iexact=degree_level)
        if year_of_study is not None:
            search = search.filter(year_of_study=year_of_study)
        if rgpd_consent is not None:
            search = search.filter(rgpd_consent=bool(rgpd_consent))
        return search
