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
            Players[user]["information"]=dict()
            Players[user]["information"]["money"]=Information["起始金额"]
            Players[user]["information"]["Start"]=False
            Players[user]["information"]["id"]=count
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
                if not Players[player]["information"]["Start"]:
                    is_start=True
                    break
        start_game(Players)
        # iterations=0
        #each game
        Information["iteration"]=0
        Information["alive_player"]=len(Players)
        while True:
            begin_iteration(Players,Information)
            cards=establish_cards()
            allocate_cards(cards,Players)
            Information["Ready"]=True
            Information["game_time"]=0 #现在进行到了第几轮，比如0是翻前。1是flop,2是
            Information["now_player"]=2
            Information["begin_bet"]=False
            # Information["max_bet"]=0
            Information["not_fold"]=Information["alive_player"]
            while True:
                if Information["not_fold"]==1 or Information["game_time"]==4:
                    break   #全部弃牌或者开牌
                if Information["game_time"]==0:#翻前
                    if Information["now_player"]==2:#轮到枪口位
                        if Information["begin_bet"]:#都加过注
                            continue_allocate=True
                            Bet_Money=[]
                            for player in Players:
                                if Players[player]["information"]["alive"] and not Players[player]["information"]["fold"]:
                                    Bet_Money.append(Players[player]["information"]["add_money"])
                            if len(set(Bet_Money))==1:#进到下一轮 
                                enter_next_iteration(Players,Information,cards)
                                #自动开牌bug
                                #盲注问题
                                #有人升注但自己不能再加
                                
                                continue
                        else:
                            Information["begin_bet"]=True
                elif Information["game_time"]>0:#翻牌后
                    if Information["now_player"]==0:#轮到小盲
                        if Information["begin_bet"]:#都加过注
                            continue_allocate=True
                            for player in Players:
                                if Players[player]["information"]["alive"] and not Players[player]["information"]["fold"]:
                                    if Players[player]["information"]["add_money"]!=Information["max_bet"]:
                                        continue_allocate=False
                                        break
                            if continue_allocate: 
                                enter_next_iteration(Players,Information,cards)
                                continue
                        else:
                            Information["begin_bet"]=True
                if activate(Players,Information):
                    while not check_ready(Players,Information):
                        pass
                Information["now_player"]=(Information["now_player"]+1)%len(Players)
                # while True:
                #     pass
            # activate(user)
            # now_player=
            # print(cards)


if __name__=="__main__":
    random.seed(int(time.time()))
    main()
 