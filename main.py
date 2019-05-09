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


def get_arg(arg_name):
    def dummy(request):
        return request.raw_args[arg_name]
    return dummy


aduit_flow = TypeMatcher(
    _type(Left) < - chain(lambda x: x.left if x.left else text("success")),
    _type(Right) < - chain(lambda x: x.right if x.right else text("failure")),
)


def group_handler(request, group):
    flow = group & (lambda x: GroupManager().find_group(x)) & (
        lambda x: x.urgent_schedule) & (lambda x: text(x))
    result = flow.attempt() & aduit_flow
    return result


def new_schedule_handler(request, group):
    title = request & get_arg('title')
    description = request & get_arg('description')
    object_group = group << lazy(lambda x: GroupManager().find_group(x))
    new_schedule = create_schedule(
        title, description, pure(datetime.datetime.now()))
    add_schedule_to_group = composer(lambda group, schedule:
                                     group.add_schedule(schedule)
                                     )(object_group, new_schedule)
    result = add_schedule_to_group.attempt() & aduit_flow
    return result


def new_group_handler(request):
    group_name = request & get_arg('group_name')
    invite_key = request & get_arg('group_invite_key')
    new_group = (create_group(group_name, invite_key) &
                 (lambda x: GroupManager().add_new_group(x))
                 )
    result = new_group.attempt() & aduit_flow
    return result


@lazy
def EffectApp():
    route('/notice/<group>', group_handler)
    route('/new/schedule/<group>', new_schedule_handler)
    route('/new/group', new_group_handler)
    app.run(host="0.0.0.0", port=8000)
    return


EfApp(EffectApp)