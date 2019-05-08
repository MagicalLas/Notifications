from group_manager import GroupManager
from group import Group


def test_create_group_nameger():
    manager = GroupManager()
    assert manager == GroupManager()
    assert isinstance(manager, GroupManager)


def test_add_new_group():
    new_group = Group('group_name', 'invite_key')
    GroupManager().add_new_group(new_group)
    assert GroupManager().find_group('group_name') == new_group
