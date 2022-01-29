from threading import Thread
from socket import *
from utility import *
import time
BUFSIZ=1024
IP='39.108.192.128'
MIN_SIZE=1
def test_ready(users_list):
    if len(users_list)<MIN_SIZE:return
    ready=True
    for user in users_list:
        if users_list[user]["Ready"]==2:
            host_name=user
        elif users_list[user]["Ready"]==0:
            ready=False
            break
    if ready:
        write(users_list[host_name]["TcpSocket"],'All Ready')
    else:
        write(users_list[host_name]["TcpSocket"],'Not All Ready')

class ClientThread(Thread):
    def __init__(self,tcpCliSock,Addr,users_list:list):
        super(ClientThread, self).__init__()
        print("Receive Connection from Player %d (ip=%s,port=%d)"%(len(users_list),Addr[0],Addr[1]))
        self.tcpCliSock=tcpCliSock
        self.Addr=Addr
        self.users_list=users_list
        write(self.tcpCliSock,"Connect Successfully")
        self.name=Addr[0]
    def run(self):
        while True:
            data_row=self.tcpCliSock.recv(BUFSIZ)
            data_row=data_row.decode('utf-8')
            # if data=="test":
            #     print(self.users_list)
            if not data_row:
                #the user exit
                print("connected terminate to ip=%s,port=%d"%(self.Addr[0],self.Addr[1]))
                if self.users_list[self.name]["Ready"]==2:#host 
                    del self.users_list[self.name]
                    for user in self.users_list:
                        self.users_list[user]["Ready"]=2
                        for other_user in self.users_list:
                            write(self.users_list[other_user]['TcpSocket'],"Change Host,"+user)
                        break
                else:
                    del self.users_list[self.name]
                for user in self.users_list:
                    write(self.users_list[user]["TcpSocket"],'User Leave,'+self.name)
                exit()
            print("from %s,%d get %s"%(self.Addr[0],self.Addr[1],data_row))
            data_row=data_row.split(".")
            for data in data_row:
                # respMsg="accepted:%s"%(data)
                datas=data.split(',')
                if datas[0]=="Ready":
                    self.users_list[self.name]["Ready"]=1
                    # allready=True
                    # for key in self.users_list:
                    #     if self.users_list[key]["Ready"]==0:
                    #         allready=False
                    #         break
                    for key in self.users_list:
                        if key!=self.name:
                            write(self.users_list[key]["TcpSocket"],'Ready,'+self.name)
                    test_ready(self.users_list)
                elif datas[0]=="Cancel Ready":
                    self.users_list[self.name]["Ready"]=False
                    # allready=True
                    # for key in self.users_list:
                    #     if self.users_list[key]["Ready"]==0:
                    #         allready=False
                    #         break
                    for key in self.users_list:
                        if key!=self.name:
                            write(self.users_list[key]["TcpSocket"],'Cancel Ready,'+self.name)
                    test_ready(self.users_list)


                elif datas[0]=="Change Name":
                    tmprecord=self.users_list[self.name]
                    del self.users_list[self.name]
                    self.users_list[datas[1]]=tmprecord
                    for user in self.users_list:
                        if user!=datas[1]:
                            write(self.users_list[user]["TcpSocket"],'Change Name,'+self.name+','+datas[1])
                    self.name=datas[1]
                elif datas[0]=="Begin Game":
                    tcp_reset = socket(AF_INET, SOCK_STREAM)
                    tcp_reset.connect(("", PORT))
                    tcp_reset.close()
                    print(self.users_list)
                    for user in self.users_list:
                        print("send begin ip%s"%self.users_list[user]["Addr"][0])
                        write(self.users_list[user]["TcpSocket"],"Begin Game")
                    break
                elif datas[0]=="Receive Game Start":
                    print("Receive Game Start in ip%s"%self.Addr[0])
                    exit()
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
            new_player_name=new_player_name[0:-1]
            if new_player_name in self.users_list:
                write(tcpCliSock,'Name Repeat')
                continue
            # while data in self.users_list:
            #     data+='1'
            if len(self.users_list)!=0:
                for user in self.users_list:
                    write(self.users_list[user]["TcpSocket"],'User Add,'+new_player_name)
                    write(tcpCliSock,"Initial Player,%s,%d"%(user,self.users_list[user]["Ready"]))
                write(tcpCliSock,"Initial Finish")
                # print("users_name:"+new_player_name)
                self.users_list[new_player_name]=dict()
                self.users_list[new_player_name]["Thread"]=t
                self.users_list[new_player_name]["TcpSocket"]=tcpCliSock
                self.users_list[new_player_name]["Addr"]=Addr
                self.users_list[new_player_name]["Ready"]=0
                t.name=new_player_name
                test_ready(self.users_list)
            else:
                print("Set host:"+new_player_name)
                write(tcpCliSock,"Initial Player Host")
                self.users_list[new_player_name]=dict()
                self.users_list[new_player_name]["Thread"]=t
                self.users_list[new_player_name]["TcpSocket"]=tcpCliSock
                self.users_list[new_player_name]["Addr"]=Addr
                self.users_list[new_player_name]["Ready"]=2
                t.name=new_player_name
                test_ready(self.users_list)
                # write(tcpCliSock,"All Ready")
            t.start()
