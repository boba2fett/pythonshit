#!/usr/bin/env python3
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


engine = create_engine('sqlite:///dcdata.db')
meta = MetaData()
conn = engine.connect()

dcOn = Table(
'dcOn', meta,
Column('timestamp', DateTime(timezone=True)),
Column('username', String),
Column('status', String),
Column('channel_id', String),
Column('deaf', Boolean),
Column('mute', Boolean),
Column('game',String)
)
meta.create_all(engine)

def total_per_day():
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)

    days=list(conn.execute("SELECT DISTINCT date(timestamp) FROm dcOn ORDER BY date(timestamp)"))
    datax=list()
    datay=list()
    for day in [x[0] for x in days]:
        res=list(conn.execute(f'SELECT COUNT(DISTINCT username) FROM dcOn WHERE date(timestamp)="{day}"'))
        y,m,d=day.split("-")
        t=datetime.datetime(year=int(y),month=int(m),day=int(d))
        datax+=[t]
        datay+=res[0]
    datax = dates.date2num(datax)
    ax1.plot(datax,datay,label="Total per day",linewidth=1)
    plt.xlabel("Day")
    plt.ylabel("Number of unique users")
    plt.xticks([datetime.datetime(year=int(t[0]),month=int(t[1]),day=int(t[2])) for t in [(days[i][0].split("-")) for i in range(0,len(days))]])
    myFmt = dates.DateFormatter('%Y-%m-%d')
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.legend(bbox_to_anchor=(1,1), loc="upper left")
    plt.title("Total per day")
    plt.show()

def total_per_weekday():#ignore
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)

    days=list(conn.execute("SELECT DISTINCT strftime('%w',timestamp) FROm dcOn ORDER BY strftime('%w',timestamp)"))
    datax=list()
    datay=list()
    for day in [x[0] for x in days]:
        res=list(conn.execute(f'SELECT COUNT(*) FROM dcOn WHERE strftime("%w",timestamp)="{day}"'))
        datax+=[day]
        datay+=res[0]
    datay=[x*5/60 for x in datay if x!= 0]
    ax1.plot(datax,datay,label="",linewidth=1)
    xticks=["So","Mo","Di","Mi","Do","Fr","Sa"]
    plt.xticks([x for x in range(0,7)], [xticks[x] for x in range(0,7)])
    plt.xlabel("Weekday")
    #plt.yticks([x for x in range(0,int(24*60/5),int(60/5))],[5*x for x in range(0,int(24*60/5),int(60/5))])
    plt.ylabel("Hours online")
    plt.legend(bbox_to_anchor=(1,1), loc="upper left")
    plt.title("Total per weekday")
    plt.show()

def total_per_time():
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    times=list(conn.execute("SELECT DISTINCT time(timestamp) FROM dcOn ORDER BY time(timestamp)"))
    datax=list()
    datay=list()
    for time in [x[0] for x in times]:
        res=list(conn.execute(f'SELECT COUNT(*) FROM dcOn WHERE time(timestamp)="{time}"'))
        h,m,_=time.split(":")
        t=datetime.datetime(year=1970,month=1,day=1,hour=int(h),minute=int(m))
        datax+=[t]
        datay+=res[0]
    datax = dates.date2num(datax)
    ax1.plot(datax,datay,label="Total",linewidth=1)
    plt.xlabel("Time")
    plt.ylabel("Hits Online at this time all users allocated")
    plt.xticks([datetime.datetime(year=1970,month=1,day=1,hour=h)for h in range (0,24)])
    myFmt = dates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.legend(bbox_to_anchor=(1,1), loc="upper left")
    plt.title("Total per time")
    plt.show()

def total_per_day_median():
    days=list(conn.execute("SELECT DISTINCT date(timestamp) FROm dcOn ORDER BY date(timestamp)"))
    fig = plt.figure()
    ax1 = fig.add_subplot(2,1,1)
    data=list()
    for day in [x[0] for x in days]:
        res=list(conn.execute(f'SELECT COUNT(*) FROM dcOn WHERE date(timestamp)="{day}"'))
        data+=res[0]
    data=[x*5/60 for x in data if x!= 0]
    ax1.boxplot(data, vert=0)
    plt.xlabel("Minutes online")
    plt.legend(bbox_to_anchor=(1,1), loc="upper left")
    plt.title(label=f"Total Minutes")
    plt.show()

total_per_day()
total_per_day_median()
total_per_weekday()
total_per_time()