#!/usr/bin/env python3
import sys
import os
from config import CONFIG
import telegram
import datetime
from dbapi import DbApi

class Send():
    def sendError(error):
        msg=f'{datetime.datetime.now()}\n{error}'
        try:
            bot = telegram.Bot(token=CONFIG["bot_token"])
            bot.sendMessage(chat_id=CONFIG["chat_id"], text=msg)
            print(f"Send {msg}")
        except Exception as ex:
            print(f'{datetime.datetime.now()} Could not send [{error}], because of {ex}')

    def sendOnlineMessages(data,lastData):
        offline=list()
        names = DbApi.subscribedUsers()
        names = [x[0] for x in names]
        for name in names:
            if name not in [x['username'] for x in data] and lastData is not None and name in [x['username'] for x in lastData]:
                Send.sendOnlineMsg(name,"offline")
                offline+=name
        on=[x for x in data if x['username'] in names and x['username'] not in offline]
        for member in on:
            try:
                oldMember = DbApi.lastState(member["username"])
                if lastData is None or member["username"] not in [x['username'] for x in lastData] or oldMember["status"] != member["status"]:
                    Send.sendOnlineMsg(member["username"], member["status"])
            except Exception as e:
                print(f'Online Message failed because of [{str(e)}]')
        if (lastData is None or not any([x["channel_id"] == None for x in lastData])) and any([x["channel_id"] != None for x in data]):
            Send.sendOnlineMsg(str(sum([x["channel_id"] == None for x in data])), "in channel")

    def sendOnlineMsg(name,status):
        bot = telegram.Bot(token=CONFIG["bot_token"])
        subscribers = DbApi.subscribers(name)
        msg = f'{name} now {status}'
        print(msg,subscribers)
        for chat_id in subscribers:
            try:
                bot.sendMessage(chat_id=chat_id, text=msg)
            except Exception as e:
                print(f'Online Message failed because of [{str(e)}]')
