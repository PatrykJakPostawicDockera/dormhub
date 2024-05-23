import flask

from packages import db_aux
from packages.db_connector import TableNames

nationalities_out = flask.Blueprint(f"{TableNames.NATIONALITIES}_out", __name__)
# PROXY: /nationalities


@nationalities_out.get('/')
def get_nationalities():
    query = db_aux.make_select(
        TableNames.NATIONALITIES,
        order_by="Nationality"
    )

    result = db_aux.get_json_from_query(TableNames.NATIONALITIES, query)
    return result


@nationalities_out.get('/<int:nationality_id>/')
def get_nationality_by_id(nationality_id):
    query = db_aux.make_select(
        TableNames.NATIONALITIES,
        order_by="Nationality",
        conditions={"NationalityId": nationality_id}
    )

    return db_aux.get_json_from_query(TableNames.NATIONALITIES, query)[0]
