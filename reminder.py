from datetime import datetime, timedelta
from task_manager import TaskManager


def get_tasks_with_days_left():
    """Get all tasks with their days left calculation"""
    try:
        task_manager = TaskManager()
        tasks = task_manager.get_all_tasks()
        
        if not tasks:
            return []
            
        # Get current date
        current_date = datetime.now()
        
        # Calculate days left for all tasks
        tasks_with_days = []
        for task in tasks:
            due_date = datetime.strptime(str(task['due_date']), '%Y-%m-%d %H:%M:%S')
            days_left = (due_date - current_date).days
            tasks_with_days.append({
                'id': task['id'],
                'title': task['title'],
                'description': task['description'],
                'due_date': due_date.strftime('%m/%d/%Y'),
                'days_left': days_left,
                'status': task['status_code'],
                'priority': task['priority_level_code']
            })
        
        # Sort by days left
        tasks_with_days.sort(key=lambda x: x['days_left'])
        return tasks_with_days
        
    finally:
        if 'task_manager' in locals():
            task_manager.close()


def get_upcoming_tasks():
    """Get tasks that are due within a month"""
    tasks = get_tasks_with_days_left()
    
    # Filter tasks due within 30 days
    current_date = datetime.now()
    one_month_later = current_date + timedelta(days=30)
    
    return [task for task in tasks if task['days_left'] >= 0 and task['days_left'] <= 30]


def print_reminders():
    """Print reminders for tasks due within a month"""
    upcoming_tasks = get_upcoming_tasks()
    
    if not upcoming_tasks:
        return
    
    print("\n=== UPCOMING TASKS (Due within 30 days) ===")
    print("--------------------------------------------")
    for task in upcoming_tasks:
        print(f"Task {task['id']}: {task['title']}")
        print(f"Status: {task['status']}")
        if task['days_left'] == 0:
            print("Due: TODAY!")
        elif task['days_left'] == 1:
            print("Due: TOMORROW!")
        else:
            print(f"Due in {task['days_left']} days ({task['due_date']})")
        print("--------------------------------------------")


def print_tasks_by_urgency():
    """Print all tasks sorted by urgency"""
    tasks = get_tasks_with_days_left()
    
    if not tasks:
        print("\nNo tasks found.")
        return
        
    # Split tasks into urgent (due within 30 days) and non-urgent
    urgent_tasks = []
    non_urgent_tasks = []
    
    for task in tasks:
        if 0 <= task['days_left'] <= 30:
            urgent_tasks.append(task)
        else:
            non_urgent_tasks.append(task)
    
    # Print urgent tasks
    if urgent_tasks:
        print("\n=== URGENT TASKS (Due within 30 days) ===")
        print("--------------------------------------------")
        for task in urgent_tasks:
            print(f"Task {task['id']}: {task['title']}")
            print(f"Description: {task['description']}")
            print(f"Status: {task['status']}")
            print(f"Priority: {task['priority']}")
            if task['days_left'] == 0:
                print("Due: TODAY!")
            elif task['days_left'] == 1:
                print("Due: TOMORROW!")
            else:
                print(f"Due in {task['days_left']} days ({task['due_date']})")
            print("--------------------------------------------")
    
    # Print non-urgent tasks
    if non_urgent_tasks:
        print("\n=== NON-URGENT TASKS ===")
        print("--------------------------------------------")
        for task in non_urgent_tasks:
            print(f"Task {task['id']}: {task['title']}")
            print(f"Description: {task['description']}")
            print(f"Status: {task['status']}")
            print(f"Priority: {task['priority']}")
            print(f"Due: {task['due_date']} (in {task['days_left']} days)")
            print("--------------------------------------------")
