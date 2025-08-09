class PriorityLevel:
    def __init__(self, priority_level):
        self.priority_level = priority_level
        
        self.priority_levels = {
            "LOW": "Low",
            "MEDIUM": "Medium",
            "HIGH": "High",
        }
        
        self.stored_priority_levels = {}
        for code, priority_level in self.priority_levels.items():
            self.stored_priority_levels[code] = priority_level
            
    def get_priority_level(self, priority_level):
        return self.stored_priority_levels.get(priority_level, "Unknown")
    
    def get_priority_level_code(self, priority_level):
        return list(self.stored_priority_levels.keys())[list(self.stored_priority_levels.values()).index(priority_level)]