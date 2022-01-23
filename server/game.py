from threading import Thread
from socket import *
import time
BUFSIZ=1024
class PlayerThread(Thread):
    def __init__(self,name,users_list:list,information:dict):
        super(PlayerThread, self).__init__()
        self.users_list=users_list
        self.name=name
        self.tcpCliSock=users_list[name]["TcpSocket"]
        self.Addr=users_list[name]["Addr"]
        self.tcpCliSock.send(bytes('Change Money,%d'%self.users_list[self.name]["information"]["money"],'utf-8'))
        self.users_list[self.name]["information"]["Start"]=True
    def run(self):
        # self.tcpCliSock.send(bytes('Game Start,Player','utf-8'))
        while True:
            receive=self.tcpCliSock.recv(BUFSIZ)
            receive=receive.decode('utf-8')
            print("receive from "+receive+" ip=%s,port=%d"%(self.Addr[0],self.Addr[1]))
            if not receive:
                #断线了
                break
            # if receive=="Accepted":
            #     self.users_list[self.name]["information"]["Write"]=True
            if receive=="Receive Game Start":
                pass
            datas=receive.split(",")
            if datas[0]=="Change Money":
                for player in self.users_list:
                    if player==datas[1]:
                        self.users_list[player]["TcpSocket"].send(bytes('Change Money,%s'%datas[2],'utf-8'))
            if datas[0]=="Information":
                print(receive)
                for player in self.users_list:
                    if player==datas[1]:
                        self.users_list[player]["TcpSocket"].send(bytes("Information,%s"%datas[2],'utf-8'))
                    
class AudienceThread(Thread):
    def __init__(self,name,users_list:list,information:dict):
        super(AudienceThread, self).__init__()
        self.name=name
        self.tcpCliSock=users_list[name]["TcpSocket"]
    def run(self):

        self.tcpCliSock.send(bytes('Game Start,Audience','utf-8'))
        while True:
            pass