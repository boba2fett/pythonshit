#!/usr/bin/env python3
import sys
import os
from config import CONFIG
import telegram
import datetime
from dbapi import DbApi

class Send():

    def __init__(self, bot_token, admin_chat_id, dbApi):
        self.bot = telegram.Bot(token=bot_token)
        self.dbApi = dbApi
        self.admin_chat = admin_chat_id

    def sendError(self, error):
        msg=f'dcNotify Error: <<{error}>>'
        try:
            self.bot.sendMessage(chat_id=self.admin_chat, text=msg)
            print(f"dcNotify Error:  <<{msg}>>")
        except Exception as ex:
            print(f'{datetime.datetime.now()} Could not send <<{error}>>, because of <<{ex}>>')
    
    def sendNormal(self, msg):
        msg=f'{msg}'
        try:
            self.bot.sendMessage(chat_id=self.admin_chat, text=msg)
            print(f"{msg}")
        except Exception as ex:
            print(f'{datetime.datetime.now()} Could not send <<{msg}>>, because of <<{ex}>>')

    def sendOnlineMessages(self, data,lastData):
        offline=list()
        names = self.dbApi.subscribedUsers()
        for name in names:
            if name not in [x['username'] for x in data] and lastData is not None and name in [x['username'] for x in lastData]:
                self.sendOnlineMsg(name,"offline")
                offline+=name
        on=[x for x in data if x['username'] in names and x['username'] not in offline]
        for member in on:
            try:
                oldMember = self.dbApi.lastState(member["username"])
                if lastData is None or member["username"] not in [x['username'] for x in lastData] or oldMember["status"] != member["status"]:
                    self.sendOnlineMsg(member["username"], member["status"])
            except Exception as e:
                self.sendError(f'Online Message failed because of <<{str(e)}>>')
        #if (lastData is None or not any([x["channel_id"] == None for x in lastData])) and any([x["channel_id"] != None for x in data]):
        #    self.sendOnlineMsg(str(sum([x["channel_id"] == None for x in data])), "in channel")

    def sendOnlineMsg(self, name,status):
        subscribers = self.dbApi.subscribers(name)
        msg = f'{name} now {status}'
        print(msg,subscribers)
        for chat_id in subscribers:
            try:
                self.bot.sendMessage(chat_id=chat_id, text=msg)
            except Exception as e:
                self.sendError(f'Online Message failed because of <<{str(e)}>>')
