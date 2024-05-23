from packages import db_connector, db_aux
from packages.db_connector import TableNames
import datetime
from dateutil.relativedelta import relativedelta


def make_nickname(data):
    if data["Nickname"] == "":
        name = data["Name"]
        surname = data["Surname"]
        data["Nickname"] = f"{name} {surname}" if surname != "" else name


def default_settings(data):
    data.update({
        "ShowSurname": True,
        "ShowAge": True,
        "ShowDate": True,
        "ShowEmail": True,
        "ShowPhone": True,
        "ShowSocial": True
    })


def get_salt(user_id):
    query = f"""
        SELECT Salt
        FROM {TableNames.USERS} u
        WHERE u.UserId='{user_id}'
    """
    return db_connector.Connector.chain_queries(query)[0][0]


def get_user_profiles(**kwargs):
    ret = []
    query = db_aux.make_select(TableNames.USERS, **kwargs)
    res = db_aux.get_json_from_query(TableNames.USERS, query)
    for user in res:
        used_keys = {"UserId", "Name", "Nickname", "Nationality", "RoomNumber", "Gender", "AvatarUrl", "AboutMe"}
        if user["ShowSurname"]:
            used_keys.add("Surname")
        if user["ShowDate"]:
            used_keys.add("ArrivalDate")
            used_keys.add("DepartureDate")
        if user["ShowEmail"]:
            used_keys.add("Email")
        if user["ShowPhone"]:
            used_keys.add("PhoneNumber")
        if user["ShowSocial"]:
            used_keys.add("InstagramLink")
            used_keys.add("FacebookLink")
        if user["ShowAge"]:
            birthday = user["Birthday"]
            today = datetime.date.today()
            user["Age"] = relativedelta(today, birthday).years
            used_keys.add("Age")
        ret.append({key: value for key, value in user.items() if key in used_keys})
    return ret


def get_floormates(dorm_id, floor):
    query = f"""
        SELECT *
        FROM {TableNames.USERS}
        WHERE DormId='{dorm_id}'
        AND RoomNumber LIKE '{floor}%'
    """
    return db_aux.get_json_from_query(TableNames.USERS, query)


def get_floor(user_id):
    query = f"""
        SELECT RoomNumber
        FROM {TableNames.USERS}
        WHERE UserID='{user_id}';
    """
    ret = db_connector.Connector.chain_queries(query)
    room = ret[0][0]
    return room[0]
