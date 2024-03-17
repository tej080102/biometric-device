# Biometric-Device
An automatic attendence recorder for the fingerprint biometric device eSSL x990. Stores the records in MySQL.

The code consists of:
setup.py : This python file is used to create the initial database if not already present , which stores all the attendence records. (Needs to be run while setting up on a new device/server.)

add_users.py : The script connects to a MySQL database and performs various operations, including inserting new users and updating existing users' privileges, using the `mysql.connector` library for database connections and the `zk` package for networking. It also disables and enables devices and commits changes to the database.
