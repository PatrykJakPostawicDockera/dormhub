import flask

from packages.log import logger
from packages.db_connector import TableNames
from packages import db_aux, au, jwt_aux

post_types_auth = flask.Blueprint(f"{TableNames.POST_TYPES}_auth", __name__)
# PROXY: /posts/types


@post_types_auth.get('/')
def get_post_types():
    query = db_aux.make_select(TableNames.POST_TYPES)
    result = db_aux.get_json_from_query(TableNames.POST_TYPES, query)
    return result


@post_types_auth.post('/')
def add_post_type():
    data = au.get_request_body()

    db_aux.insertify_list(
        TableNames.POST_TYPES,
        data,
        do_insert=True,
        add_empty=True
    )

    return flask.jsonify(data)
