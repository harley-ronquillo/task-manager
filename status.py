class Status:
    def __init__(self, status_code):
        self.status_code = status_code
        self.statuses = {
            "PENDING": "Pending",
            "IN_PROGRESS": "In Progress",
            "COMPLETED": "Completed",
        }
        self.stored_statuses = {}
        for code, status in self.statuses.items():
            self.stored_statuses[code] = status

    def get_status(self, status_code):
        return self.stored_statuses.get(status_code, "Unknown")

    def get_status_code(self, status):
        return list(self.stored_statuses.keys())[list(self.stored_statuses.values()).index(status)]
    