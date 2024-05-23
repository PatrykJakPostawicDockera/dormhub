import datetime

from packages import db_connector
from packages.db_connector import TableNames


def show_tasks(conditions_sql=""):

    query = f"""
            SELECT ta.TaskDate, ta.TaskRepeats,
               ts.TaskTitle, ts.TaskDescription, ts.IsImportant,
               uc.Nickname AS Creator
            FROM {TableNames.TASK_ASSIGNEE} ta
            JOIN {TableNames.TASKS_SCHEDULE} ts ON ts.TaskId = ta.TaskId
            JOIN {TableNames.USERS} ua ON ta.TaskAssignee = ua.UserId
            JOIN {TableNames.USERS} uc ON ts.TaskCreator = uc.UserId
            WHERE ta.TaskRepeats > 0 OR ta.TaskDate > CURDATE()
            {conditions_sql};
        """

    res = db_connector.Connector.chain_queries(query)
    ret = []
    for row in res:
        nearest_date = nearest_task_date(row[0], row[1])
        ret.append({
            "TaskDate": row[0],
            "TaskRepeats": row[1],
            "TaskTitle": row[2],
            "TaskDescription": row[3],
            "IsImportant": row[4],
            "Creator": row[5],
            "NearestDate": nearest_date
        })

    return ret


def nearest_task_date(first_date: datetime.date, repeat: int) -> datetime.date:
    today = datetime.date.today()
    if first_date > today:
        return first_date
    days_difference = (today - first_date).days
    cycles = days_difference // repeat
    next_task_date = first_date + datetime.timedelta(days=(cycles + 1) * repeat)
    return next_task_date
