class Group_student:
    def __init__(self, id, group_id, student_id):
        self.__group_id = group_id
        self.__student_id = student_id

    def __str__(self):
        return f"Group_student(Group ID: {self.__group_id}, Student ID: {self.__student_id})"

    def get_group_id(self):
        return self.__group_id
    
    def get_student_id(self):
        return self.__student_id