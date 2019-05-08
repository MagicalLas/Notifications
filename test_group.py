import datetime
from group import Group
from schedule import Schedule


def test_create_group():
    sadistix_group = Group("Sadistix Coders", "Invite_key")
    assert isinstance(sadistix_group, Group)
    assert sadistix_group.name == "sadistix_coders"
    assert sadistix_group.invite_key == "Invite_key"


def test_add_schedule_to_group():
    sadistix_group = Group("Sadistix Coders", "Invite_key")
    first_schedule = Schedule("Title", "Discription", datetime.datetime.now())
    sadistix_group.add_schedule(first_schedule)
    assert sadistix_group.schedule_count == 1
