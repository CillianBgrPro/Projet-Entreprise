class Group_professor:
    def __init__(self, professor_id, group_id):
        self.professor_id = professor_id
        self.group_id = group_id

    def __str__(self):
        return f"Professor ID: {self.professor_id}, Group ID: {self.group_id}"

    def get_professor_id(self):
        return self.professor_id

    def get_group_id(self):
        return self.group_id
    
    def set_professor_id(self, professor_id):
        self.professor_id = professor_id