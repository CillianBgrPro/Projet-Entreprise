from django.db import models

class StudentManager(models.Manager):
    """
    A custom model manager for the Student model
    for querying students based on various attributes.
    """

    # Getter methods that return a single student

    def get_by_id(self, student_id):
        """
        Get a single student by their ID.

        Args:
            student_id (int): The ID of the student to retrieve.

        Returns:
            Student: A `Student` object matching the given ID.
        
        Raises:
            models.ObjectDoesNotExist: If no student is found with the specified ID.
            models.MultipleObjectsReturned: If multiple students are found with the same ID.
        """
        return self.get(id=student_id)

    def get_by_ine(self, ine):
        """
        Get a single student by their INE (unique identifier).

        Args:
            ine (str): The INE of the student to retrieve.

        Returns:
            Student: A `Student` object matching the given INE.
        
        Raises:
            models.ObjectDoesNotExist: If no student is found with the specified INE.
            models.MultipleObjectsReturned: If multiple students are found with the same INE.
        """
        return self.get(ine=ine)

    # Getter methods that return a list of students

    def get_by_university(self, university_name):
        """
        Get students from a specific university.

        Args:
            university_name (str): The name of the university to filter by. Uses case-insensitive search.

        Returns:
            QuerySet: A `QuerySet` of `Student` objects matching the given university.
        """
        return self.filter(university__icontains=university_name)

    def get_by_speciality(self, speciality):
        """
        Get students matching a specific speciality.

        Args:
            speciality (str): The speciality to filter by. Uses case-insensitive search.

        Returns:
            QuerySet: A `QuerySet` of `Student` objects matching the given speciality.
        """
        return self.filter(speciality__icontains=speciality)

    def get_by_gender(self, gender):
        """
        Get students by their gender.

        Args:
            gender (str): The gender to filter by. Uses case-insensitive search.

        Returns:
            QuerySet: A `QuerySet` of `Student` objects matching the given gender.
        """
        return self.filter(gender__iexact=gender)

    def get_by_degree_level(self, degree_level):
        """
        Get students by their degree level.

        Args:
            degree_level (str): The degree level to filter by. Uses case-insensitive search.

        Returns:
            QuerySet: A `QuerySet` of `Student` objects matching the given degree level.
        """
        return self.filter(degree_level__iexact=degree_level)

    def get_by_year_of_study(self, year):
        """
        Get students in a specific year of study.

        Args:
            year (int): The year of study to filter by.

        Returns:
            QuerySet: A `QuerySet` of `Student` objects matching the given year of study.
        """
        return self.filter(year_of_study=year)

    def get_by_age(self, age):
        """
        Get students of a specific age.

        Args:
            age (int): The age to filter by.

        Returns:
            QuerySet: A `QuerySet` of `Student` objects matching the given age.
        """
        return self.filter(age=age)

    def get_by_rgpd_consent(self, has_consent: bool):
        """
        Get students filtered by RGPD consent status.

        Args:
            has_consent (bool): True to retrieve students who have accepted RGPD, False otherwise.

        Returns:
            QuerySet: A `QuerySet` of `Student` objects matching the given RGPD consent status.
        """
        return self.filter(rgpd_consent=bool(has_consent))

    def get_consented(self):
        """
        Get all students who have accepted the RGPD.

        Returns:
            QuerySet: A `QuerySet` of `Student` objects who have accepted the RGPD.
        """
        return self.filter(rgpd_consent=True)

    # Dynamic search method

    def search(self, university=None, speciality=None, degree_level=None, year_of_study=None, rgpd_consent=None):
        """
        Dynamic search with optional filters.

        Args:
            university (str, optional): The name of the university to filter by.
            speciality (str, optional): The speciality to filter by.
            degree_level (str, optional): The degree level to filter by.
            year_of_study (int, optional): The year of study to filter by.
            rgpd_consent (bool, optional): True to retrieve students who have accepted RGPD, False otherwise.

        Returns:
            QuerySet: A `QuerySet` of `Student` objects matching the given filters.
        """
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