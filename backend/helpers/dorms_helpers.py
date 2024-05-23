import string
import random
import flask

from packages import db_aux, db_connector
from packages.db_connector import TableNames
from packages.log import logger


def get_dorm_id_by_code(dorm_code):
    query = db_aux.make_select(db_connector.TableNames.DORMS, conditions={"DormCode": dorm_code})
    return db_aux.get_json_from_query(db_connector.TableNames.DORMS, query)[0]["DormId"]


def generate_dorm_code():
    codes = get_all_dorm_codes()
    for i in range(1000):
        letters_and_digits = string.ascii_uppercase + string.digits
        code = ''.join(random.choices(letters_and_digits, k=6))
        if code not in codes:
            return code
    logger.error("Unable to generate dorm code")
    flask.abort(500)


def get_all_dorm_codes():
    query = f"""
        SELECT d.DormCode
        FROM {TableNames.DORMS} d;
    """
    ret = db_connector.Connector.chain_queries(query)
    return [elem[0] for elem in ret]


def get_all_dorm_names():
    query = f"""
            SELECT d.Name
            FROM {TableNames.DORMS} d;
        """
    ret = db_connector.Connector.chain_queries(query)
    return [elem[0] for elem in ret]
