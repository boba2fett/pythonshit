from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, Boolean, ForeignKeyConstraint
import requests
from sqlalchemy.sql import select, exists


#DB
newengine = create_engine("sqlite:///dcTgData.db")
oldengine = create_engine("sqlite:///dcdata.db")
newmeta = MetaData()
oldmeta = MetaData()

newdcOn = Table(
'dcOn', newmeta,
Column('timestamp', DateTime(timezone=True), primary_key=True),
Column('username', String, primary_key=True),
Column('status', String),
Column('channel_id', String),
Column('deaf', Boolean),
Column('mute', Boolean)
)

olddcOn = Table(
'dcOn', oldmeta,
Column('timestamp', DateTime(timezone=True)),
Column('username', String),
Column('status', String),
Column('channel_id', String),
Column('deaf', Boolean),
Column('mute', Boolean)
)

subscribe = Table(
'subscribe', newmeta,
Column('timestamp', DateTime(timezone=True)),
Column('chat_id', String, primary_key=True),
Column('dc_user', String, primary_key=True),
Column('username', String),
Column('first_name', String),
Column('last_name', String),
#ForeignKeyConstraint(['username', 'dc_user'], ['dcOn.username', 'subscribe.dc_user'])
)

newmeta.create_all(newengine)
oldmeta.create_all(oldengine)


def status(end=False):
        conn = newengine.connect()
        datasets = conn.execute(select([newdcOn]).count())
        datasets = [x[0] for x in datasets]
        databegin = conn.execute(select([newdcOn.c.timestamp]).order_by(newdcOn.c.timestamp)).first()[0]
        dataend = conn.execute(select([newdcOn.c.timestamp]).order_by(newdcOn.c.timestamp.desc())).first()[0]

        now_online = conn.execute(select([newdcOn.c.username,newdcOn.c.status,newdcOn.c.channel_id]).where(newdcOn.c.timestamp==dataend))
        now_online = "\n".join([f"{x[0]} is {x[1]} in {x[2]}" for x in now_online])
        if not end:
            print(f"datasets: {datasets}, from: [{databegin}], until: [{dataend}]", end="\r")
        else:
            print(f"datasets: {datasets}, from: [{databegin}], until: [{dataend}]")

def insInNew(oldObj):
    conn = newengine.connect()
    conn.execute(newdcOn.insert()
        .values(
            timestamp=oldObj["timestamp"],
            username=oldObj["username"],
            status=oldObj["status"],
            channel_id=oldObj["channel_id"],
            deaf=oldObj["deaf"],
            mute=oldObj["mute"]
        )
    )

def insInNew(oldObj):
    try:
        conn = newengine.connect()
        conn.execute(newdcOn.insert()
            .values(
                timestamp=oldObj["timestamp"],
                username=oldObj["username"],
                status=oldObj["status"],
                channel_id=oldObj["channel_id"],
                deaf=oldObj["deaf"],
                mute=oldObj["mute"]
            )
        )
    except KeyboardInterrupt:
        return False
    except:
        pass
    return True

def migrate():
    conn = oldengine.connect()
    req = conn.execute(select([olddcOn]))
    count = 0
    for obj in req:
        if not insInNew(obj):
            break
        count+=1
        if count > 1000:
            count = 0
            status()
    status(end=True)

print("Start\n")
migrate()