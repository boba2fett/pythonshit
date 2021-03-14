#!/usr/bin/env python3
import requests
import time
import sys
import datetime

#import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates

import recoonlib
states=recoonlib.states

dataset=recoonlib.dataset

users = sys.argv[1::]
print(users)

def per_day():
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    days=recoonlib.days()
    for user in users:
        datax=list()
        datay=list()
        for day in days:
            res = len(recoonlib.day_user(day, user))
            datax+=[day]
            datay+=[res]
        datax = dates.date2num(datax)
        ax1.plot(datax,datay,label=user,linewidth=1)

        for status in states:
            datax=list()
            datay=list()
            for day in days:
                res=len(recoonlib.day_user_status(day, user, status))
                datax+=[day]
                datay+=[res]
            datax = dates.date2num(datax)
            ax1.plot(datax,datay,label=f"{user}:{status}",linewidth=1)
    
    plt.xlabel("Day")
    plt.ylabel("Minutes online")
    myFmt = dates.DateFormatter('%Y-%m-%d')
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.legend(bbox_to_anchor=(1,1), loc="upper left")
    plt.title(label="Total per day per user")
    plt.show()

def per_weekday():
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    wdays=recoonlib.weekdays()
    datax=list()
    for user in users:
        datax=list()
        datay=list()
        for wday in wdays:
            res = len(recoonlib.weekday_user(wday, user))
            datax+=[wday]
            datay+=[res]
        ax1.plot(datax,datay,label=user,linewidth=1)

        for status in states:
            datax=list()
            datay=list()
            for wday in wdays:
                res=len(recoonlib.weekday_user_status(wday, user, status))
                datax+=[wday]
                datay+=[res]
            ax1.plot(datax,datay,label=f"{user}:{status}",linewidth=1)
    
    xticks=["Mo","Di","Mi","Do","Fr","Sa","So"]
    plt.xticks([x for x in range(0,7)], [xticks[x] for x in range(0,7)])
    plt.xlabel("Weekday")
    plt.ylabel("Minutes online")
    plt.legend(bbox_to_anchor=(1,1), loc="upper left")
    plt.title("Total per weekday per user")
    plt.show()

def per_time():
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    times=recoonlib.times()
    for user in users:
        datax=list()
        datay=list()
        for time in times:
            res = len([e for e in dataset if e["timestamp"].time() == time and e["username"]==user])
            t=recoonlib.time_to_datetime(time)
            datax+=[t]#[time]
            datay+=[res]
        datax = dates.date2num(datax)
        ax1.plot(datax,datay,label=user,linewidth=1)

        for status in states:
            datax=list()
            datay=list()
            for time in times:
                res = len([e for e in dataset if e["timestamp"].time() == time and e["username"]==user and e["status"]==status])
                t=recoonlib.time_to_datetime(time)
                datax+=[t]#[time]
                datay+=[res]
            datax = dates.date2num(datax)
            ax1.plot(datax,datay,label=f"{user}:{status}",linewidth=1)
    
    plt.xlabel("Time")
    plt.ylabel("Hits Online at this time")
    plt.xticks([datetime.datetime(year=1970,month=1,day=1,hour=h)for h in range (0,24)])
    myFmt = dates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.legend(bbox_to_anchor=(1,1), loc="upper left")
    plt.title("Total per time per user")
    plt.show()

def per_week():
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)

    wdays=recoonlib.weekdays()
    times=recoonlib.times()
    for user in users:
        datax=list()
        datay=list()
        for wday in wdays:
            for time in times:
                res = len(recoonlib.weekday_time_user(wday, time, user))
                t=datetime.datetime(year=1970,month=1,wday=wday+4,hour=time.hour,minute=time.minute)
                datax+=[t]
                datay+=[res]
        ax1.plot(datax,datay,label=user,linewidth=1)

        for status in states:
            datax=list()
            datay=list()
            for wday in wdays:
                for time in times:
                    res = len(recoonlib.weekday_time_user_status(wday, time, user, status))
                    t=datetime.datetime(year=1970,month=1,wday=wday+4,hour=time.hour,minute=time.minute)
                    datax+=[t]
                    datay+=[res]
            ax1.plot(datax,datay,label=f"{user}:{status}",linewidth=1)
    
    plt.xlabel("Weekday:Time")
    plt.ylabel("Hits Online at this time")
    plt.xticks([datetime.datetime(year=1970,month=1,wday=wday+4,hour=3*h)for h in range (0,24//3) for wday in range(0,7)])
    myFmt = dates.DateFormatter('%H')
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.legend(bbox_to_anchor=(1,1), loc="upper left")
    plt.title("Total per time in a week per user")
    plt.show()

def total():
    colors = plt.rcParams["axes.prop_cycle"]()
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    bars=list()
    categories=list()
    y_pos = range(len(categories))
    accOffset=0
    if len(users)>0:
        offset=0.8/len(users)
        accOffset=-0.3
    for user in users:
        
        categories=list()
        data=list()

        categories+=["Unique Days"]
        data+=[len(set(e["timestamp"].date() for e in dataset if e["username"]==user))]

        # categories+=["lonley"]
        # temp=0
        # times=list(e["timestamp"] for e in dataset)
        # for time in times:
        #     res=len([e for e in dataset if e["timestamp"].time() == time and e.get("channel_id")!=None and e["channel_id"] != "696401199120777247"])
        #     if res==1:
        #         temp+=1
        # data+=[temp]

        categories+=["muted"]
        data+=[len([e for e in dataset if e["username"]==user and e.get("mute")!=None and e.get("self_mute")!=None and e["mute"]==True and e["self_mute"]==True])]

        categories+=["idle"]
        data+=[len([e for e in dataset if e["username"]==user and e["status"]=="idle"])]

        categories+=["dnd"]
        data+=[len([e for e in dataset if e["username"]==user and e["status"]=="dnd"])]

        categories+=["channel"]
        data+=[len([e for e in dataset if e["username"]==user and e.get("channel_id")!=None])]

        categories+=["Total"]
        data+=[len([e for e in dataset if e["username"]==user])]

        y_pos = range(len(categories))
        c = next(colors)["color"]
        bar=ax1.barh([y+accOffset for y in y_pos], data, height=offset,label=user, color=c,edgecolor=c,alpha=0.5)
        bars+=[bar]
        accOffset+=offset
    ax1.legend(labels=users, bbox_to_anchor=(1,1),loc='upper right')
    plt.ylabel("Category")
    plt.xlabel("Hits")
    plt.yticks(y_pos,categories)
    plt.legend(bbox_to_anchor=(1,1), loc="upper left")
    plt.title(label="Total")
    plt.show()

def per_day_median2():
    days=recoonlib.days()
    days.sort()
    bps=list()
    colors = plt.rcParams["axes.prop_cycle"]()
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    accOffset=0
    if len(users)>0:
        offset=0.6/len(users)
        accOffset=-0.2
    for user in users:
        data=list()
        for day in days:
            res=len(recoonlib.day_user(day, user))
            data+=[res]
        data=[x*5/60 for x in data]
        bp=ax1.boxplot(data, vert=0,patch_artist=True,positions=[accOffset], widths=offset)
        c = next(colors)["color"]
        for element in ['boxes', 'whiskers', 'fliers', 'means', 'medians', 'caps']:
            plt.setp(bp[element], color=c, alpha=0.5)
        for patch in bp['boxes']:
            patch.set(facecolor=c)
        bps+=[bp]
        accOffset+=offset
    plt.yticks([])
    ax1.legend([bp["boxes"][0] for bp in bps], users, bbox_to_anchor=(1,1),loc='upper right')
    plt.xlabel("Hours online")
    plt.title(label=f"Total Hours from {user}")
    plt.show()

def per_weekday_median3():
    colors = plt.rcParams["axes.prop_cycle"]()
    fig = plt.figure()#constrained_layout=True
    fig.suptitle(f"Hours online")
    ax1 = fig.add_subplot(111)
    bps=list()
    accOffset=0
    if len(users)>0:
        offset=0.6/len(users)
        accOffset=-0.2
    for user in users:
        boxdata=list()
        for wday in recoonlib.weekdays():
            data=list()
            days=list(set(e["timestamp"].date() for e in dataset if e["timestamp"].weekday()==wday))
            days.sort()
            for day in days:
                res=len(recoonlib.day_user(day, user))
                data+=[res]
            data=[x*5/60 for x in data]
            boxdata+=[data]
        c = next(colors)["color"]
        bp=ax1.boxplot(boxdata, vert=0,patch_artist=True,positions=[y+accOffset for y in range(1,8)], widths=offset)
        for element in ['boxes', 'whiskers', 'fliers', 'means', 'medians', 'caps']:
            plt.setp(bp[element], color=c, alpha=0.5)
        for patch in bp['boxes']:
            patch.set(facecolor=c)
        bps+=[bp]
        accOffset+=offset
    
    ax1.legend([bp["boxes"][0] for bp in bps], users, bbox_to_anchor=(1,1),loc='upper right')
    plt.yticks(range(1,8),["Mo","Di","Mi","Do","Fr","Sa","So"])
    #plt.title(f"{wdays[w]}",y=0.1)
    plt.show()


per_day()
per_weekday()
per_time()
total()
per_day_median2()
per_weekday_median3()