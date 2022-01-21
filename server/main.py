from host_start import *
from game import *
import time
def main():
    users_list=dict()
    Threads=[]
    '''initial network'''
    # signal=[False]
    mainthread=MainThread(users_list,Threads)
    mainthread.daemon=True
    mainthread.start()
    Threads.append(mainthread)
    #before begin
    Players=dict()
    Audience=dict()
    while True:
        all_finish=True
        for thread in Threads:
            if thread.is_alive():
                all_finish=False
                break
        if all_finish:
            judge=0
            for user in users_list:
                if users_list[user]["Ready"]:
                    judge+=1
                    Players[user]=users_list[user]
                else:
                    Audience[user]=users_list[user]
            print("Player:%d, Audience:%d"%(len(Players),len(Audience)))
            break
    # print(t.is_alive())
    # print(mainThread[0].is_alive())
    information=dict()
    information["起始金额"]=2000
    information["起始底注"]=10
    count=0
    print(1)
    for user in Players:
            Players[user]["information"]=dict()
            Players[user]["information"]["money"]=information["起始金额"]
            Players[user]["information"]["Start"]=False
            Players[user]["information"]["id"]=count
            new_thread=PlayerThread(user,Players,information)
            Players[user]["Thread"]=new_thread
            new_thread.daemon=True
            count+=1

            # users_list[user]["information"]["action"]=False
            # users_list[user]["information"]["action content"]=str()
    for user in Audience:
            new_thread=AudienceThread(user,Audience,information)
            Audience[user]["Thread"]=new_thread
            new_thread.daemon=True
    print(len(Players))
    for user in Players:
        print("Start:"+user)
        Players[user]["Thread"].start()
    while True:
        is_start=True
        while is_start:
            is_start=False
            for player in Players:
                if not Players[player]["information"]["Start"]:
                    is_start=True
                    break
        iterations=0
        for player in Players:
            Players[player]["information"]["position"]=(Players[player]["information"]["id"]+iterations)%len(Players)
            for key in Players:
                while not Players[player]["information"]["Write"]:
                    a=1
                Players[player]["TcpSocket"].send(bytes('Initial State,%s,%d,%d'%(key,Players[key]["information"]["id"],(Players[key]["information"]["id"]+iterations)%len(Players)),'utf-8'))
                Players[player]["information"]["Write"]=False
            while not Players[player]["information"]["Write"]:
                a=1
            # print("Finish")
            Players[player]["TcpSocket"].send(bytes("Initial State Finish",'utf-8'))
            Players[player]["information"]["Write"]=False
        a=input()


if __name__=="__main__":
    main()