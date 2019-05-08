import datetime

from fanic import route, app
from sanic.response import text
from lazy.effect import lazy, pure
from lazy.ef_app import EfApp

from group import Group
from schedule import Schedule
from group_manager import GroupManager


def group_handler(request, group):
    return pure(text(GroupManager().find_group(group.execute).urgent_schedule))


def new_schedule_handler(request, group):
    request = request.execute
    try:
        title = request.raw_args['title']
        description = request.raw_args['description']
        new_schedule = Schedule(title, description, datetime.datetime.now())
        GroupManager().find_group(group.execute).add_schedule(new_schedule)
        return pure(text("success"))    
    except Exception as e:
        print(e)
        return pure(text("failure"))


def new_group_handler(request):
    request = request.execute
    try:
        group_name = request.raw_args['group_name']
        invite_key = request.raw_args['group_invite_key']
        new_group = Group(group_name, invite_key)
        GroupManager().add_new_group(new_group)
        return pure(text("success"))
    except Exception as e:
        print(e)
        return pure(text("failure"))


@lazy
def EffectApp():
    route('/notice/<group>', group_handler)
    route('/new/schedule/<group>', new_schedule_handler)
    route('/new/group', new_group_handler)
    app.run(host="0.0.0.0", port=8000)
    return


EfApp(EffectApp)
