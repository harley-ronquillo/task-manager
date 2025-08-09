from database import Database
from task import Task
from status import Status
from priority_level import PriorityLevel
import pymysql

class TaskManagerError(Exception):
    """Custom exception for database operation errors"""
    pass

class TaskManager:
    def __init__(self):
        """Initialize database connection and ensure lookup data exists"""
        self.db = Database()
        self.db.create_tables()
        self._init_lookup_data()

    def _init_lookup_data(self):
        """Initialize status and priority level data"""
        try:
            with self.db.connection.cursor() as cursor:
                # Get default values from Status and PriorityLevel classes
                status = Status("")
                priority = PriorityLevel("")

                # Insert status codes if they don't exist
                for status_code in status.stored_statuses.keys():
                    cursor.execute("""
                        INSERT IGNORE INTO statuses (status_code) 
                        VALUES (%s)
                    """, (status_code,))

                # Insert priority levels if they don't exist
                for priority_code in priority.stored_priority_levels.keys():
                    cursor.execute("""
                        INSERT IGNORE INTO priority_levels (priority_level_code) 
                        VALUES (%s)
                    """, (priority_code,))

                self.db.connection.commit()
        except pymysql.Error as e:
            raise TaskManagerError(f"Error initializing lookup data: {str(e)}")

    def get_status_id(self, status_code):
        """Get status ID from status code"""
        try:
            with self.db.connection.cursor() as cursor:
                query = "SELECT id FROM statuses WHERE status_code = %s"
                cursor.execute(query, (status_code,))
                result = cursor.fetchone()
                if result:
                    return result['id']
                raise TaskManagerError(f"Invalid status code: {status_code}")
        except pymysql.Error as e:
            raise TaskManagerError(f"Error getting status ID: {str(e)}")

    def get_priority_id(self, priority_code):
        """Get priority level ID from priority code"""
        try:
            with self.db.connection.cursor() as cursor:
                query = "SELECT id FROM priority_levels WHERE priority_level_code = %s"
                cursor.execute(query, (priority_code,))
                result = cursor.fetchone()
                if result:
                    return result['id']
                raise TaskManagerError(f"Invalid priority level code: {priority_code}")
        except pymysql.Error as e:
            raise TaskManagerError(f"Error getting priority level ID: {str(e)}")

    def create_task(self, task_data):
        """Create a new task in database"""
        try:
            # Create Task object for validation and conversion
            task = Task(
                title=task_data['title'],
                description=task_data['description'],
                status=task_data['status'],
                priority_level=task_data['priority_level'],
                due_date=task_data['due_date']
            )
            
            # Convert to dictionary for database
            task_dict = task.to_dict()
            
            # Get IDs for status and priority level
            status_id = self.get_status_id(task_dict['status_code'])
            priority_id = self.get_priority_id(task_dict['priority_level_code'])
            
            # Insert into database
            with self.db.connection.cursor() as cursor:
                query = """
                    INSERT INTO tasks (title, description, status_id, priority_level_id, due_date)
                    VALUES (%s, %s, %s, %s, %s)
                """
                values = (
                    task_dict['title'],
                    task_dict['description'],
                    status_id,
                    priority_id,
                    task_dict['due_date']
                )
                
                cursor.execute(query, values)
                task_id = cursor.lastrowid
                self.db.connection.commit()
                
                # Get the created task
                return self.get_task(task_id)
                
        except pymysql.Error as e:
            raise TaskManagerError(f"Error creating task: {str(e)}")

    def mark_as_completed(self, task_id):
        """Mark a task as completed"""
        try:
            # First check if task exists
            task = self.get_task(task_id)
            if not task:
                raise TaskManagerError(f"Task {task_id} not found")

            # Get the status ID for "COMPLETED"
            completed_status = self.get_status_id("COMPLETED")
                
            # Update task to mark as completed and change status
            with self.db.connection.cursor() as cursor:
                query = """
                    UPDATE tasks 
                    SET is_completed = TRUE,
                        status_id = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """
                cursor.execute(query, (completed_status, task_id))
                self.db.connection.commit()
                
                # Get the updated task
                return self.get_task(task_id)
                
        except pymysql.Error as e:
            raise TaskManagerError(f"Error marking task as completed: {str(e)}")


    def get_task(self, task_id):
        """Get task from database by ID"""
        try:
            with self.db.connection.cursor() as cursor:
                query = """
                    SELECT 
                        t.id,
                        t.title,
                        t.description,
                        t.due_date,
                        t.is_completed,
                        t.created_at,
                        t.updated_at,
                        s.status_code,
                        p.priority_level_code
                    FROM tasks t
                    JOIN statuses s ON t.status_id = s.id
                    JOIN priority_levels p ON t.priority_level_id = p.id
                    WHERE t.id = %s
                """
                cursor.execute(query, (task_id,))
                return cursor.fetchone()
        except pymysql.Error as e:
            raise TaskManagerError(f"Error retrieving task: {str(e)}")

    def get_all_tasks(self):
        """Get all tasks from database"""
        try:
            with self.db.connection.cursor() as cursor:
                query = """
                    SELECT 
                        t.id,
                        t.title,
                        t.description,
                        t.due_date,
                        t.is_completed,
                        t.created_at,
                        t.updated_at,
                        s.status_code,
                        p.priority_level_code
                    FROM tasks t
                    JOIN statuses s ON t.status_id = s.id
                    JOIN priority_levels p ON t.priority_level_id = p.id
                """
                cursor.execute(query)
                return cursor.fetchall()
        except pymysql.Error as e:
            raise TaskManagerError(f"Error retrieving tasks: {str(e)}")

    def get_tasks_by_status(self, status):
        """Get tasks by status from database"""
        try:
            with self.db.connection.cursor() as cursor:
                query = """
                    SELECT 
                        t.id,
                        t.title,
                        t.description,
                        t.due_date,
                        t.is_completed,
                        t.created_at,
                        t.updated_at,
                        s.status_code,
                        p.priority_level_code
                    FROM tasks t
                    JOIN statuses s ON t.status_id = s.id
                    JOIN priority_levels p ON t.priority_level_id = p.id
                    WHERE s.status_code = %s
                """
                cursor.execute(query, (status,))
                return cursor.fetchall()
        except pymysql.Error as e:
            raise TaskManagerError(f"Error retrieving tasks by status: {str(e)}")

    def get_tasks_by_priority(self, priority):
        """Get tasks by priority from database"""
        try:
            with self.db.connection.cursor() as cursor:
                query = """
                    SELECT 
                        t.id,
                        t.title,
                        t.description,
                        t.due_date,
                        t.is_completed,
                        t.created_at,
                        t.updated_at,
                        s.status_code,
                        p.priority_level_code
                    FROM tasks t
                    JOIN statuses s ON t.status_id = s.id
                    JOIN priority_levels p ON t.priority_level_id = p.id
                    WHERE p.priority_level_code = %s
                """
                cursor.execute(query, (priority,))
                return cursor.fetchall()
        except pymysql.Error as e:
            raise TaskManagerError(f"Error retrieving tasks by priority: {str(e)}")

    def update_task(self, task_id, update_data):
        """Update task in database"""
        try:
            # Get current task data
            current_task = self.get_task(task_id)
            if not current_task:
                raise TaskManagerError(f"Task {task_id} not found")

            # Create Task object with updated data
            task = Task(
                title=update_data.get('title', current_task['title']),
                description=update_data.get('description', current_task['description']),
                status=update_data.get('status', current_task['status_code']),
                priority_level=update_data.get('priority_level', current_task['priority_level_code']),
                due_date=update_data.get('due_date', current_task['due_date']),
                task_id=task_id
            )

            # Convert to dictionary and get IDs
            task_dict = task.to_dict()
            status_id = self.get_status_id(task_dict['status_code'])
            priority_id = self.get_priority_id(task_dict['priority_level_code'])
            
            # Update in database
            with self.db.connection.cursor() as cursor:
                query = """
                    UPDATE tasks 
                    SET title = %s,
                        description = %s,
                        status_id = %s,
                        priority_level_id = %s,
                        due_date = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """
                values = (
                    task_dict['title'],
                    task_dict['description'],
                    status_id,
                    priority_id,
                    task_dict['due_date'],
                    task_id
                )
                
                cursor.execute(query, values)
                self.db.connection.commit()
                
                # Get the updated task
                return self.get_task(task_id)
                
        except pymysql.Error as e:
            raise TaskManagerError(f"Error updating task: {str(e)}")

    def delete_task(self, task_id):
        """Delete task from database"""
        try:
            with self.db.connection.cursor() as cursor:
                query = "DELETE FROM tasks WHERE id = %s"
                cursor.execute(query, (task_id,))
                self.db.connection.commit()
                return cursor.rowcount > 0
        except pymysql.Error as e:
            raise TaskManagerError(f"Error deleting task: {str(e)}")

    def __del__(self):
        """Ensure database connection is closed"""
        if hasattr(self, 'db'):
            self.db.close()

    def close(self):
        """Explicitly close the database connection"""
        if hasattr(self, 'db'):
            self.db.close()