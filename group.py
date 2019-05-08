from utils import formating_string


class Group(object):
    def __init__(self, group_name, password):
        self._name = formating_string(group_name)
        self._password = password
        self._schedules = []

    def add_schedule(self, schedule):
        try:
            self._schedules.append(schedule)
        except AttributeError:
            self._schedules = [schedule]

    @property
    def name(self):
        return self._name

    @property
    def schedule_count(self):
        return len(self._schedules)

    @property
    def invite_key(self):
        return self._password
