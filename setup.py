import mysql.connector

HOST = "localhost"
USER = "test"
PASSWORD = "test@mysql"


def create_connection(host_name=HOST, user_name=USER, user_password=PASSWORD):
    """connecting to the SQL server"""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
        )
        print("Connection to MySQL DB successful")
    except mysql.connector.Error as e:
        print(f"The error1 '{e}' occurred")
    return connection


def setup(connection):
    cursor = connection.cursor()
    query = [
        "CREATE DATABASE IF NOT EXISTS att_records",
        "USE att_records",
        "CREATE TABLE IF NOT EXISTS att_logs (UID VARCHAR(20), Name VARCHAR(100), Time TIMESTAMP(0), PRIMARY KEY(UID))",
        "CREATE TABLE IF NOT EXISTS users (UID VARCHAR(20), Name VARCHAR(100), Privilege VARCHAR(20), PRIMARY KEY(UID))",
        "COMMIT",
    ]
    try:
        for q in query:
            cursor.execute(q)
        print(query, "run successfully")
    except mysql.connector.Error as e:
        print(f"The error '{e}' occurred")


conn = create_connection()
setup(conn)
