class Professor:
    def __init__(self, id, user_id, specialty, university, rgpd_consent, department):
        self.__id = id
        self.__user_id = user_id
        self.__specialty = specialty
        self.__university = university
        self.__rgpd_consent = rgpd_consent
        self.__department = department

    def __str__(self):
        return f"Professor {self.__id} from {self.__department} department 
        at {self.__university} with specialty in {self.__specialty} (RGPD Consent: {self.__rgpd_consent})"
    
    def get_id(self):
        return self.__id
    
    def get_user_id(self):
        return self.__user_id
    
    def get_specialty(self):
        return self.__specialty
    
    def get_university(self):
        return self.__university
    
    def get_rgpd_consent(self):
        return self.__rgpd_consent
    
    def get_department(self):
        return self.__department
    
    def set_specialty(self, specialty):
        self.__specialty = specialty
        
    def set_university(self, university):
        self.__university = university
    
    def set_rgpd_consent(self, rgpd_consent):
        self.__rgpd_consent = rgpd_consent
    
    def set_department(self, department):
        self.__department = department