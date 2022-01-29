from threading import Thread
from socket import *
from utility import *
from cards import *
import time
BUFSIZ=1024
Max_Money=2000

'''
Players[player]["information"]

"alive" 是否还在游戏中
"fold"  是否盖牌
"position"  下注位置
"add_money"  加注金额
"Ready" 是否准备好了（收到信息）  由于线程同步性问题，
'''


class PlayerThread(Thread):
    def __init__(self,name,users_list:list,Information:dict):
        super(PlayerThread, self).__init__()
        self.users_list=users_list
        self.name=name
        self.tcpCliSock=users_list[name]["TcpSocket"]
        self.Addr=users_list[name]["Addr"]
        self.users_list[self.name]["information"]["Start"]=True
        self.Information=Information
        self.users_list[self.name]["information"]["Ready"]=True
    def run(self):
        while True:
            receive=self.tcpCliSock.recv(BUFSIZ)
            receive=receive.decode('utf-8')
            print("receive "+receive+" from  ip=%s,port=%d"%(self.Addr[0],self.Addr[1]))
            if not receive:
                #断线了
                break
            # if receive=="Accepted":
            #     self.users_list[self.name]["information"]["Write"]=True
            if receive=="Receive Game Start":
                pass
            receives=receive.split(".")
            for receive in receives:
                datas=receive.split(",")
                if datas[0]=="Change Money":
                    for player in self.users_list:
                        write(self.users_list[player]["TcpSocket"],'Change Money,%s,%s'%(datas[1],datas[2]))
                elif datas[0]=="Information":
                    print(receive)
                    for player in self.users_list:
                        if player==datas[1]:
                            write(self.users_list[player]["TcpSocket"],"Information,%s"%datas[2])
                elif datas[0]=="Accepted":
                    self.users_list[self.name]["information"]["Ready"]=True
                    # print("Name="+self.name)
                elif datas[0]=="Bet":
                    self.users_list[self.name]["information"]["add_money"]
                    for key in self.users_list:
                        write(self.users_list[key]["TcpSocket"],"Someone Bet,%s,%s"%((self.name),datas[1]))
                        self.users_list[key]["information"]["Ready"]=False
                    
class AudienceThread(Thread):
    def __init__(self,name,users_list:list,information:dict):
        super(AudienceThread, self).__init__()
        self.name=name
        self.tcpCliSock=users_list[name]["TcpSocket"]
    def run(self):
        write(self.tcpCliSock,'Game Start,Audience')
        while True:
            pass
def start_game(Players):
    for player in Players:
        Players[player]["information"]["alive"]=True#没有出局
        for key in Players:
            write(Players[player]["TcpSocket"],'Initial State,%s,%d'%(key,Players[key]["information"]["id"]))
            write(Players[player]["TcpSocket"],"Change Money,%s,%d"%(key,Max_Money))
        write(Players[player]["TcpSocket"],"Initial State Finish")
def begin_iteration(Players,Information):
    count=0
    for player in Players:
        if Players[player]["information"]["alive"]:
            Players[player]["information"]["position"]=(count+Information["iteration"])%len(Players)#下注位置
            Players[player]["information"]["fold"]=False#没有fold
            Players[player]["information"]["add_money"]=0#起始下注为0
            count+=1
    for player in Players:
        for key in Players:
            write(Players[player]["TcpSocket"],'Initial Position,%s,%d'%(key,Players[key]["information"]["position"]))
        write(Players[player]["TcpSocket"],"Initial Position Finish")
def activate(Players,Information):
    # 找目前玩家的name
    for player in Players:
        if Players[player]["information"]["id"]==(Information["now_player"]+Information["iteration"])%len(Players):
            break
    #该玩家已经弃牌或者出局
    if (not Players[player]["information"]["alive"]) or Players[player]["information"]["fold"]:
        return False
    #正常下注
    else:
        for key in Players:
            write(Players[player]["TcpSocket"],"Activate,"+player)
        # Information["Ready"]=False
        Players[player]["information"]["Ready"]=False
        return True
def enter_next_iteration(Players,Information,cards):
    Information["begin_bet"]=False
    Information["game_time"]+=1
    if Information["game_time"]==1:
        l=[2,3,4]
    elif Information["game_time"]==2:
        l=[5]
    elif Information["game_time"]==3:
        l=[6]
    else:
        return
    allocate_cards_same(cards,Players,l)


