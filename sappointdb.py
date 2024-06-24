import mysql.connector
from datetime import datetime

# Function to calculate sap_point (hypothetical algorithm)
def calculate_sap_point(year, event, student_class):
    sap_point = year * 10 + len(event) + (int(student_class.split('-')[0]) // 10)
    return sap_point

# Function to connect to MySQL
def connect_to_mysql():
    conn = mysql.connector.connect(
        host='localhost',
        database='project',
        user='root',
        password='Vishnu@1804'
    )
    return conn

# Function to insert student data
def insert_student_data(conn):
    cursor = conn.cursor()

    # Get input for student details
    rollno = input("Enter student roll number: ")
    
    # Check if student with the same roll number already exists
    query_existing = "SELECT COUNT(*) FROM students WHERE student_rollno = %s"
    cursor.execute(query_existing, (rollno,))
    result = cursor.fetchone()

    if result[0] > 0:
        print(f"Student with roll number {rollno} already exists. Skipping insertion.")
        return

    name = input("Enter student name: ")
    year = int(input("Enter year of study: "))
    email = input("Enter student email: ")
    event = input("Enter event participated: ")
    student_class = input("Enter student class (e.g., 1-AIML-B): ")

    # Calculate sap_point
    sap_point = calculate_sap_point(year, event, student_class)

    # Prepare SQL query to insert data into students table
    insert_query = """
    INSERT INTO students (student_rollno, student_name, year, email, enrollment_date, event, class, sap_point)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    # Data to be inserted
    data = (rollno, name, year, email, datetime.now().date(), event, student_class, sap_point)

    # Execute the insert query
    cursor.execute(insert_query, data)

    # Commit changes to database
    conn.commit()

    print('Data inserted successfully')
    print(f'SAP Point calculated: {sap_point}')

    cursor.close()

# Function to display SAP points for a particular student
def display_sap_points(conn):
    cursor = conn.cursor()

    rollno = input("Enter student roll number to display SAP points: ")

    # Query to retrieve SAP points for a specific student
    query = "SELECT sap_point FROM students WHERE student_rollno = %s"
    cursor.execute(query, (rollno,))
    result = cursor.fetchone()

    if result:
        print(f'SAP Points for student with roll number {rollno}: {result[0]}')
    else:
        print(f'No student found with roll number {rollno}')

    cursor.close()

# Main function to handle user choices
def main():
    conn = connect_to_mysql()

    while True:
        print("\n1. Add items\n2. Display SAP points for a particular student\n3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            insert_student_data(conn)
        elif choice == '2':
            display_sap_points(conn)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please enter a valid option.")

    conn.close()
    print('MySQL connection closed')

if __name__ == "__main__":
    main()