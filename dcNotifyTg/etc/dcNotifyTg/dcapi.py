import json
import requests
from config import CONFIG

headers = {'User-Agent': CONFIG["User-Agent"]}
ignore = CONFIG["db_ignore"]

class DcApi():

    def parseData(data):
        data=[x for x in data if (not x['username'] in ignore) or (not x.get('channel_id') is None)]
        for member in data:
            if member.get('channel_id') is None:
                member['channel_id']=None
                member['deaf']=None
                member['mute']=None
            else:
                member['deaf']=member['deaf'] or member['self_deaf']
                member['mute']=member['mute'] or member['self_mute']
        return data

    def loadNewData():
        try:
            dcData = requests.get(
                CONFIG["dc_server"], headers=headers).text  # link is under server settings widgets or similar
        except Exception as e:
            raise Exception(f"Server not Reachable: {e}")
        dc = json.loads(dcData)
        if (dc.get('members') is None):
            raise Exception("Ratelimited")
        data=dc['members']
        return data

    def getData():
        return DcApi.parseData(DcApi.loadNewData())