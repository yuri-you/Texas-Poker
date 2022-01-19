from host_start import *
import time
def main():
    '''initial network'''
    users_list=dict()
    signal=True
    mainthread=MainThread(users_list)
    mainthread.daemon=True
    mainthread.start()
    while True:
    # while signal:
        x=input()
        if x=="1":
            signal=False
        print(users_list)
        # time.sleep(20)



if __name__=="__main__":
    main()