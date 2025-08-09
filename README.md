# Task Management System

A command-line task management system built with Python and MySQL. The system allows users to create, view, update, and delete tasks with status tracking, priority levels, and due date management.

## Features

- **Task Management**
  - Create new tasks with title, description, status, priority, and due date
  - View all tasks or filter by status/priority
  - Update existing tasks
  - Delete tasks
  - Automatic task reminders for items due within 30 days

- **Status Tracking**
  - Pending
  - In Progress
  - Completed

- **Priority Levels**
  - Low
  - Medium
  - High

- **Data Validation**
  - Required field validation
  - Date format validation (MM/DD/YYYY)
  - Future date validation for due dates
  - Status and priority level validation

## Prerequisites

- Python 3.x
- MySQL Server
- PyMySQL package
- python-dotenv package

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd task-management-system
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your MySQL credentials:
   ```
   DB_HOST=localhost
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_NAME=your_database_name
   ```

4. Run the application:
   ```bash
   python app.py
   ```

## Project Structure

- `app.py` - Main CLI interface
- `database.py` - Database connection and table management
- `task.py` - Task class definition and validation
- `task_manager.py` - Task CRUD operations
- `task_validator.py` - Input validation logic
- `status.py` - Status code management
- `priority_level.py` - Priority level management
- `reminder.py` - Task reminder functionality

## Usage

### Main Menu
```
=== Task Management System ===
1. Create Task
2. Show Tasks
3. Update Task
4. Delete Task
5. Exit
```

### Creating a Task
1. Enter task title
2. Enter task description
3. Select status (1-3):
   - 1 - Pending
   - 2 - In Progress
   - 3 - Completed
4. Select priority (1-3):
   - 1 - Low
   - 2 - Medium
   - 3 - High
5. Enter due date (MM/DD/YYYY)

### Viewing Tasks
- View all tasks
- View task by ID
- Filter tasks by status
- Filter tasks by priority

### Task Reminders
The system automatically displays tasks due within the next 30 days at the top of the main menu, including:
- Tasks due today
- Tasks due tomorrow
- Tasks due within the month

## Database Schema

### Tasks Table
- id (INT, AUTO_INCREMENT, PRIMARY KEY)
- title (VARCHAR(100))
- description (TEXT)
- status_id (INT, FOREIGN KEY)
- priority_level_id (INT, FOREIGN KEY)
- due_date (DATETIME)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

### Statuses Table
- id (INT, AUTO_INCREMENT, PRIMARY KEY)
- status_code (VARCHAR(20))

### Priority Levels Table
- id (INT, AUTO_INCREMENT, PRIMARY KEY)
- priority_level_code (VARCHAR(20))

## Error Handling

The system includes comprehensive error handling for:
- Database connection issues
- Invalid input validation
- Missing required fields
- Invalid date formats
- Past due dates
- Invalid status/priority codes

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 