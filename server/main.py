from host_start import *
from game import *
from cards import *
import time
import random

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
    Information=dict()
    Information["起始金额"]=2000
    Information["起始底注"]=10
    count=0
    for user in Players:
            Players[user]["Information"]=dict()
            Players[user]["Information"]["Money"]=Information["起始金额"]
            Players[user]["Information"]["Start"]=False
            Players[user]["Information"]["Id"]=count
            new_thread=PlayerThread(user,Players,Information)
            Players[user]["Thread"]=new_thread
            new_thread.daemon=True
            count+=1

            # users_list[user]["information"]["action"]=False
            # users_list[user]["information"]["action content"]=str()
    for user in Audience:
            new_thread=AudienceThread(user,Audience,Information)
            Audience[user]["Thread"]=new_thread
            new_thread.daemon=True
    for user in Players:
        print("Start:"+user)
        Players[user]["Thread"].start()
    #initialize game
    while True:
        is_start=True
        while is_start:
            is_start=False
            for player in Players:
                if not Players[player]["Information"]["Start"]:
                    is_start=True
                    break
        start_game(Players)
        # iterations=0
        #each game
        Information["Iteration"]=0
        Information["Alive player"]=len(Players)
        for player in Players:
            Players[player]["Information"]["Cards"]=list()
        while True:
            begin_iteration(Players,Information)
            cards=establish_cards()
            allocate_cards(cards,Players)
            Information["Ready"]=True
            Information["Game time"]=0 #现在进行到了第几轮，比如0是翻前。1是flop,2是
            Information["Now player"]=2
            Information["Begin bet"]=0#0进入这一轮之前 1第一轮下注  2都加过注
            Information["Max bet"]=0
            Information["Not fold"]=Information["Alive player"]
            Information["Dichi"]=0
            Players[player]["Information"]["Cards"].clear()
            while True:
                if Information["Not fold"]==1 or Information["Game time"]==4:
                    break   #全部弃牌或者开牌
                print(Information["Not fold"])
                if Information["Game time"]==0:#翻前
                    if Information["Now player"]==2:#轮到枪口位
                        if Information["Begin bet"]:#都加过注
                            continue_allocate=True
                            Bet_Money=[]
                            for player in Players:
                                if Players[player]["Information"]["Alive"] and not Players[player]["Information"]["Fold"]:
                                    Bet_Money.append(Players[player]["Information"]["Add money"])
                            # print(Bet_Money)
                            if len(set(Bet_Money))==1:#进到下一轮 
                                enter_next_iteration(Players,Information,cards)
                                Information["Now player"]=0
                                #盲注问题                                
                                continue
                        Information["Begin bet"]+=1
                elif Information["Game time"]>0:#翻牌后
                    if Information["Now player"]==0:#轮到小盲
                        if Information["Begin bet"]:#都加过注
                            continue_allocate=True
                            Bet_Money=[]
                            for player in Players:
                                if Players[player]["Information"]["Alive"] and not Players[player]["Information"]["Fold"]:
                                    Bet_Money.append(Players[player]["Information"]["Add money"])
                            # print(Bet_Money)
                            if len(set(Bet_Money))==1:#进到下一轮 
                                enter_next_iteration(Players,Information,cards)
                                #盲注问题                                
                                continue
                        Information["Begin bet"]+=1

                if activate(Players,Information):
                    # print("activate successfully")
                    while not check_ready(Players,Information):
                        pass
                # print(Information["now_player"])
                Information["Now player"]=(Information["Now player"]+1)%len(Players)
                time.sleep(0.1)
            if Information["Not fold"]==1:
                for player in Players:
                    if not Players[player]["Information"]["Fold"]:
                        break
                for key in Players:
                    write(Players[key]["TcpSocket"],"Add Money,%s,%d"%(player,Information["Dichi"]))
                
                # while True:
                #     pass
            # activate(user)
            # now_player=
            # print(cards)


if __name__=="__main__":
    random.seed(int(time.time()))
    main()
 