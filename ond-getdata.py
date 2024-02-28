from zk import ZK, const
import json
import time

with open("users.json") as f:
    u = json.load(f)
    f.close()
attendance_log = []
conn = None
# create ZK instance
ips = [f"172.24.10.10{i}" for i in range(1,5)]

for ip in ips:
    zk = ZK(ip, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
    try:
        # connect to device
        conn = zk.connect()
        # disable device, this method ensures no activity on the device while the process is run
        conn.disable_device()
        
        # another commands will be here!
        # Example: Get All Users
        '''users = conn.get_users()
        for user in users:
            print(user)
            u[user.user_id] = user.name
            privilege = 'User'
            if user.privilege == const.USER_ADMIN:
                privilege = 'Admin'
            print ('+ UID #{}'.format(user.uid))
            print ('  Name       : {}'.format(user.name))
            print ('  Privilege  : {}'.format(privilege))
            print ('  Password   : {}'.format(user.password))
            print ('  Group ID   : {}'.format(user.group_id))
            print ('  User  ID   : {}'.format(user.user_id))
            
        
        with open("users.json", "w") as f:
            json.dump(u, f)
            f.close()
        '''
        # Test Voice: Say Thank
        #conn.test_voice()
        # re-enable device after all commands already executed
        '''
        print(conn.get_firmware_version())
        print(conn.get_serialnumber())
        print(conn.get_platform())
        print(conn.get_device_name())
        print(conn.get_face_version())
        print(conn.get_fp_version())
        print(conn.get_extend_fmt())
        print(conn.get_user_extend_fmt())
        print(conn.get_face_fun_on())
        print(conn.get_compat_old_firmware())
        print(conn.get_network_params())
        print(conn.get_mac())
        print(conn.get_pin_width())
        '''
        attendances = conn.get_attendance()

        print(f"attendance {ip}: ")
        for attendance in attendances:
            try:
                attendance_log.append((attendance,ip))
                #print(f"UID:{attendance.user_id}  name:{u[attendance.user_id]}    time:{attendance.timestamp}   status:{attendance.status}   punch:{attendance.punch}   device:{ip}")
            except:
                #print(f"UID:{attendance.user_id}  name:{attendance.user_id}    time:{attendance.timestamp}   status:{attendance.status}   punch:{attendance.punch}   device:{ip}")
                pass
        print()
        conn.enable_device()

    except Exception as e:
        print ("Process terminate : {}".format(e))
    finally:
        if conn:
            conn.disconnect()
attendance_log.sort(key=lambda x: x[0].timestamp)
for attendance, ip in attendance_log:
    try:
        #attendance_log.append(attendance)
        print(f"UID:{attendance.user_id}  name:{u[attendance.user_id]}    time:{attendance.timestamp}   status:{attendance.status}   punch:{attendance.punch}   device:{ip}")
    except:
        print(f"UID:{attendance.user_id}  name:{attendance.user_id}    time:{attendance.timestamp}   status:{attendance.status}   punch:{attendance.punch}   device:{ip}")
             
