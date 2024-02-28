from zk import ZK
import json
import threading

with open("users.json") as f:
    u = json.load(f)
    f.close()

conn = None
ips = [f"172.24.10.10{i}" for i in range(1, 5)]


def capture(ip):
    zk = ZK(ip, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)

    try:

        conn = zk.connect()
        print(f"Starting live capture {ip}")
        for attendance in conn.live_capture():
            print(f"{ip}:  {attendance}")
            if attendance is None:
                pass
            else:
                try:
                    print(
                        f"UID:{attendance.user_id}  name:{u[attendance.user_id]}    time:{attendance.timestamp}   status:{attendance.status}   punch:{attendance.punch}   device:{ip}"
                    )
                except:
                    print(
                        f"UID:{attendance.user_id}  name:{attendance.user_id}    time:{attendance.timestamp}   status:{attendance.status}   punch:{attendance.punch}   device:{ip}\n"
                    )

    except Exception as e:
        print(f"Process terminate : {e}")
    finally:
        if conn:
            conn.disconnect()


for ip in ips:
    threading.Thread(target=capture, args=(ip,)).start()
