import argparse
from datetime import datetime
from status import Status
from priority_level import PriorityLevel
from task_validator import TaskValidator, TaskValidationError


class Task:
    def __init__(self, title, description, status, priority_level, due_date,
                 task_id=None, created_at=None, updated_at=None):
        try:
            TaskValidator.validate_fields(
                title, description, status, priority_level, due_date)
            
            self.task_id = task_id
            self.title = title.strip()
            self.description = description.strip()
            self.status = Status(status_code=status)
            self.priority_level = PriorityLevel(priority_level=priority_level)
            self.due_date = TaskValidator.parse_due_date(due_date)
            self.created_at = created_at or datetime.now()
            self.updated_at = updated_at or datetime.now()
            
        except TaskValidationError as e:
            raise TaskValidationError(str(e))
        except Exception as e:
            raise TaskValidationError(f"Error creating task: {str(e)}")

    def to_dict(self):
        """Convert task to dictionary for database operations"""
        return {
            'id': self.task_id,
            'title': self.title,
            'description': self.description,
            'status_code': self.status.status_code,
            'priority_level_code': self.priority_level.priority_level,
            'due_date': TaskValidator.format_date_for_db(self.due_date),
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Task instance from a dictionary (e.g., database result)"""
        return cls(
            title=data['title'],
            description=data['description'],
            status=data['status_code'],
            priority_level=data['priority_level_code'],
            due_date=data['due_date'],
            task_id=data.get('id'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

    def update(self, title=None, description=None, status=None,
              priority_level=None, due_date=None):
        """Update task attributes with validation"""
        try:
            # Use current values for any fields not being updated
            new_title = title if title is not None else self.title
            new_description = description if description is not None else self.description
            new_status = status if status is not None else self.status.status_code
            new_priority = priority_level if priority_level is not None else self.priority_level.priority_level
            new_due_date = due_date if due_date is not None else TaskValidator.format_date_for_display(self.due_date)

            # Validate all fields together
            TaskValidator.validate_fields(
                new_title, new_description, new_status,
                new_priority, new_due_date)

            # If validation passes, update the fields
            if title is not None:
                self.title = title.strip()
            if description is not None:
                self.description = description.strip()
            if status is not None:
                self.status = Status(status_code=status)
            if priority_level is not None:
                self.priority_level = PriorityLevel(priority_level=priority_level)
            if due_date is not None:
                self.due_date = TaskValidator.parse_due_date(due_date)
            
            self.updated_at = datetime.now()
            
        except TaskValidationError as e:
            raise TaskValidationError(str(e))
        except Exception as e:
            raise TaskValidationError(f"Error updating task: {str(e)}")

    def __str__(self):
        """String representation of the task"""
        return (
            f"Task {self.task_id}:\n"
            f"  Title: {self.title}\n"
            f"  Description: {self.description}\n"
            f"  Status: {self.status.get_status_message(self.status.status_code)}\n"
            f"  Priority: {self.priority_level.get_priority_level(self.priority_level.priority_level)}\n"
            f"  Due Date: {TaskValidator.format_date_for_display(self.due_date)}\n"
            f"  Created: {self.created_at.strftime('%m/%d/%Y %H:%M:%S')}\n"
            f"  Updated: {self.updated_at.strftime('%m/%d/%Y %H:%M:%S')}"
        )

    def get_task_id(self):
        return self.task_id
    
        