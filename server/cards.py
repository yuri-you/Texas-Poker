from utility import *
import random
def establish_cards():
    cards=list()
    for number in range(1,14):
        for card_type in ["S","H","C","D"]:
            if number==1:card_number='A'
            elif number==10:card_number='T'
            elif number==11:card_number='J'
            elif number==12:card_number='Q'
            elif number==13:card_number='K'
            else:
                card_number="%d"%number
            card=card_number+card_type
            cards.append(card)
    # print(cards)
    random.shuffle(cards)
    return cards
def allocate_cards(cards,Players):
    for player in Players:
        write(Players[player]["TcpSocket"],"Receive card,0,"+cards[-1])
        cards.pop()
        write(Players[player]["TcpSocket"],"Receive card,1,"+cards[-1])
        cards.pop()
def allocate_cards_same(cards,Players,lists):
    ready_card=[]
    for i in range(len(lists)):
        ready_card.append(cards[-1])
        cards.pop()
    for player in Players:
        for j in range(len(lists)):
            write(Players[player]["TcpSocket"],"Receive card,%d,%s"%(lists[j],ready_card[j]))