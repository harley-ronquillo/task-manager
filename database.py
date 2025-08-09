import os
import pymysql
from dotenv import load_dotenv
from status import Status
from priority_level import PriorityLevel

load_dotenv()

class Database:
    def __init__(self):
        self.connection = None
        try:
            self.connection = pymysql.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME'),
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Successfully connected to MySQL database")
            
            # Initialize Status and PriorityLevel to get their values
            self.status_manager = Status("")
            self.priority_manager = PriorityLevel("")
            
        except pymysql.Error as e:
            print(f"Error connecting to MySQL: {e}")

    def create_tables(self):
        if self.connection is None:
            print("No database connection")
            return

        try:
            with self.connection.cursor() as cursor:
                # Create status table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS statuses (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        status_code VARCHAR(20) UNIQUE NOT NULL
                    )
                """)

                # Create priority levels table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS priority_levels (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        priority_level_code VARCHAR(20) UNIQUE NOT NULL
                    )
                """)

                # Create tasks table with foreign keys
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        title VARCHAR(100) NOT NULL,
                        description TEXT NOT NULL,
                        status_id INT NOT NULL,
                        priority_level_id INT NOT NULL,
                        due_date DATETIME NOT NULL,
                        is_completed BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
                        ON UPDATE CURRENT_TIMESTAMP,
                        FOREIGN KEY (status_id) REFERENCES statuses(id),
                        FOREIGN KEY (priority_level_id) REFERENCES 
                        priority_levels(id)
                    )
                """)

                # Insert default statuses from Status class
                cursor.execute("SELECT COUNT(*) as count FROM statuses")
                result = cursor.fetchone()
                if result['count'] == 0:
                    status_values = [(code,) for code in self.status_manager.stored_statuses.keys()]
                    cursor.executemany(
                        "INSERT INTO statuses (status_code) VALUES (%s)",
                        status_values
                    )

                # Insert default priority levels from PriorityLevel class
                cursor.execute("SELECT COUNT(*) as count FROM priority_levels")
                result = cursor.fetchone()
                if result['count'] == 0:
                    priority_values = [(code,) for code in self.priority_manager.stored_priority_levels.keys()]
                    cursor.executemany(
                        "INSERT INTO priority_levels (priority_level_code) VALUES (%s)",
                        priority_values
                    )

                self.connection.commit()

        except pymysql.Error as e:
            print(f"Error creating tables: {e}")

    def close(self):
        """Explicitly close the database connection"""
        try:
            if self.connection:
                self.connection.close()
                self.connection = None
        except pymysql.Error:
            pass  # Ignore errors during closing

    def __del__(self):
        """Ensure connection is closed when object is destroyed"""
        self.close() 