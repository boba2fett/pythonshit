#!/usr/bin/env python3
import requests
import datetime

from config import CONFIG

states=CONFIG["states"]

def todate(x):
    return datetime.datetime.fromtimestamp(x)

def time_to_datetime(time):
    return datetime.datetime(year=1970,month=1,day=1,hour=time.hour,minute=time.minute)

def getAll():
    db = CONFIG["db_server"]
    user = CONFIG["db_server_user"]
    pwd = CONFIG["db_server_pass"]
    auth = (user, pwd)
    dataset = requests.get(db+"/log",  auth=auth).json()
    for element in dataset:
        element["timestamp"] = todate(element["timestamp"])
    return dataset

dataset=getAll()

_dayscache=None
def _days():
    days=list(set(e["timestamp"].date() for e in dataset))
    days.sort()
    return days
    
def days():
    global _dayscache
    if _dayscache:
        return _dayscache
    _dayscache = _days()
    return _dayscache

def weekdays():
    return list(range(0,7))

_timescache=None

def _times():
    times = list(set(e["timestamp"].time() for e in dataset))
    times.sort()
    return times

def times():
    global _timescache
    if _timescache:
        return _timescache
    _timescache = _times()
    return _timescache

def weekdays_names():
    return ["Mo","Di","Mi","Do","Fr","Sa","So"]

_day_user_cache=dict()

def _day_user(day, user):
    return [e for e in dataset if e["timestamp"].date() == day and e["username"]==user]

def day_user(day, user):
    key=str(day)+user
    if _day_user_cache.get(key)!=None:
        return _day_user_cache.get(key)
    _day_user_cache[key]=_day_user(day, user)
    return _day_user_cache.get(key)

_day_user_status_cache=dict()

def _day_user_status(day, user, status):
    return [e for e in dataset if e["timestamp"].date() == day and e["username"]==user and e["status"]==status]

def day_user_status(day, user, status):
    key=str(day)+user+status
    if _day_user_status_cache.get(key)!=None:
        return _day_user_status_cache.get(key)
    _day_user_status_cache[key]=_day_user_status(day, user, status)
    return _day_user_status_cache.get(key)

_weekday_user_cache=dict()

def _weekday_user(weekday, user):
    return [e for e in dataset if e["timestamp"].weekday() == weekday and e["username"]==user]

def weekday_user(weekday, user):
    key=str(weekday)+user
    if _weekday_user_cache.get(key)!=None:
        return _weekday_user_cache.get(key)
    _weekday_user_cache[key]=_weekday_user(weekday, user)
    return _weekday_user_cache.get(key)

_weekday_user_status_cache=dict()

def _weekday_user_status(weekday, user, status):
    return [e for e in dataset if e["timestamp"].weekday() == weekday and e["username"]==user and e["status"]==status]

def weekday_user_status(weekday, user, status):
    key=str(weekday)+user+status
    if _weekday_user_status_cache.get(key)!=None:
        return _weekday_user_status_cache.get(key)
    _weekday_user_status_cache[key]=_weekday_user_status(weekday, user, status)
    return _weekday_user_status_cache.get(key)

_time_user_cache=dict()

def _time_user(time, user):
    return [e for e in dataset if e["timestamp"].time() == time and e["username"]==user]

def time_user(time, user):
    key=str(time)+user
    if _time_user_cache.get(key)!=None:
        return _time_user_cache.get(key)
    _time_user_cache[key]=_time_user(time, user)
    return _time_user_cache.get(key)

_time_user_status_cache=dict()

def _time_user_status(time, user, status):
    return [e for e in dataset if e["timestamp"].time() == time and e["username"]==user and e["status"]==status]

def time_user_status(time, user, status):
    key=str(time)+user+status
    if _time_user_status_cache.get(key)!=None:
        return _time_user_status_cache.get(key)
    _time_user_status_cache[key]=_time_user_status(time, user, status)
    return _time_user_status_cache.get(key)

_weekday_time_user_cache=dict()

def _weekday_time_user(weekday, time, user):
    return [e for e in dataset if e["timestamp"].weekday() == weekday and e["timestamp"].time() == time and e["username"]==user]

def weekday_time_user(weekday, time, user):
    key=str(weekday)+str(time)+user
    if _weekday_time_user_cache.get(key)!=None:
        return _weekday_time_user_cache.get(key)
    _weekday_time_user_cache[key]=_weekday_time_user(weekday, time, user)
    return _weekday_time_user_cache.get(key)

_weekday_time_user_status_cache=dict()

def _weekday_time_user_status(weekday, time, user, status):
    return [e for e in dataset if e["timestamp"].weekday() == weekday and e["timestamp"].time() == time and e["username"]==user and e["status"]==status]

def weekday_time_user_status(weekday, time, user, status):
    key=str(weekday)+str(time)+user+status
    if _weekday_time_user_status_cache.get(key)!=None:
        return _weekday_time_user_status_cache.get(key)
    _weekday_time_user_status_cache[key]=_weekday_time_user_status(weekday, time, user, status)
    return _weekday_time_user_status_cache.get(key)
