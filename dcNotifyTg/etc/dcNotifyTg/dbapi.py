from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, Boolean, ForeignKeyConstraint
from config import CONFIG
import requests
from sqlalchemy.sql import select, exists

headers = {'User-Agent': CONFIG["User-Agent"]}

#DB
engine = create_engine(CONFIG["db_connection"])
meta = MetaData()

dcOn = Table(
'dcOn', meta,
Column('timestamp', DateTime(timezone=True), primary_key=True),
Column('username', String, primary_key=True),
Column('status', String),
Column('channel_id', String),
Column('deaf', Boolean),
Column('mute', Boolean)
)

subscribe = Table(
'subscribe', meta,
Column('timestamp', DateTime(timezone=True)),
Column('chat_id', String, primary_key=True),
Column('dc_user', String, primary_key=True),
Column('username', String),
Column('first_name', String),
Column('last_name', String),
#ForeignKeyConstraint(['username', 'dc_user'], ['dcOn.username', 'subscribe.dc_user'])
)

meta.create_all(engine)

class DbApi():
    
    def dbCollect(data,time):
        conn = engine.connect()
        for member in data:
            conn.execute(dcOn.insert().values(
                    timestamp=time,
                    username=member["username"],
                    status=member["status"],
                    channel_id=member["channel_id"],
                    deaf=member["deaf"],
                    mute=member["mute"]
                )
            )
            

    def dbSend(data):
        for member in data:
            req = requests.get(CONFIG["log_server"], headers=headers, params=
                {
                    "t":CONFIG["log_server_token"],
                    "username": member["username"],
                    "status": member["status"],
                    "channel_id": member["channel_id"],
                    "deaf": member["deaf"],
                    "mute": member["mute"]
                }
            )
            if req.status_code != 200:
                raise Exception(f"No 200 return Code, actual: {req.status_code}")

    def users():
        conn = engine.connect()
        return conn.execute(select([dcOn.c.username]).distinct())

    def subscribedUsers():
        conn = engine.connect()
        return conn.execute(select([subscribe.c.dc_user]).distinct())

    def chatSubscribedUsers(chat_id):
        conn = engine.connect()
        return conn.execute(select([subscribe.c.dc_user]).where(subscribe.c.chat_id == chat_id ))

    def lastState(name):
        conn = engine.connect()
        return conn.execute(dcOn.select()
            .where(dcOn.c.username==name)
            .order_by(dcOn.c.timestamp.desc())
            ).first()

    def subscribers(name):
        conn = engine.connect()
        req = conn.execute(subscribe.select()
            .where(subscribe.c.dc_user==name)
        )
        return [r["chat_id"] for r in req]

    def newSubscriber(chat_id,dc_user, username, first_name, last_name):
        conn = engine.connect()
        conn.execute(subscribe.insert()
            .values(
                timestamp=datetime.now(),
                chat_id = chat_id,
                dc_user = dc_user,
                username = username,
                first_name = first_name,
                last_name = last_name
            )
        )
    
    def rmSubscriber(chat_id,dc_user):
        conn = engine.connect()
        conn.execute(subscribe.delete()
            .where(subscribe.c.chat_id == chat_id)
            .where(subscribe.c.dc_user == dc_user)
        )

    def test():
        try:
            return f"Started, db seems to work\nStatus:\n"+DbApi.adminStatus()
        except Exception as e:
            return f"Started, db doesn't seem to work: {e}"

    def status():
        conn = engine.connect()
        subscribedusers = conn.execute(select([subscribe.c.dc_user]).distinct().count())
        subscribedusers = [x[0] for x in subscribedusers]
        subscribtions = conn.execute(select([subscribe.c.dc_user]).count())
        subscribtions = [x[0] for x in subscribtions]
        datasets = conn.execute(select([dcOn]).count())
        datasets = [x[0] for x in datasets]
        databegin = conn.execute(select([dcOn.c.timestamp]).order_by(dcOn.c.timestamp)).first()[0]
        dataend = conn.execute(select([dcOn.c.timestamp]).order_by(dcOn.c.timestamp.desc())).first()[0]

        return f"""
subscribtions: {subscribtions}
datasets: {datasets}
from: [{databegin}]
until: [{dataend}]
"""

    def adminStatus():
            conn = engine.connect()
            subscribedusers = conn.execute(select([subscribe.c.dc_user]).distinct().count())
            subscribedusers = [x[0] for x in subscribedusers]
            subscribtions = conn.execute(select([subscribe.c.dc_user]).count())
            subscribtions = [x[0] for x in subscribtions]
            datasets = conn.execute(select([dcOn]).count())
            datasets = [x[0] for x in datasets]
            databegin = conn.execute(select([dcOn.c.timestamp]).order_by(dcOn.c.timestamp)).first()[0]
            dataend = conn.execute(select([dcOn.c.timestamp]).order_by(dcOn.c.timestamp.desc())).first()[0]

            actual_subscribtions = conn.execute(select([subscribe.c.username,subscribe.c.dc_user]))
            actual_subscribtions = "\n".join([f"{x[0]} -> {x[1]}" for x in actual_subscribtions])

            now_online = conn.execute(select([dcOn.c.username,dcOn.c.status,dcOn.c.channel_id]).where(dcOn.c.timestamp==dataend))
            now_online = "\n".join([f"{x[0]} is {x[1]} in {x[2]}" for x in now_online])
            return f"""
subscribtions: {subscribtions}
subscribedusers: {subscribedusers}
datasets: {datasets}
from: [{databegin}]
until: [{dataend}]

subsriptions:
{actual_subscribtions}

current:
{now_online}
"""