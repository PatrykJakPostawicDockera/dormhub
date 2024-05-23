import flask

from packages import db_aux, au
from packages.db_connector import TableNames
from packages.log import logger

nationalities_auth = flask.Blueprint(f"{TableNames.NATIONALITIES}_auth", __name__)
# PROXY: /nationalities


@nationalities_auth.post('/')
def add_nationality():
    data = au.get_request_body()

    db_aux.insertify_list(
        TableNames.NATIONALITIES,
        data,
        do_insert=True,
        add_empty=True
    )

    return flask.jsonify(data)
