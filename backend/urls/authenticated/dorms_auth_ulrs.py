import flask

from packages import db_aux, qr_generator, au, jwt_aux
from packages.db_connector import TableNames
from packages.log import logger
from helpers import users_helpers

dorms_auth = flask.Blueprint(f"{TableNames.DORMS}_auth", __name__)
# PROXY: /dorms


@dorms_auth.get('/')
def get_dorms():
    query = db_aux.make_select(TableNames.DORMS)
    result = db_aux.get_json_from_query(TableNames.DORMS, query)
    return result


@dorms_auth.get('/<uuid:dorm_id>/')
def get_dorm_by_id(dorm_id):
    query = db_aux.make_select(
        TableNames.DORMS,
        conditions={
            "DormId": dorm_id
        }
    )

    result = db_aux.get_json_from_query(TableNames.DORMS, query)
    return result


@dorms_auth.get('/<uuid:dorm_id>/members/')
def get_dorm_members(dorm_id):
    return users_helpers.get_user_profiles(conditions={"DormId": dorm_id})


@dorms_auth.get('/<uuid:dorm_id>/<int:floor>/users/')
def get_users_by_floor(dorm_id, floor):
    return users_helpers.get_floormates(dorm_id, floor)


@dorms_auth.get('/<uuid:dorm_id>/qr/')
def download_qr(dorm_id):
    query = db_aux.make_select(
        TableNames.DORMS,
        conditions={
            "DormId": dorm_id
        }
    )

    try:
        json_obj = db_aux.get_json_from_query(TableNames.DORMS, query)[0]
    except IndexError:
        logger.error("Incorrect dorm id")
        return "Incorrect dorm id, try checking the id in the link"
    code = json_obj["DormCode"]
    name = json_obj["Name"]
    return qr_generator.download(name, code)


@dorms_auth.post('/')
def add_dorm():
    data = au.get_request_body()

    db_aux.insertify_list(
        TableNames.DORMS,
        data,
        do_insert=True,
        first_column_uuid=True
    )

    return flask.jsonify(data)
