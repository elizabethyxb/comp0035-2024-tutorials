from pathlib import Path

import pandas as pd

import sqlite3

def df_to_sql(df, db_path):
    conn = sqlite3.connect(db_path)

    # Save the dataframe to the database, this will create a table called 'enrollments' and replace it if
    # it exists. The index column is not saved to the table.
    # If the file does not exist then it will be created.
    df.to_sql('enrollments', conn, if_exists='replace', index=False)

    # Close the connection.
    conn.close()

def create_tables(df, db_path):
    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    student_sql = '''CREATE TABLE IF NOT EXISTS student (
                                student_id INTEGER PRIMARY KEY,
                                student_name STRING NOT NULL,
                                student_email STRING NOT NULL);
                                '''
    teacher_sql = '''CREATE TABLE IF NOT EXISTS teacher (
                                teacher_id INTEGER PRIMARY KEY,
                                teacher_name STRING NOT NULL,
                                teacher_email STRING NOT NULL UNIQUE);
                                '''
    course_sql = '''CREATE TABLE IF NOT EXISTS course (
                                course_id INTEGER PRIMARY KEY,
                                course_name STRING NOT NULL,
                                course_code INTEGER NOT NULL,
                                course_schedule STRING,
                                course_location STRING);
                                '''
    enrollment_sql = '''CREATE TABLE IF NOT EXISTS enrollment (
                                student_id INTEGER NOT NULL, 
                                course_id INTEGER NOT NULL,
                                teacher_id INTEGER,
                                PRIMARY KEY (student_id, course_id, teacher_id),
                                FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE ON UPDATE CASCADE,
                                FOREIGN KEY (course_id) REFERENCES course(course_id) ON DELETE CASCADE ON UPDATE CASCADE,
                                FOREIGN KEY (teacher_id) REFERENCES teacher(teacher_id) ON UPDATE CASCADE ON DELETE SET NULL);
                                '''
    
    # By default, foreign key constraints are disabled in SQLite, enable them explicitly for each database connection.
    cursor.execute('PRAGMA foreign_keys = ON;')
    cursor.execute(enrollment_sql)
    cursor.execute(student_sql)
    cursor.execute(teacher_sql)
    cursor.execute(course_sql)
    # Commit the changes
    conn.commit()

    # Close the connection.
    conn.close()

def insert_data(df, db_path):
    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    # Enable foreign key constraints for sqlite
    # By default, foreign key constraints are disabled in SQLite, enable them explicitly for each database connection.
    cursor.execute('PRAGMA foreign_keys = ON;')
    conn.commit()

    student_sql = 'INSERT INTO student (student_name, student_email) VALUES (?, ?)'

    # Create a dataframe with the unique values for the columns needed for the student table (excluding the student_id PK)
    student_df = pd.DataFrame(df[['student_name', 'student_email']].drop_duplicates())

    # Get the values as a list rather than pandas Series. The parameterised query expects a list.
    student_data = student_df.values.tolist()

    # Use `executemany()` with a parameterised query to add the values to the table.
    cursor.executemany(student_sql, student_data)

if __name__ == '__main__':
    project_root = Path(__file__).parent.parent

    # Find the .csv file relative to the project root and join to that path the data folder and then the example.csv file
    data_path = project_root.joinpath('tutorialpkg', 'data_db_activity', 'student_data.csv')

    df = pd.read_csv(data_path)
    
    unnormalised_db_path = project_root.joinpath('tutorialpkg', 'data_db_activity', 'enrollments_unnormalised.db')
    df_to_sql(df, unnormalised_db_path)

    db_path = project_root.joinpath('tutorialpkg', 'data_db_activity', 'enrollments_normalised.db')
    create_tables(df, db_path)
    insert_data(df, db_path)


