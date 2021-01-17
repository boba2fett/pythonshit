#!/usr/bin/env python3
import time
import datetime
import sys, os

def mainloop():
    lastData=None
    while True:
        try:
            currtime=time.time()
            distance=300 - currtime % 300
            alligned_time=currtime+distance
            time.sleep(distance) # wait to the next 5 min
            timestamp=datetime.datetime.fromtimestamp(int(alligned_time)) # everyone gets same 5min alligned time

            data = DcApi.getData()
            Send.sendOnlineMessages(data,lastData)
            try:
                DbApi.dbCollect(data,timestamp)
            except Exception as e:
                Send.sendError(Exception(f"DataCollection unsuccesful, because of {str(e)}"))
            try:
                DbApi.dbSend(data)
            except Exception as e:
                Send.sendError(Exception(f"LogServer was not reached: {str(e)}"))
        except Exception as e:
            Send.sendError(f"Fail in Mainloop pending 290s: {e}")
            time.sleep(290)
        finally:
            try:
                lastData=data
            except Exception as e:
                lastData=None

def main():

    print(f"starting dcnotify in {CONFIG['env']}")
    Send.sendError(DbApi.test())
    mainloop()

if __name__ == '__main__':
    if len(sys.argv)>1 and sys.argv[1]=="dev":
        os.environ['tg-env'] = "dev"
    
    from config import CONFIG
    from dcapi import DcApi
    from dbapi import DbApi
    from send import Send
    import handler
    main()
