import mysql.connector
import threading
from datetime import datetime
from zk import ZK

HOST = "localhost"
USER = ""
PASSWORD = ""
DB = "att_records"

def make_connection(host_name = HOST, user_name = USER, user_password = PASSWORD, db_name = DB):
  '''connecting to the database in server'''
  
  connection = None
  try:
    connection = mysql.connector.connect(
        host=host_name,
        user=user_name,
        passwd=user_password,
        database=db_name
    )
    print("Connection to MySQL DB ",db_name," successful")
    
  except mysql.connector.Error as e:
    print(f"The error '{e}' occurred")
  return connection

def run_query(connection, query):
  '''Running a query'''

  cursor = connection.cursor()
  try:
      cursor.execute(query)
      print(query,"run successfully")
  except mysql.connector.Error as e:
      print(f"The error '{e}' occurred")

def add_data(connection, att):
    add_data_query=f"INSERT INTO att_logs VALUES ('{att.user_id}','{att.timestamp.strftime('%Y-%m-%d %H:%M:%S')}')"
    run_query(connection,add_data_query)
    

dev_conn = None
ips = [f"172.24.10.10{i}" for i in range(1,5)]


def capture(ip):
    '''Adding LIVE capture to the database'''
  
    zk = ZK(ip, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
    sql_conn = make_connection()


    try:
        dev_conn = zk.connect()
        print(f"Starting live capture {ip}")

        for attendance in dev_conn.live_capture():
            print(f"{ip}:  {attendance}")
            if attendance is None:
                pass
            else:
                add_data(sql_conn, attendance)
                sql_conn.commit()

    except Exception as e:
        print (f"Error: {e}")
    finally:
        if dev_conn:
            dev_conn.disconnect()

for ip in ips:
    threading.Thread(target=capture, args=(ip,)).start()
