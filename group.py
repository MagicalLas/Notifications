from utils import formating_string
from lazy.effect import composer


class Group(object):

    EMPTY_SCHEDULE_HTML_TEMPLATE = """<div class="card" style="width: 20rem;"><img class="card-img-top" src="https://github.com/Las-Wonho/Notifications/raw/master/icon.png" alt="Card image cap"><div class="card-body"><h4 class="card-title">New Schedule</h4><p class="card-text">새로운 스케줄을 생성할 수 있습니다.</p><a class="btn btn-primary" onmousedown="CreateNewScheduleFrom()">새로운 스케줄 생성하기</a></div></div>"""

    def __init__(self, group_name, password):
        self._name = formating_string(group_name)
        self._password = password
        self._schedules = []

    def add_schedule(self, schedule):
        try:
            self._schedules.append(schedule)
        except AttributeError:
            self._schedules = [schedule]

    def finish_schedule(self):
        del self._schedules[0]

    @property
    def name(self):
        return self._name

    @property
    def schedule_count(self):
        return len(self._schedules)

    @property
    def invite_key(self):
        return self._password

    @property
    def urgent_schedule(self):
        if not self._schedules:
            return self.EMPTY_SCHEDULE_HTML_TEMPLATE
        return self._schedules[0]


@composer
def create_group(group_name, invite_key):
    return Group(group_name, invite_key)
