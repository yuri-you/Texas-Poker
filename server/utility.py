PORT=11001
def write(socket,string):
    strings=string
    strings+='.'
    print("write:"+strings)
    socket.send(bytes(strings,'utf-8'))