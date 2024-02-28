import mysql.connector
from zk import ZK, const

def make_connection(host_name, user_name, user_password, db_name):
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
	cursor = connection.cursor()
	try:
			cursor.execute(query)
			print(query,"run successfully")
	except mysql.connector.Error as e:
			print(f"The error '{e}' occurred")

def add_user(connection, user):
		add_data_query = f"INSERT INTO users VALUES ('{user.uid}','{user.name}','{user.privilege}')"
		run_query(connection,add_data_query)

ips = [f"172.24.10.10{i}" for i in range(1,5)]
sql_conn = make_connection("localhost", "test", "test@mysql", "att_records")

for ip in ips:
		zk = ZK(ip, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
		try:
				conn = zk.connect()
				conn.disable_device()
				
				users = conn.get_users()
				
				for user in users:
						if user.privilege == const.USER_ADMIN:
							user.privilege = "Admin"
						else:
							user.privilege = "User"

						add_user(sql_conn, user)
						
				conn.enable_device()

		except Exception as e:
				print ("Process terminate : {}".format(e))
		finally:
				if conn:
						conn.disconnect()
sql_conn.commit()