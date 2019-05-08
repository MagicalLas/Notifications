from utils import Singleton
from group import Group


class GroupManager(Singleton):
    groups = []

    def add_new_group(self, new_group):
        self.groups.append(new_group)

    def find_group(self, group_name):
        for group in self.groups:
            if group.name == group_name:
                return group
        return None
