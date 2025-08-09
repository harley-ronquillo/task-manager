from database import Database
import mysql.connector
from mysql.connector import Error

def test_database_connection():
    """Test database connection and table creation"""
    try:
        # Create database instance
        db = Database()
        
        # Create tables
        db.create_tables()
        
        # Verify tables were created and data was inserted
        verify_tables(db.connection)
        
    except Error as e:
        print(f"Error during testing: {e}")

def verify_tables(connection):
    """Verify that tables exist and contain the expected data"""
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Check statuses table
        print("\nChecking statuses table:")
        cursor.execute("SELECT * FROM statuses")
        statuses = cursor.fetchall()
        print(f"Found {len(statuses)} status records:")
        for status in statuses:
            print(f"ID: {status['id']}, Code: {status['status_code']}")
        
        # Check priority levels table
        print("\nChecking priority_levels table:")
        cursor.execute("SELECT * FROM priority_levels")
        priority_levels = cursor.fetchall()
        print(f"Found {len(priority_levels)} priority level records:")
        for priority in priority_levels:
            print(f"ID: {priority['id']}, Code: {priority['priority_level_code']}")
        
        # Check tasks table structure
        print("\nChecking tasks table structure:")
        cursor.execute("""
            SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_KEY, EXTRA 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'tasks'
        """)
        columns = cursor.fetchall()
        print("Tasks table columns:")
        for column in columns:
            print(f"Column: {column['COLUMN_NAME']}")
            print(f"  Type: {column['COLUMN_TYPE']}")
            print(f"  Nullable: {column['IS_NULLABLE']}")
            print(f"  Key: {column['COLUMN_KEY']}")
            print(f"  Extra: {column['EXTRA']}")
            print()
        
        # Check foreign keys
        print("\nChecking foreign key constraints:")
        cursor.execute("""
            SELECT 
                CONSTRAINT_NAME,
                COLUMN_NAME,
                REFERENCED_TABLE_NAME,
                REFERENCED_COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = 'tasks'
            AND REFERENCED_TABLE_NAME IS NOT NULL
        """)
        foreign_keys = cursor.fetchall()
        print("Foreign key relationships:")
        for fk in foreign_keys:
            print(f"Constraint: {fk['CONSTRAINT_NAME']}")
            print(f"  Column: {fk['COLUMN_NAME']}")
            print(f"  References: {fk['REFERENCED_TABLE_NAME']}({fk['REFERENCED_COLUMN_NAME']})")
            print()
        
    except Error as e:
        print(f"Error verifying tables: {e}")
    finally:
        cursor.close()

if __name__ == "__main__":
    test_database_connection() 