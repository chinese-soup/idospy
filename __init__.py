# coding=utf-8

# Built-ins
from datetime import datetime

# Data class stuff #
from typing import Any

# External
import requests

# Locals
from .api_objects import * # TODO: you know...

class IDOSAdapter:
    def __init__(self, comb_id: str, api_user_id: str=None, api_user_desc: str=None, hostname: str=None):
        if not hostname:
            self.hostname = "ext.crws.cz"

        self.url = f"https://{self.hostname}/api"
        self.api_user_id = api_user_id
        self.api_user_desc = api_user_desc

        if not self.api_user_id:
            self.api_user_id = "" # TODO: You are missing userID

        if not self.api_user_desc:
            self.api_user_desc = "" # TODO: You are missing userDesc

        self._combination_id = comb_id

    def post(self, endpoint: str, payload: dict = None, additional_params: dict = None) -> dict:
        if payload is None:
            payload = {}

        # HTTP parameters that the API accepts
        params = {"userID": self.api_user_id,
                  "userDesc": self.api_user_desc}

        if additional_params is not None:
            params.update(additional_params)

        req = requests.post(f"{self.url}/{self._combination_id}/{endpoint}",
                            params=params,
                            json=payload,
                            headers={"Content-type": "text/json"})

        if req.status_code == 200:
            return req.json()
        else:
            raise Exception(req.text)

    def find_connection_simple(self, station_from: str, station_to: str, via: str = None, count: int = 5):
        """
        TODO: Is Any any useful? The API allows and accepts list of from and to stations, but doesn't seem to
        do anything with it? At least not in find_connection_simple aka /connections/, I guess
        :param station_from:
        :param station_to:
        :return:
        """
        payload = {} # params that are accepted by the API as POST payload
        params = {} # params that are accepted by the API as params

        # Don't get confused by the word params.
        # These are just parameters for the API, but are sent in the POST payload!
        connection_params = {"prefereTrains": 1, "autoStrategy": True}

        if isinstance(station_from, str):
            payload["from"] = [ {"name": station_from} ]

        if isinstance(station_to, str):
            payload["to"] = [ {"name": station_to} ]

        if isinstance(via, str):
            payload["via"] = [ {"name": via} ]

        if isinstance(count, int):
            params["maxCount"] = count

        payload["conn_params"] = connection_params

        data = self.post("connections", payload=payload, additional_params=params)
        connections = []

        if data["fromObjects"][0].get("status") == 1:
            raise Exception("'From' object not found.")

        if data["toObjects"][0].get("status") == 1:
            raise Exception("'To' object not found.")

        for i in data["connInfo"]["connections"]:
            instance = Connection.from_dict(i)
            connections.append(instance)

        return connections

    def find_connection(self, stations_from: Any, stations_to: Any):
        pass
