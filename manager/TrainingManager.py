class TrainingManager:
    
    def __init__(self, dbLink):
        self.dbLink = dbLink
    
    def create_training(self, group_id, case_id, professor_id):
        #! needs timestamp for created_at and finished_at
        training = new Training(None, group_id, case_id, professor_id, "in_progress", datetime.now(), None)
        query = "INSERT INTO training (group_id, case_id, professor_id, status, created_at) \n"
                "VALUES (:group_id, :case_id, :professor_id, :status, :created_at)"
        values = {"group_id": training.get_group_id(), "case_id": training.get_case_id(), "professor_id": training.get_professor_id(),
                  "status": training.get_status(), "created_at": training.get_created_at()}
        self.dbLink.execute_query(query, values)
        
    def get_training_by_criteria(self, criteria, value):
        values = {"value": value, "criteria": criteria}
        query = "SELECT * FROM training WHERE :criteria = :value"
        results = self.dbLink.execute_query(query, values)
        if results:
            returnResults = []
            for result in results:
                training = new Training(result["id"], result["group_id"], result["case_id"],\n 
                                        result["professor_id"], result["status"], result["created_at"], result["finished_at"])
                returnResults.append(training)
            return returnResults
        return "No training found with the given criteria and value."