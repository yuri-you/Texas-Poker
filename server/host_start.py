from threading import Thread
from socket import *
from time import ctime
BUFSIZ=1024
class ClientThread(Thread):
    def __init__(self,tcpCliSock,addr,users_list:list):
        super(ClientThread, self).__init__()
        print("Receive Connection from Player %d (ip=%s,port=%d)"%(len(users_list),addr[0],addr[1]))
        self.tcpCliSock=tcpCliSock
        self.addr=addr
        self.users_list=users_list
        respMsg="Connect Successfully"
        self.tcpCliSock.send(bytes(respMsg,'utf-8'))
        self.name=addr[0]
    def run(self):
        while True:
            data=self.tcpCliSock.recv(BUFSIZ)
            data=data.decode('utf-8')
            print("from %s,%d get %s"%(self.addr[0],self.addr[1],data))
            if not data:
                print("connected terminate to ip=%s,port=%d"%(self.addr[0],self.addr[1]))
                del self.users_list[self.name]
                break
            respMsg="accepted:%s"%(data)
            self.tcpCliSock.send(bytes(respMsg,'utf-8'))
class MainThread(Thread):
    def __init__(self,users_list:dict):
        super(MainThread, self).__init__()
        self.users_list=users_list
    def run(self):
        HOST=""
        PORT=11001
        BUFSIZ=1024
        ADDR=(HOST,PORT)
        tcpSvrSock=socket(AF_INET,SOCK_STREAM)
        tcpSvrSock.bind(ADDR)
        tcpSvrSock.listen(20)
        while True:
            tcpCliSock,addr=tcpSvrSock.accept()
            t=ClientThread(tcpCliSock,addr,self.users_list)
            t.daemon=True
            data=tcpCliSock.recv(BUFSIZ).decode('utf-8')
            if data in self.users_list:
                tcpCliSock.send(bytes('Name Repeat','utf-8'))
                continue
            # while data in self.users_list:
            #     data+='1'
            self.users_list[data]=dict()
            self.users_list[data]["thread"]=t
            self.users_list[data]["tcpSocket"]=tcpCliSock
            self.users_list[data]["addr"]=addr
            t.name=data
            t.start()
