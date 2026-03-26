class Training:
    def __init__(self,id, group_id, case_id, professor_id, status, created_at, finished_at):
        self.__id = id
        self.__group_id = group_id
        self.__case_id = case_id
        self.__professor_id = professor_id
        self.__status = status
        self.__created_at = created_at
        self.__finished_at = finished_at

    def __str__(self):
        return f"Training(ID: {self.__id}, Group ID: {self.__group_id}, Case ID: {self.__case_id},
        Professor ID: {self.__professor_id}, Status: {self.__status}, Created At: {self.__created_at},
        Finished At: {self.__finished_at})"

    def get_id(self):
        return self.__id

    def get_group_id(self):
        return self.__group_id
    
    def get_case_id(self):
        return self.__case_id
    
    def get_professor_id(self):
        return self.__professor_id
    
    def get_status(self):
        return self.__status
    
    def get_created_at(self):
        return self.__created_at
    
    def get_finished_at(self):
        return self.__finished_at
    
    def set_status(self, status):
        self.__status = status
    
    def set_finished_at(self, finished_at):
        if type(finished_at) == str:
            self.__finished_at = datetime.strptime(finished_at, "%Y-%m-%d %H:%M:%S")
        else:
            print("Invalid type for finished_at. Expected string in format 'YYYY-MM-DD HH:MM:SS'.")