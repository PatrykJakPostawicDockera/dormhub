import flask

from packages.db_connector import TableNames
from packages import db_aux, au, db_connector
from helpers import users_helpers, tasks_helpers
from packages.log import logger


tasks_auth = flask.Blueprint("tasks_auth", __name__)
# PROXY: /tasks


@tasks_auth.get("/")
def get_tasks():
    query = db_aux.make_select(TableNames.TASKS_SCHEDULE)
    return db_aux.get_json_from_query(TableNames.TASKS_SCHEDULE, query)


@tasks_auth.post("/create/")
def create_task():
    body = au.get_request_body()
    body["TaskCreator"] = flask.g.token["UserId"]
    query, task_id = db_aux.insertify_list(
        TableNames.TASKS_SCHEDULE,
        body,
        skip=("Assignees",),
        first_column_uuid=True,
        return_uuid=True
    )
    floor_mates = users_helpers.get_floormates(flask.g.token["DormId"], body["Floor"])
    floor_mates_by_nicks = {item.pop("Nickname"): item for item in floor_mates}
    for assignee in body["Assignees"]:
        assignee_obj = floor_mates_by_nicks[assignee["AssigneeNick"]]
        assignee["TaskAssigneeId"] = 0
        assignee["TaskAssignee"] = assignee_obj["UserId"]
        assignee["TaskId"] = str(task_id[0])
    db_aux.get_json_from_query(TableNames.TASKS_SCHEDULE, query)
    db_aux.insertify_list(
        TableNames.TASK_ASSIGNEE,
        body["Assignees"],
        do_insert=True,
        add_empty=True
    )
    return "Query OK", 200


@tasks_auth.get("/mytasks/")
def show_tasks_by_user():
    return tasks_helpers.show_tasks(f"""
            AND ua.UserId='{flask.g.token['UserId']}'
        """), 200


@tasks_auth.get("/myfloor/")
def show_tasks_by_floor():
    floor = users_helpers.get_floor(flask.g.token["UserId"])
    return tasks_helpers.show_tasks(f"""
            AND ua.RoomNumber LIKE'{floor}%'
        """), 200
