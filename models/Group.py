class Group:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        
    def __str__(self):
        return f"Group ID: {self.id}, Name: {self.name}"
    
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name