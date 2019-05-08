import json

from lazy.effect import composer


class Schedule(object):
    def __init__(self, title, description, date):
        self._title = title
        self._desciption = description
        self._date = date

    def __str__(self):
        json_data = {
            "title": self._title,
            "desciption": self._desciption
        }
        return json.dumps(json_data)


@composer
def create_schedule(title, description, date):
    return Schedule(title, description, date)
