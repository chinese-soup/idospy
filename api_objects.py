
# Dataclass #
from typing import List, Dict
from dataclass_wizard import JSONWizard
from dataclasses import dataclass, field

# Built-ins
from datetime import datetime

@dataclass
class TimeTableItem(JSONWizard):
    """
    'timetableObject': {
        'item': {
            'listId': 301003,
            'item': 716,
            'name': 'Čechovo náměstí'
        }

    """
    listId: int
    item: str
    name: str

class GlobalListItemInfo(object):
    pass

class ObjectsInfo(object):
    pass

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
