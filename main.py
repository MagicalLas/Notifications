import datetime

from fanic import route, app
from sanic.response import text
from lazy.effect import lazy, pure, composer
from lazy.ef_app import EfApp
from lazy.typematcher import _type, chain, TypeMatcher
from lazy.either import Left, Right

from group import Group, create_group
from schedule import Schedule, create_schedule
from group_manager import GroupManager


def group_handler(request, group):
    return pure(text(GroupManager().find_group(group.execute).urgent_schedule))


def new_schedule_handler(request, group):
    title = request & (lambda x: x.raw_args['title'])
    description = request & (lambda x: x.raw_args['description'])
    object_group = group << lazy(lambda x: GroupManager().find_group(x))
    new_schedule = create_schedule(title, description, pure(datetime.datetime.now()))
    add_schedule_to_group = composer(lambda group, schedule:
                                     group.add_schedule(schedule)
                                     )(object_group, new_schedule).attempt()

    result = add_schedule_to_group & TypeMatcher(
        _type(Left) < - chain(lambda x: text("success")),
        _type(Right) < - chain(lambda x: text("failure")),
    )
    return result


def new_group_handler(request):
    group_name = request & (lambda x: x.raw_args['group_name'])
    invite_key = request & (lambda x: x.raw_args['group_invite_key'])
    new_group = (create_group(group_name, invite_key) &
                 (lambda x: GroupManager().add_new_group(x))
                 ).attempt()
    result = new_group & TypeMatcher(
        _type(Left) < - chain(lambda x: text("success")),
        _type(Right) < - chain(lambda x: text("failure")),
    )
    return result


@lazy
def EffectApp():
    route('/notice/<group>', group_handler)
    route('/new/schedule/<group>', new_schedule_handler)
    route('/new/group', new_group_handler)
    app.run(host="0.0.0.0", port=8000)
    return


EfApp(EffectApp)
