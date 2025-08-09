import argparse
from datetime import datetime
from task import Task, TaskValidationError
from task_manager import TaskManager, TaskManagerError
from task_validator import TaskValidator
from reminder import print_reminders, print_tasks_by_urgency
import os

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

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_main_menu():
    """Display the main menu"""
    # Show reminders first
    print_reminders()
    
    print("\n=== Task Management System ===")
    print("1. Create Task")
    print("2. Show Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task as Completed")
    print("6. Exit")

def get_user_input(prompt, required=True, input_type=None):
    """
    Get input from user with validation
    input_type can be: None (regular input), 'date', 'status', 'priority'
    """
    while True:
        value = input(prompt).strip()
        
        if not required and not value:
            return value
            
        if not value and required:
            print("This field is required. Please try again.")
            continue
            
        if input_type == 'date':
            try:
                # Validate the date format and value
                TaskValidator.parse_due_date(value)
                return value
            except TaskValidationError as e:
                print(f"\nError: {str(e)}")
                print("Please try again.")
                continue
                
        elif input_type == 'status':
            status = STATUS_MAP.get(value)
            if not status:
                print("\nError: Invalid status ID. Must be between 1 and 3.")
                print("Please try again.")
                continue
            return status
            
        elif input_type == 'priority':
            priority = PRIORITY_MAP.get(value)
            if not priority:
                print("\nError: Invalid priority level ID. Must be between 1 and 3.")
                print("Please try again.")
                continue
            return priority
            
        return value

def create_task():
    """Get task details from user and create task"""
    print("\n=== Create New Task ===")
    
    task_manager = None
    try:
        # Get task details
        title = get_user_input("Enter task title: ")
        description = get_user_input("Enter task description: ")
        
        # Get status
        print("\nStatus options:")
        for key, value in STATUS_MAP.items():
            print(f"{key} - {value}")
        status = get_user_input("Enter status (1-3): ", input_type='status')
        
        # Get priority
        print("\nPriority levels:")
        for key, value in PRIORITY_MAP.items():
            print(f"{key} - {value}")
        priority = get_user_input("Enter priority level (1-3): ", input_type='priority')
        
        # Get due date with validation
        due_date = get_user_input("Enter due date (MM/DD/YYYY): ", input_type='date')
        
        # Create task through task manager
        task_data = {
            'title': title,
            'description': description,
            'status': status,
            'priority_level': priority,
            'due_date': due_date
        }
        
        task_manager = TaskManager()
        saved_task = task_manager.create_task(task_data)
        
        print("\nTask created successfully!")
        print_task(saved_task)
        input("\nPress Enter to continue...")
        
    except TaskManagerError as e:
        print(f"\nError saving task: {e}")
        input("\nPress Enter to continue...")
    finally:
        if task_manager:
            task_manager.close()
        clear_screen()

def print_task(task_data):
    """Print task details in a formatted way"""
    print(f"\nTask {task_data['id']}:")
    print(f"  Title: {task_data['title']}")
    print(f"  Description: {task_data['description']}")
    
    # Get status text directly from status_code
    status_code = task_data['status_code']
    print(f"  Status: {status_code}")
    
    # Get priority text directly from priority_code
    priority_code = task_data['priority_level_code']
    print(f"  Priority: {priority_code}")
    
    print(f"  Due Date: {task_data['due_date']}")
    if 'created_at' in task_data:
        print(f"  Created: {task_data['created_at']}")
    if 'updated_at' in task_data:
        print(f"  Updated: {task_data['updated_at']}")

def show_tasks():
    """Display tasks based on user selection"""
    print("\n=== Show Tasks ===")
    print("1. Show all tasks")
    print("2. Show task by ID")
    print("3. Show tasks by status")
    print("4. Show tasks by priority")
    print("5. Show tasks by urgency")
    
    task_manager = None
    try:
        choice = get_user_input("Enter your choice (1-5): ")
        task_manager = TaskManager()
        
        if choice == "1":
            tasks = task_manager.get_all_tasks()
            if tasks:
                for task in tasks:
                    print_task(task)
            else:
                print("\nNo tasks found.")
                
        elif choice == "2":
            task_id = get_user_input("Enter task ID: ")
            task = task_manager.get_task(task_id)
            if task:
                print_task(task)
            else:
                print("\nTask not found.")
                
        elif choice == "3":
            print("\nStatus options:")
            for key, value in STATUS_MAP.items():
                print(f"{key} - {value}")
            status = get_user_input("Enter status (1-3): ", input_type='status')
            tasks = task_manager.get_tasks_by_status(status)
            if tasks:
                for task in tasks:
                    print_task(task)
            else:
                print("\nNo tasks found with this status.")
                
        elif choice == "4":
            print("\nPriority levels:")
            for key, value in PRIORITY_MAP.items():
                print(f"{key} - {value}")
            priority = get_user_input("Enter priority level (1-3): ", input_type='priority')
            tasks = task_manager.get_tasks_by_priority(priority)
            if tasks:
                for task in tasks:
                    print_task(task)
            else:
                print("\nNo tasks found with this priority level.")
        elif choice == "5":
            print_tasks_by_urgency()
        else:
            print("\nInvalid choice.")
            
        input("\nPress Enter to continue...")
            
    except TaskManagerError as e:
        print(f"\nError retrieving tasks: {e}")
        input("\nPress Enter to continue...")
    finally:
        if task_manager:
            task_manager.close()
        clear_screen()

def update_task():
    """Get updated task details from user"""
    print("\n=== Update Task ===")
    
    task_manager = None
    try:
        task_manager = TaskManager()
        task_id = get_user_input("Enter task ID to update: ")
        task = task_manager.get_task(task_id)
        
        if not task:
            print("\nTask not found.")
            input("\nPress Enter to continue...")
            return
            
        print("\nCurrent task details:")
        print_task(task)
        print("\nLeave field empty to keep current value")
        
        # Get updated values
        update_data = {}
        
        title = get_user_input("Enter new title (or press Enter to skip): ", required=False)
        if title:
            update_data['title'] = title
            
        description = get_user_input("Enter new description (or press Enter to skip): ", required=False)
        if description:
            update_data['description'] = description
            
        # Get status
        print("\nStatus options:")
        for key, value in STATUS_MAP.items():
            print(f"{key} - {value}")
        status = get_user_input("Enter new status (1-3, or press Enter to skip): ", required=False, input_type='status')
        if status:
            update_data['status'] = status
            
        # Get priority
        print("\nPriority levels:")
        for key, value in PRIORITY_MAP.items():
            print(f"{key} - {value}")
        priority = get_user_input("Enter new priority (1-3, or press Enter to skip): ", required=False, input_type='priority')
        if priority:
            update_data['priority_level'] = priority
            
        # Get due date with validation
        due_date = get_user_input("Enter new due date (MM/DD/YYYY, or press Enter to skip): ", required=False, input_type='date')
        if due_date:
            update_data['due_date'] = due_date
        
        # Update through task manager
        if update_data:
            updated_task = task_manager.update_task(task_id, update_data)
            print("\nTask updated successfully!")
            print_task(updated_task)
        else:
            print("\nNo changes made.")
            
        input("\nPress Enter to continue...")
        
    except TaskManagerError as e:
        print(f"\nError updating task: {e}")
        input("\nPress Enter to continue...")
    finally:
        if task_manager:
            task_manager.close()
        clear_screen()

def delete_task():
    """Delete task after confirmation"""
    print("\n=== Delete Task ===")
    
    task_manager = None
    try:
        task_manager = TaskManager()
        task_id = get_user_input("Enter task ID to delete: ")
        task = task_manager.get_task(task_id)
        
        if not task:
            print("\nTask not found.")
            input("\nPress Enter to continue...")
            return
            
        print("\nTask to delete:")
        print_task(task)
        
        confirm = input("\nAre you sure you want to delete this task? (y/n): ").lower()
        if confirm == 'y':
            task_manager.delete_task(task_id)
            print("\nTask deleted successfully!")
        else:
            print("\nDeletion cancelled.")
            
        input("\nPress Enter to continue...")
            
    except TaskManagerError as e:
        print(f"\nError deleting task: {e}")
        input("\nPress Enter to continue...")
    finally:
        if task_manager:
            task_manager.close()
        clear_screen()

def mark_task_completed():
    """Mark a task as completed"""
    print("\n=== Mark Task as Completed ===")
    
    task_manager = None
    try:
        task_manager = TaskManager()
        task_id = get_user_input("Enter task ID to mark as completed: ")
        task = task_manager.get_task(task_id)
        
        if not task:
            print("\nTask not found.")
            input("\nPress Enter to continue...")
            return
            
        if task['is_completed']:
            print("\nThis task is already marked as completed.")
            input("\nPress Enter to continue...")
            return
            
        print("\nCurrent task details:")
        print_task(task)
        
        confirm = input("\nAre you sure you want to mark this task as completed? (y/n): ").lower()
        if confirm == 'y':
            updated_task = task_manager.mark_as_completed(task_id)
            print("\nTask marked as completed successfully!")
            print_task(updated_task)
        else:
            print("\nOperation cancelled.")
            
        input("\nPress Enter to continue...")
            
    except TaskManagerError as e:
        print(f"\nError marking task as completed: {e}")
        input("\nPress Enter to continue...")
    finally:
        if task_manager:
            task_manager.close()
        clear_screen()

def main():
    while True:
        show_main_menu()
        choice = get_user_input("Enter your choice (1-6): ")
        
        if choice == "1":
            clear_screen()
            create_task()
        elif choice == "2":
            clear_screen()
            show_tasks()
        elif choice == "3":
            clear_screen()
            update_task()
        elif choice == "4":
            clear_screen()
            delete_task()
        elif choice == "5":
            clear_screen()
            mark_task_completed()
        elif choice == "6":
            clear_screen()
            print("Goodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")
            input("\nPress Enter to continue...")
            clear_screen()

if __name__ == "__main__":
    main()
