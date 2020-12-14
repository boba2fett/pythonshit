#!/usr/bin/env python3
from matplotlib.dates import DAYS_PER_MONTH
from matplotlib.ticker import scale_range
import requests
import time
import json
import os
import sys
import datetime
from systemd.journal import JournalHandler
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func

#import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import numpy as np


engine = create_engine('sqlite:///dcdata.db')
meta = MetaData()
conn = engine.connect()

states=["idle","dnd"]

users = sys.argv[1::]
print(users)

def per_day():
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    days=list(conn.execute("SELECT DISTINCT date(timestamp) FROm dcOn ORDER BY date(timestamp)"))
    for user in users:
        datax=list()
        datay=list()
        for day in [x[0] for x in days]:
            res=list(conn.execute(f'SELECT COUNT(*) FROM dcOn WHERE username = "{user}" AND date(timestamp)="{day}"'))
            y,m,d=day.split("-")
            t=datetime.datetime(year=int(y),month=int(m),day=int(d))
            datax+=[t]
            datay+=res[0]
        datax = dates.date2num(datax)
        ax1.plot(datax,datay,label=user,linewidth=1)

        for status in states:
            datax=list()
            datay=list()
            for day in [x[0] for x in days]:
                res=list(conn.execute(f'SELECT COUNT(*) FROM dcOn WHERE username = "{user}" AND date(timestamp)="{day}" AND status="{status}"'))
                y,m,d=day.split("-")
                t=datetime.datetime(year=int(y),month=int(m),day=int(d))
                datax+=[t]
                datay+=res[0]
            datax = dates.date2num(datax)
            ax1.plot(datax,datay,label=f"{user}:{status}",linewidth=1)
    
    plt.xlabel("Day")
    plt.ylabel("Minutes online")
    #plt.xticks([datetime.datetime(year=int(t[0]),month=int(t[1]),day=int(t[2])) for t in [(days[i][0].split("-")) for i in range(0,len(days))]])
    #plt.yticks([x for x in range(0,int(24*60/5),int(60/5))],[5*x for x in range(0,int(24*60/5),int(60/5))])
    myFmt = dates.DateFormatter('%Y-%m-%d')
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.legend(bbox_to_anchor=(1,1), loc="upper left")
    plt.title(label="Total per day per user")
    plt.show()

def per_weekday():
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    days=list(conn.execute("SELECT DISTINCT strftime('%w',timestamp) FROm dcOn ORDER BY strftime('%w',timestamp)"))
    days=[int(x[0]) for x in days]
    datax=list()
    for user in users:
        datax=list()
        datay=list()
        for day in days:
            res=list(conn.execute(f'SELECT COUNT(*) FROM dcOn WHERE username = "{user}" AND strftime("%w",timestamp)="{day}"'))
            datax+=[day]
            datay+=res[0]
        ax1.plot(datax,datay,label=user,linewidth=1)

        for status in states:
            datax=list()
            datay=list()
            for day in days:
                res=list(conn.execute(f'SELECT COUNT(*) FROM dcOn WHERE username = "{user}" AND strftime("%w",timestamp)="{day}" AND status="{status}"'))
                datax+=[day]
                datay+=res[0]
            ax1.plot(datax,datay,label=f"{user}:{status}",linewidth=1)
    
    xticks=["So","Mo","Di","Mi","Do","Fr","Sa"]
    plt.xticks([x for x in range(0,7)], [xticks[x] for x in range(0,7)])
    plt.xlabel("Weekday")
    #plt.yticks([x for x in range(0,int(24*60/5),int(60/5))],[5*x for x in range(0,int(24*60/5),int(60/5))])
    plt.ylabel("Minutes online")
    plt.legend(bbox_to_anchor=(1,1), loc="upper left")
    plt.title("Total per weekday per user")
    plt.show()

def per_time():
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    times=list(conn.execute("SELECT DISTINCT time(timestamp) FROM dcOn ORDER BY time(timestamp)"))
    for user in users:
        datax=list()
        datay=list()
        for time in [x[0] for x in times]:
            res=list(conn.execute(f'SELECT COUNT(*) FROM dcOn WHERE username = "{user}" AND time(timestamp)="{time}"'))
            h,m,_=time.split(":")
            t=datetime.datetime(year=1970,month=1,day=1,hour=int(h),minute=int(m))
            datax+=[t]
            datay+=res[0]
        datax = dates.date2num(datax)
        ax1.plot(datax,datay,label=user,linewidth=1)

        for status in states:
            datax=list()
            datay=list()
            for time in [x[0] for x in times]:
                res=list(conn.execute(f'SELECT COUNT(*) FROM dcOn WHERE username = "{user}" AND time(timestamp)="{time}" AND status="{status}"'))
                h,m,_=time.split(":")
                t=datetime.datetime(year=1970,month=1,day=1,hour=int(h),minute=int(m))
                datax+=[t]
                datay+=res[0]
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

    wdays=list(conn.execute("SELECT DISTINCT strftime('%w',timestamp) FROm dcOn ORDER BY strftime('%w',timestamp)"))
    wdays=[int(x[0]) for x in wdays]
    times=list(conn.execute("SELECT DISTINCT time(timestamp) FROM dcOn ORDER BY time(timestamp)"))
    times=[x[0] for x in times]

    for user in users:
        datax=list()
        datay=list()
        for day in wdays:
            for time in times:
                res=list(conn.execute(f'SELECT COUNT(*) FROM dcOn WHERE username = "{user}" AND strftime("%w",timestamp)="{day}" AND time(timestamp)="{time}"'))
                h,m,_=time.split(":")
                t=datetime.datetime(year=1970,month=1,day=day+4,hour=int(h),minute=int(m))
                datax+=[t]
                datay+=res[0]
        ax1.plot(datax,datay,label=user,linewidth=1)

        for status in states:
            datax=list()
            datay=list()
            for day in wdays:
                for time in times:
                    res=list(conn.execute(f'SELECT COUNT(*) FROM dcOn WHERE username = "{user}" AND strftime("%w",timestamp)="{day}" AND time(timestamp)="{time}" AND status="{status}"'))
                    h,m,_=time.split(":")
                    t=datetime.datetime(year=1970,month=1,day=day+4,hour=int(h),minute=int(m))
                    datax+=[t]
                    datay+=res[0]
            ax1.plot(datax,datay,label=f"{user}:{status}",linewidth=1)
    
    plt.xlabel("Weekday:Time")
    plt.ylabel("Hits Online at this time")
    plt.xticks([datetime.datetime(year=1970,month=1,day=day+4,hour=3*h)for h in range (0,24//3) for day in range(0,7)])
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
        data+=[len(list(conn.execute(f'SELECT DISTINCT time(timestamp) FROM dcOn WHERE username = "{user}" ORDER BY time(timestamp)')))]

        categories+=["lonley"]
        temp=0
        times=list(conn.execute(f'SELECT timestamp FROM dcOn WHERE username = "{user}" AND channel_id IS NOT NULL AND channel_id != "696401199120777247"'))
        times=[x[0] for x in times]
        for time in times:
            res=list(conn.execute(f'SELECT COUNT(*) FROM dcOn WHERE timestamp = "{time}" AND channel_id IS NOT NULL AND channel_id != "696401199120777247"'))[0]
            if res[0]==1:
                temp+=1
        data+=[temp]

        categories+=["muted"]
        data+=list(conn.execute(f'SELECT COUNT(*) FROM dcOn WHERE username = "{user}" AND mute = 1'))[0]

        categories+=["idle"]
        data+=list(conn.execute(f'SELECT COUNT(*) FROM dcOn WHERE username = "{user}" AND status="idle"'))[0]

        categories+=["dnd"]
        data+=list(conn.execute(f'SELECT COUNT(*) FROM dcOn WHERE username = "{user}" AND status="dnd"'))[0]

        categories+=["channel"]
        data+=list(conn.execute(f'SELECT COUNT(*) FROM dcOn WHERE username = "{user}" AND channel_id IS NOT NULL AND mute != 1'))[0]

        categories+=["Total"]
        data+=list(conn.execute(f'SELECT COUNT(*) FROM dcOn WHERE username = "{user}"'))[0]

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

def per_day_median():
    days=list(conn.execute("SELECT DISTINCT date(timestamp) FROm dcOn ORDER BY date(timestamp)"))
    for user in users:
        fig = plt.figure()
        ax1 = fig.add_subplot(2,1,1)
        data=list()
        for day in [x[0] for x in days]:
            res=list(conn.execute(f'SELECT COUNT(*) FROM dcOn WHERE username = "{user}" AND date(timestamp)="{day}"'))
            data+=res[0]
        data=[x*5/60 for x in data]
        ax1.boxplot(data, vert=0)
        plt.xlabel("Hours online")
        plt.legend(bbox_to_anchor=(1,1), loc="upper left")
        plt.title(label=f"Total Hours from {user}")
        plt.show()

def per_day_median2():
    days=list(conn.execute("SELECT DISTINCT date(timestamp) FROm dcOn ORDER BY date(timestamp)"))
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
        for day in [x[0] for x in days]:
            res=list(conn.execute(f'SELECT COUNT(*) FROM dcOn WHERE username = "{user}" AND date(timestamp)="{day}"'))
            data+=res[0]
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

def per_weekday_median():
    wdays=["So","Mo","Di","Mi","Do","Fr","Sa"]
    for user in users:
        fig = plt.figure()#constrained_layout=True
        fig.suptitle(f"Hours online: {user}")
        for w in range(0,7):
            ax1 = fig.add_subplot(3,3,w+1)
            data=list()
            days=list(conn.execute(f'SELECT DISTINCT date(timestamp) FROM dcOn WHERE username = "{user}" AND strftime("%w",timestamp)="{w}"'))
            for day in [x[0] for x in days]:
                res=list(conn.execute(f'SELECT COUNT(*) FROM dcOn WHERE username = "{user}" AND date(timestamp)="{day}"'))
                data+=res[0]
            data=[x*5/60 for x in data]
            ax1.boxplot(data, vert=0)
            plt.title(f"{wdays[w]}",y=0.1)
        plt.show()
    
def per_weekday_median2():
    wdays=["So","Mo","Di","Mi","Do","Fr","Sa"]
    for user in users:
        fig = plt.figure()#constrained_layout=True
        fig.suptitle(f"Hours online: {user}")
        ax1 = fig.add_subplot(111)
        boxdata=list()
        for w in range(0,7):
            data=list()
            days=list(conn.execute(f'SELECT DISTINCT date(timestamp) FROM dcOn WHERE strftime("%w",timestamp)="{w}"'))
            for day in [x[0] for x in days]:
                res=list(conn.execute(f'SELECT COUNT(*) FROM dcOn WHERE username = "{user}" AND date(timestamp)="{day}"'))
                data+=res[0]
            data=[x*5/60 for x in data]
            boxdata+=[data]
        ax1.boxplot(boxdata, vert=0)
        plt.yticks(range(1,8),["So","Mo","Di","Mi","Do","Fr","Sa"])
        #plt.title(f"{wdays[w]}",y=0.1)
        plt.show()

def per_weekday_median3():
    wdays=["So","Mo","Di","Mi","Do","Fr","Sa"]
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
        for w in range(0,7):
            data=list()
            days=list(conn.execute(f'SELECT DISTINCT date(timestamp) FROM dcOn WHERE strftime("%w",timestamp)="{w}"'))
            for day in [x[0] for x in days]:
                res=list(conn.execute(f'SELECT COUNT(*) FROM dcOn WHERE username = "{user}" AND date(timestamp)="{day}"'))
                data+=res[0]
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
    plt.yticks(range(1,8),["So","Mo","Di","Mi","Do","Fr","Sa"])
    #plt.title(f"{wdays[w]}",y=0.1)
    plt.show()


per_day()
per_weekday()
per_time()
total()
##per_day_median()
per_day_median2()
##per_weekday_median2()
per_weekday_median3()