import flask


from packages.db_connector import TableNames
from packages import db_aux, jwt_aux, au
from helpers import users_helpers, dorms_helpers


users_auth = flask.Blueprint(f"{TableNames.USERS}_auth", __name__)
# PROXY: /users


@users_auth.get('/')
def get_users():
    query = db_aux.make_select(TableNames.USERS)
    result = db_aux.get_json_from_query(TableNames.USERS, query)
    return result


@users_auth.get('/<uuid:user_id>/')
def get_user_by_id(user_id):
    query = db_aux.make_select(
        TableNames.USERS,
        conditions={
            "UserId": user_id
        }
    )

    result = db_aux.get_json_from_query(TableNames.USERS, query)
    return result


@users_auth.get('/settings_info/')
def show_settings_info():

    if type(flask.g.token) == tuple:
        return flask.g.token
    ret = db_aux.get_json_from_query(None, f"""
        SELECT DepartureDate, RoomNumber, Surname
        FROM users
        WHERE UserId='{flask.g.token["UserId"]}';
    """, ("DepartureDate", "RoomNumber", "SurnameExists"))[0]
    ret["SurnameExists"] = False if ret["SurnameExists"] == "" else True
    return ret


@users_auth.get('/<uuid:user_id>/profile/')
def get_user_profile(user_id):
    return users_helpers.get_user_profiles(conditions={'UserId': user_id})[0]


@users_auth.put('/settings_info/')
def put_user_info():
    data = au.get_request_body()

    if "SuiteCode" in data.keys():
        data["DormId"] = dorms_helpers.get_dorm_id_by_code(data["SuiteCode"])
    if "ProfilePhoto" in data.keys():
        # TODO
        pass
    if "Password" in data.keys():
        data["Password"] = au.encode_pass(data["Password"], users_helpers.get_salt(flask.g.token["UserId"]))
    return db_aux.put_from_json(
        TableNames.USERS,
        data,
        {
            'UserId': flask.g.token['UserId']
        }, ("SuiteCode", "ProfilePhoto")
    )
