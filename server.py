import socket
import sys
from thread import *
import threading
host = "0.0.0.0"
port = int(sys.argv[1])

max_threads = 3

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
studentID = "11321436" 

s.bind((host, port))

s.listen(1)
print "listening"

semaphore = threading.BoundedSemaphore(value=max_threads)

def handler(conn):
    keepalive = True
    print "in thread"
    data = conn.recv(1024)
    tokens = data.split(" ")
    command = tokens[0]
    if command == "HELO":
        response = data + "IP:{}\nPort:{}\nStudentId:{}" \
            .format(host, port, studentID)
    elif command == "KILL_SERVICE":
        sys.exit(0)
    else:
        response = "No handler"
    conn.sendall(response)
    conn.close()
    semaphore.release()
    return

while(1):
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    semaphore.acquire()
    start_new_thread(handler, (conn,))

s.close()

