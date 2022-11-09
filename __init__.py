# coding=utf-8

# Locals
from datetime import datetime

# Data class stuff #
from typing import Any, List, Dict
from dataclass_wizard import JSONWizard
from dataclasses import dataclass, field

# External
import requests


class TimeTableItem(object):
    def __init__(self, listId, item, name):
        """
        'timetableObject': {
            'item': {
                'listId': 301003,
                'item': 716,
                'name': 'Čechovo náměstí'
            }

        :param listId:
        :param item:
        :param name:
        """
        self.listId = listId
        self.item = item
        self.name = name

class GlobalListItemInfo(object):
    pass

class ObjectsInfo(object):
    pass

class TrainData(JSONWizard):
    """ 'trainData': {
              'info': {
                'train': 27564,
                'num1': '99',
                'type': 'NTram',
                'typeName': 'tramvaj noční',
                'flags': 2097184,
                'color': 255,
                'id': 3
              },"""

class TimeTableObject(object):
    pass

@dataclass
class TrainDataInfo(JSONWizard):
    color: int
    flags: int
    id: int
    num1: str
    train: int
    type: str
    typeName: str

@dataclass
class TrainData(JSONWizard):
    info: TrainDataInfo
    route: List[Dict]

@dataclass
class Train(JSONWizard):
    dateTime1: str
    dateTime2: str
    delay: int
    trainData: TrainData
    delayQuery: str = field(default=0)
    timeLength: str = field(default=0)
    dateTime_start: datetime = field(default=datetime)
    dateTime_end: datetime = field(default=datetime)

    def __post_init__(self):
        self.dateTime_start = datetime.strptime(self.dateTime1, "%d.%m.%Y %H:%M")
        self.dateTime_end = datetime.strptime(self.dateTime2, "%d.%m.%Y %H:%M")


@dataclass
class Connection(JSONWizard):
    id: int
    timeLength: str
    trains: List[Train]

class IDOSAdapter:
    def __init__(self, comb_id: str, userID: str=None, userDesc: str=None, hostname: str=None):
        if not hostname:
            self.hostname = "ext.crws.cz"

        self.url = f"https://{self.hostname}/api"
        self.api_user_id = userID
        self.api_user_desc = userDesc

        if not self.api_user_id:
            self.api_user_id = "" # TODO: You are missing userID

        if not self.api_user_desc:
            self.api_user_desc = "" # TODO: You are missing userDesc

        self._combination_id = comb_id

    def post(self, endpoint: str, payload=None) -> dict:
        if payload is None:
            payload = {}

        req = requests.post(f"{self.url}/{self._combination_id}/{endpoint}",
                            params={"userID": self.api_user_id,
                                    "userDesc": self.api_user_desc},
                            json=payload,
                            headers={"Content-type": "text/json"})

        if req.status_code == 200:
            return req.json()
        else:
            return req.text # TODO: Obv

    def find_connection_simple(self, station_from: str, station_to: str, via: str=None):
        """
        TODO: Is Any any useful? The API allows and accepts list of from and to stations, but doesn't seem to
        do anything with it? At least not in find_connection_simple aka /connections/, I guess
        :param station_from:
        :param station_to:
        :return:
        """
        payload = {}
        conn_params = {"prefereTrains": 1, "autoStrategy": True}

        if isinstance(station_from, str):
            payload["from"] = [ {"name": station_from} ]

        if isinstance(station_to, str):
            payload["to"] = [ {"name": station_to} ]

        if isinstance(via, str):
            payload["via"] = [ {"name": via} ]

        payload["conn_params"] = conn_params

        data = self.post("connections", payload=payload)
        connections = []

        for i in data["connInfo"]["connections"]:
            # print(i["trains"], end="\n\n")
            instance = Connection.from_dict(i)
            connections.append(instance)

        return connections

    def find_connection(self, stations_from: Any, stations_to: Any):
        pass