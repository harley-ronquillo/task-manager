from datetime import datetime

class TaskValidationError(Exception):
    """Custom exception for task validation errors"""
    pass

class TaskValidator:
    # Map IDs to status codes
    STATUS_MAP = {
        "1": "PENDING",
        "2": "IN_PROGRESS",
        "3": "COMPLETED"
    }

    # Map IDs to priority codes
    PRIORITY_MAP = {
        "1": "LOW",
        "2": "MEDIUM",
        "3": "HIGH"
    }

    @staticmethod
    def validate_fields(title, description, status, priority_level, due_date):
        """Validate required fields"""
        missing_fields = []
        
        # Check for empty values
        if not title or not title.strip():
            missing_fields.append("title")
        if not description or not description.strip():
            missing_fields.append("description")
        if not status:
            missing_fields.append("status")
        if not priority_level:
            missing_fields.append("priority level")
        if not due_date:
            missing_fields.append("due date")
        
        if missing_fields:
            raise TaskValidationError(f"Missing required fields: {', '.join(missing_fields)}")

        # Validate status and priority level values
        if status not in TaskValidator.STATUS_MAP.values():
            raise TaskValidationError(f"Invalid status code: {status}")

        if priority_level not in TaskValidator.PRIORITY_MAP.values():
            raise TaskValidationError(f"Invalid priority level code: {priority_level}")

    @staticmethod
    def validate_date_parts(month, day, year):
        """Validate individual date components"""
        current_date = datetime.now()
        
        # Validate month (1-12)
        if not (1 <= month <= 12):
            raise TaskValidationError(f"Month must be between 1 and 12, got {month}")
            
        # Validate day (1-31)
        # Get the actual max days for the given month
        month_days = {
            1: 31,  # January
            2: 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,  # February (leap year check)
            3: 31,  # March
            4: 30,  # April
            5: 31,  # May
            6: 30,  # June
            7: 31,  # July
            8: 31,  # August
            9: 30,  # September
            10: 31,  # October
            11: 30,  # November
            12: 31   # December
        }
        max_days = month_days[month]
        
        if not (1 <= day <= max_days):
            raise TaskValidationError(f"Day must be between 1 and {max_days} for month {month}, got {day}")
            
        # Create the date object for comparison
        try:
            input_date = datetime(year, month, day)
            current_date = datetime(current_date.year, current_date.month, current_date.day)
            
            # Check if the date is in the past
            if input_date < current_date:
                raise TaskValidationError("Due date cannot be in the past")
                
        except ValueError as e:
            raise TaskValidationError(f"Invalid date: {str(e)}")

    @staticmethod
    def parse_due_date(due_date):
        """Parse and validate due date in MM/DD/YYYY format"""
        if isinstance(due_date, datetime):
            # If it's already a datetime, validate it's not in the past
            current_date = datetime.now()
            if due_date.date() < current_date.date():
                raise TaskValidationError("Due date cannot be in the past")
            return due_date
            
        try:
            # First check the format strictly
            if not due_date.count('/') == 2:
                raise TaskValidationError("Due date must be in MM/DD/YYYY format")
            
            # Split and convert parts
            try:
                month_str, day_str, year_str = due_date.split('/')
                month = int(month_str)
                day = int(day_str)
                year = int(year_str)
            except ValueError:
                raise TaskValidationError("Month, day, and year must be valid numbers")
            
            # Validate the individual parts
            TaskValidator.validate_date_parts(month, day, year)
            
            # If all validation passes, create the datetime object
            return datetime(year, month, day)
            
        except ValueError as e:
            if "day is out of range for month" in str(e):
                raise TaskValidationError(f"Invalid day for the given month")
            raise TaskValidationError("Invalid due date format. Use MM/DD/YYYY format")

    @staticmethod
    def format_date_for_display(date):
        """Format a datetime object to MM/DD/YYYY string"""
        return date.strftime("%m/%d/%Y")

    @staticmethod
    def format_date_for_db(date):
        """Format a datetime object for database storage"""
        return date.strftime("%Y-%m-%d %H:%M:%S") 