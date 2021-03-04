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
        return requests.post(self.dburl+"/subscribe/distinct/chat_id", json={"dc_user": dc_user}, auth=self.auth).json()

    def newSubscriber(self, chat_id,dc_user, username, first_name, last_name):
        requests.post(self.dburl+"/subscribe/insert", auth=self.auth, json=
            [{
                "timestamp": time.time(),
                "chat_id": chat_id,
                "dc_user": dc_user,
                "username": username,
                "first_name": first_name,
                "last_name": last_name
            }]
        )
    
    def rmSubscriber(self, chat_id, dc_user):
        requests.post(self.dburl+"/subscribe/delete", auth=self.auth, json=
            {
                "chat_id": chat_id,
                "dc_user": dc_user
            }
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