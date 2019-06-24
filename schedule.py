import json

from lazy.effect import composer


class Schedule(object):
    def __init__(self, title, description, date):
        self._title = title
        self._desciption = description
        self._date = date
        self._html_template = """<div class="row"><div class="col-sm-6"><div class="card" style="width: 20rem;"><img class="card-img-top" src="https://github.com/Las-Wonho/Notifications/raw/master/icon.png" alt="Card image cap"><div class="card-body"><h4 class="card-title">{title}</h4><p class="card-text">{des}</p><a class="btn btn-primary" onmousedown="FinishSchedule()">스케줄 완료하기</a></div></div></div><div class="col-sm-6"> <div class="card" style="width: 20rem;"><img class="card-img-top" src="https://github.com/Las-Wonho/Notifications/raw/master/icon.png" alt="Card image cap"><div class="card-body"><h4 class="card-title">New Schedule</h4><p class="card-text">새로운 스케줄을 생성할 수 있습니다.</p><a class="btn btn-primary" onmousedown="CreateNewScheduleFrom()">새로운 스케줄 생성하기</a></div></div></div></div>"""

    @property
    def rendered_html(self):
        return self._html_template.format(title=self._title, des=self._desciption)

    def __str__(self):
        json_data = {
            "title": self._title,
            "desciption": self._desciption
        }
        return json.dumps(json_data)


@composer
def create_schedule(title, description, date):
    return Schedule(title, description, date)
