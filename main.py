import datetime

from fanic import route, app
from sanic.response import text, html
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


def get_group(group_name):
    return GroupManager().find_group(group_name)


aduit_flow = TypeMatcher(
    _type(Left) < - chain(lambda x: x.left if x.left else text("success")),
    _type(Right) < - chain(lambda x: text("failure")),
)

f = open("./main.html", 'r', encoding="utf-8")
lines = f.readlines()
main_page = ""
for i in lines:
    main_page += i
main_page += ""

g = open("./group_view.html", 'r', encoding="utf-8")
lines = g.readlines()
group_page = ""
for i in lines:
    group_page += i
group_page += ""


def main_page_handler(request):
    return pure(html(main_page))


def group_page_handler(request, group):
    return pure(html(group_page))


def group_handler(request, group):
    flow = (group &
            get_group &
            (lambda x: x.invite_key) &
            (lambda x: (x == request.execute.raw_args['invite_key'])))
    is_available_code = (flow & aduit_flow).execute
    if is_available_code:
        flow = (group &
                (lambda x: GroupManager().find_group(x)) &
                (lambda x: x.urgent_schedule) &
                (lambda x: text(x.rendered_html) if isinstance(x, Schedule) else text(x)))
        result = flow.attempt()
        return result & aduit_flow
    else:
        return pure(text("Error"))


def invite_key_handler(request, group):
    flow = (group &
            get_group &
            (lambda x: x.invite_key) &
            (lambda x: "success" if x == request.execute.raw_args['invite_key'] else "failure") &
            (lambda x: text(x)))
    return flow & aduit_flow


def new_schedule_handler(request, group):
    title = request & get_arg('title')
    description = request & get_arg('description')
    object_group = group & get_group
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
    route('/', main_page_handler)
    route('/notice/<group>', group_page_handler)
    route('/schedule/<group>', group_handler)
    route('/new/schedule/<group>', new_schedule_handler)
    route('/new/group', new_group_handler)
    route('/invite_key/<group>', invite_key_handler)
    app.run(host="0.0.0.0", port=8000)
    return


EfApp(EffectApp)
