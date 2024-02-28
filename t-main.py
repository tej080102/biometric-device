import mysql.connector
from mysql.connector import Error
import json
import threading
from numpy import insert
from zk import ZK
from matplotlib.pyplot import table

from mysql.connector import pooling


def create_connection(
    host_name,
    user_name,
    user_password,
):
    """connecting to the SQL server"""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


connection = create_connection(
    "localhost",
    "root",
    "Tejusp@08",
)


"""Creating a database"""


def run_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print(query, "run successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


create_database_query = "CREATE DATABASE IF NOT EXISTS trial1;"
run_query(connection, create_database_query)
"""connecting to the database in server"""


def make_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name, user=user_name, passwd=user_password, database=db_name
        )
        print("Connection to MySQL DB ", db_name, " successful")

    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


"""CREATE TABLE """
connection = make_connection("localhost", "root", "Tejusp@08", "trial1")
create_table_query = "CREATE TABLE IF NOT EXISTS USERS1 (UID VARCHAR(20), Name VARCHAR(100), Time TIMESTAMP(0), PRIMARY KEY(UID) )"
run_query(connection, create_table_query)


"""ADD VALUES TO TABLE FROM JSON FILE"""
with open("users.json") as f:
    u = json.load(f)
    f.close()

for val in u:
    print(val, u[val], "123123" "\n")
    add_values = f"INSERT INTO USERS1 VALUES ('{val}','{u[val]}','123123')"
    run_query(connection, add_values)


def add_data(Uid, Name, Time):
    add_data_query = f"INSERT INTO USERS1 VALUES ('{Uid}','{Name}','{Time}')"
    run_query(connection, add_data_query)


add_data("001212", "Tejus", "1221")


"""ADDING LIVE CAPTURE TO THE DATABASE"""

conn1 = None
ips = [f"172.24.10.10{i}" for i in range(1, 5)]


def capture(ip):
    zk = ZK(ip, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
    # db.add_connection()
    # db_conn = db.get_connection()
    try:

        conn1 = zk.fconnect()
        print(f"Starting live capture {ip}")
        for attendance in conn1.live_capture():
            print(f"{ip}:  {attendance}")
            # l.write(f"{ip}:  {attendance}\n")
            if attendance is None:
                pass
            else:
                try:
                    # attendance_log.append(attendance)
                    print(
                        f"UID:{attendance.user_id}  name:{u[attendance.user_id]}    time:{attendance.timestamp}   status:{attendance.status}   punch:{attendance.punch}   device:{ip}"
                    )
                    add_data(
                        attendance.user_id, u[attendance.user_id], attendance.timestamp
                    )
                except:
                    print(
                        f"UID:{attendance.user_id}  name:{attendance.user_id}    time:{attendance.timestamp}   status:{attendance.status}   punch:{attendance.punch}   device:{ip}\n"
                    )
                    add_data(
                        attendance.user_id, u[attendance.user_id], attendance.timestamp
                    )

    except Exception as e:
        print(f"Process terminate : {e}")
    finally:
        if conn1:
            conn1.disconnect()


# capture(ips[0])
for ip in ips:
    threading.Thread(target=capture, args=(ip,)).start()

connection.commit()
connection.close()