from threading import Thread
from socket import *
import time
BUFSIZ=1024
IP='39.108.192.128'
PORT=12005

class ClientThread(Thread):
    def __init__(self,tcpCliSock,Addr,users_list:list):
        super(ClientThread, self).__init__()
        print("Receive Connection from Player %d (ip=%s,port=%d)"%(len(users_list),Addr[0],Addr[1]))
        self.tcpCliSock=tcpCliSock
        self.Addr=Addr
        self.users_list=users_list
        respMsg="Connect Successfully"
        self.tcpCliSock.send(bytes(respMsg,'utf-8'))
        self.name=Addr[0]
    def run(self):
        while True:
            data=self.tcpCliSock.recv(BUFSIZ)
            data=data.decode('utf-8')
            if data=="test":
                print(self.users_list)
            print("from %s,%d get %s"%(self.Addr[0],self.Addr[1],data))
            if not data:
                #the user exit
                print("connected terminate to ip=%s,port=%d"%(self.Addr[0],self.Addr[1]))
                if self.users_list[self.name]["Ready"]==2: 
                    del self.users_list[self.name]
                    for user in self.users_list:
                        self.users_list[user]["Ready"]=2
                        for other_user in self.users_list:
                            self.users_list[other_user]['TcpSocket'].send(bytes("Change Host,"+user,'utf-8'))
                else:
                    del self.users_list[self.name]
                for user in self.users_list:
                    self.users_list[user]["TcpSocket"].send(bytes('User Leave,'+self.name,'utf-8'))
                break
            # respMsg="accepted:%s"%(data)
            datas=data.split(',')
            if datas[0]=="Ready":
                self.users_list[self.name]["Ready"]=1
                allready=True
                for key in self.users_list:
                    if self.users_list[key]["Ready"]==0:
                        allready=False
                        break
                for key in self.users_list:
                    if key!=self.name:
                        self.users_list[key]["TcpSocket"].send(bytes('Ready,'+self.name,'utf-8'))
                        if self.users_list[key]["Ready"]==2 and allready:
                                self.users_list[key]["TcpSocket"].send(bytes('All Ready','utf-8'))
            elif datas[0]=="Cancel Ready":
                self.users_list[self.name]["Ready"]=False
                
                allready=True
                for key in self.users_list:
                    if self.users_list[key]["Ready"]==0:
                        allready=False
                        break
                for key in self.users_list:
                    if key!=self.name:
                        self.users_list[key]["TcpSocket"].send(bytes('Cancel Ready,'+self.name,'utf-8'))
                        if self.users_list[key]["Ready"]==2 and not allready:
                                self.users_list[key]["TcpSocket"].send(bytes('Not All Ready','utf-8'))
            elif datas[0]=="Change Name":
                tmprecord=self.users_list[self.name]
                del self.users_list[self.name]
                self.users_list[datas[1]]=tmprecord
                for user in self.users_list:
                    if user!=datas[1]:
                        self.users_list[user]["TcpSocket"].send(bytes('Change Name,'+self.name+','+datas[1],'utf-8'))
                self.name=datas[1]
            elif datas[0]=="Begin Game":
                tcp_reset = socket(AF_INET, SOCK_STREAM)
                tcp_reset.connect(("", PORT))
                tcp_reset.close()
                print(self.users_list)
                for user in self.users_list:
                    print("send begin ip%s"%self.users_list[user]["Addr"][0])
                    self.users_list[user]["TcpSocket"].send(bytes("Begin Game",'utf-8'))
                break
            elif datas[0]=="Receive Game Start":
                print("Receive Game Start in ip%s"%self.Addr[0])
                break
            # elif datas[0]=='Begin Game':
            #     break
            # self.tcpCliSock.send(bytes(respMsg,'utf-8'))
class MainThread(Thread):
    def __init__(self,users_list:dict,mainthread):
        super(MainThread, self).__init__()
        self.users_list=users_list
        self.mainthread=mainthread
    def run(self):
        HOST=""
        BUFSIZ=1024
        Addr=(HOST,PORT)
        tcpSvrSock=socket(AF_INET,SOCK_STREAM)
        tcpSvrSock.bind(Addr)
        tcpSvrSock.listen(20)
        while True:
            tcpCliSock,Addr=tcpSvrSock.accept()
            if Addr[0]=="127.0.0.1":#self
                print("End")
                break
            t=ClientThread(tcpCliSock,Addr,self.users_list)
            # t.daemon=True
            self.mainthread.append(t)
            new_player_name=tcpCliSock.recv(BUFSIZ).decode('utf-8')
            if new_player_name in self.users_list:
                tcpCliSock.send(bytes('Name Repeat','utf-8'))
                continue
            # while data in self.users_list:
            #     data+='1'
            if len(self.users_list)!=0:
                for user in self.users_list:
                    self.users_list[user]["TcpSocket"].send(bytes('User Add,'+new_player_name,'utf-8'))
                    tcpCliSock.send(bytes("Initial Player,%s,%d"%(user,self.users_list[user]["Ready"]),'utf-8'))
                    time.sleep(1)
                tcpCliSock.send(bytes("Initial Finish",'utf-8'))
                # print("users_name:"+new_player_name)
                self.users_list[new_player_name]=dict()
                self.users_list[new_player_name]["Thread"]=t
                self.users_list[new_player_name]["TcpSocket"]=tcpCliSock
                self.users_list[new_player_name]["Addr"]=Addr
                self.users_list[new_player_name]["Ready"]=0
                t.name=new_player_name
            else:
                print("host")
                tcpCliSock.send(bytes("Initial Player Host",'utf-8'))
                self.users_list[new_player_name]=dict()
                self.users_list[new_player_name]["Thread"]=t
                self.users_list[new_player_name]["TcpSocket"]=tcpCliSock
                self.users_list[new_player_name]["Addr"]=Addr
                self.users_list[new_player_name]["Ready"]=2
                t.name=new_player_name
                tcpCliSock.send(bytes('All Ready','utf-8'))
            t.start()
