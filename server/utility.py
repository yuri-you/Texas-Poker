import time
PORT=11000
def write(socket,string):
    strings=string
    strings+='.'
    print("write:"+strings)
    socket.send(bytes(strings,'utf-8'))
def check_ready(Players,Information):
    time.sleep(1)
    for player in Players:
        if Players[player]["information"]["Ready"]==False:
            # print(player+"ip=%s,port=%d"%(Players[player]["Addr"]))
            return False
    if Information["Ready"]==False:
        return False
    return True