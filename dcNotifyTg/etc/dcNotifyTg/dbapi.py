import time
from datetime import datetime
import requests

class DbApi():

    def __init__(self, dburl, user, pwd):
        self.auth = (user, pwd)
        self.dburl = dburl
    
    def dbCollect(self, data):
        req = requests.post(self.dburl+"/log/insert", json=data)
        if req.status_code != 201:
            raise Exception(req.json())

    def users(self):
        return requests.post(self.dburl+"/log/distinct/username", json={}, auth=self.auth).json()

    def subscribedUsers(self):
        return requests.post(self.dburl+"/subscribe/distinct/dc_user", json={}, auth=self.auth).json()

    def chatSubscribedUsers(self, chat_id):
        return requests.post(self.dburl+"/subscribe/filter", json={"chat_id": chat_id}, auth=self.auth).json()

    def lastState(self, username):
        return requests.post(self.dburl+"/log/last/timestamp", json={"username": username}, auth=self.auth).json()

    def subscribers(self, dc_user):
        chat_ids = requests.post(self.dburl+"/subscribe/distinct/chat_id", json={"dc_user": dc_user}, auth=self.auth).json()
        potential = requests.post(self.dburl+"/subscribe/filter", json={
            "dc_user": dc_user,
            "chat_id": {"$in": chat_ids},
            "active": True
        }, auth=self.auth).json()
        potential_not = requests.post(self.dburl+"/subscribe/filter", json={
            "dc_user": dc_user,
            "chat_id": {"$in": chat_ids},
            "active": False
        }, auth=self.auth).json()
        subscribers = list()
        for subscribed in potential:
            #not_subscribed = potential_not.find(x => x["chat_id"] == subsc["chat_id"])
            not_subscribed = [x for x in potential_not if x["chat_id"] == subscribed["chat_id"]]
            not_subscribed = not_subscribed[0] if len(not_subscribed) > 0 else None
            if not_subscribed is None or subscribed["timestamp"] > not_subscribed["timestamp"]: 
                subscribers += [subscribed["chat_id"]]
        return subscribers

    def newSubscriber(self, chat_id,dc_user, username, first_name, last_name):
        state = requests.post(self.dburl+"/subscribe/last/timestamp", auth=self.auth, json=
            {
                "chat_id": chat_id,
                "dc_user": dc_user
            }
        ).json()
        if state is None or not state["active"]:
            requests.post(self.dburl+"/subscribe/insert", auth=self.auth, json=
                [{
                    "timestamp": time.time(),
                    "chat_id": chat_id,
                    "dc_user": dc_user,
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                    "active": True
                }]
            )

    def rmSubscriber(self, chat_id, dc_user):
        state = requests.post(self.dburl+"/subscribe/last/timestamp", auth=self.auth, json=
            {
                "chat_id": chat_id,
                "dc_user": dc_user
            }
        ).json()
        if state is None or state["active"]:
            requests.post(self.dburl+"/subscribe/insert", auth=self.auth, json=
                [{
                    "timestamp": time.time(),
                    "chat_id": chat_id,
                    "dc_user": dc_user,
                    "active": False
                }]
            )

    def test(self):
        #try:
            return f"Started, db seems to work\nStatus:\n"+self.adminStatus()
        #except Exception as e:
            #return f"Started, db doesn't seem to work: {e}"


    def adminStatus(self):
        if requests.post(self.dburl+"/log/last/timestamp", json={}, auth=self.auth).status_code == 200:
            subscribtions = requests.post(self.dburl+"/subscribe/count", json={}, auth=self.auth).json()
            datasets = requests.post(self.dburl+"/log/count", json={}, auth=self.auth).json()
            until = requests.post(self.dburl+"/log/last/timestamp", json={}, auth=self.auth).json()
            until = datetime.fromtimestamp(until["timestamp"])
            return f"""
subscribtions: {subscribtions}
datasets: {datasets}
until: [{until}]
"""
        else:
            return "Not used"

    def adminStatus_for(self, dc_user):
        return self.subscribers(dc_user)