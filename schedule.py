import json

from lazy.effect import composer


class Schedule(object):
    def __init__(self, title, description, date):
        self._title = title
        self._desciption = description
        self._date = date

    @property
    def rendered_html(self):
        return """<div class="card" style="width: 20rem;"><img class="card-img-top" src="https://github.com/Las-Wonho/Notifications/raw/master/icon.png" alt="Card image cap"><div class="card-body"><h4 class="card-title">{title}</h4><p class="card-text">{des}</p></div></div>""".format(title=self._title, des=self._desciption)

    def __str__(self):
        json_data = {
            "title": self._title,
            "desciption": self._desciption
        }
        return json.dumps(json_data)


@composer
def create_schedule(title, description, date):
    return Schedule(title, description, date)
