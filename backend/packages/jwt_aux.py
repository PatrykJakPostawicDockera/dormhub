import jwt
import flask
import datetime

from packages import au, db_aux, db_connector
from packages.db_connector import TableNames
from packages.log import logger


def encode(**kwargs):
    return jwt.encode(kwargs, au.get_environ("JWT_SECRET"), algorithm="HS256")


def get_token(user_id):
    query = f"""
    SELECT u.*, d.DormId, d.Address, d.Name AS DormName
    FROM {TableNames.DORMS} d
    JOIN {TableNames.USERS} u on d.DormId = u.DormId
    WHERE u.UserId='{user_id}';
    """
    # u.UserId, u.Nickname, u.RoomNumber, u.AvatarUrl, u.IsAdmin, d.DormId, d.Address, d.Name
    res = db_aux.get_json_from_query(TableNames.USERS, query, ("DormId", "Address", "Name"))[0]
    keys = {"UserId", "Nickname", "RoomNumber", "AvatarUrl", "IsAdmin", "DormId", "Address", "Name"}
    filtered_res = {key: value for key, value in res.items() if key in keys}
    return encode(**filtered_res)


def read_token():
    token = flask.request.headers.get(au.get_environ("TOKEN_HEADER_KEY"))
    if token and token.startswith('Bearer '):
        jwt_token = token.split(' ')[1]
        return jwt_token
    return None


def decode_token(token):
    if token is None:
        return "Unauthorized", 401
    try:
        return jwt.decode(token, au.get_environ("JWT_SECRET"), algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return "Token is expired", 401
    except jwt.InvalidTokenError:
        return "Invalid token", 401


def verify_token(token) -> bool:
    return token in get_tokens()


def get_tokens():
    res = db_connector.Connector.chain_queries(f"""
        SELECT s.SessionToken
        FROM {TableNames.SESSIONS} s
        WHERE CURDATE() < s.ExpirationDate;
    """)
    return [elem[0] for elem in res]


def save_token(token):
    decoded = decode_token(token)
    if type(decoded) == tuple:
        flask.abort(decoded[1])
        return "Token error", 500
    elif type(decoded) == dict:
        exp_date = datetime.datetime.now() + datetime.timedelta(hours=int(au.get_environ("TOKEN_HOURS")))
        data = [{
            "SessionToken": token,
            "UserId": str(decoded["UserId"]),
            "ExpirationDate": exp_date
        }]
        db_aux.insertify_list(
            TableNames.SESSIONS,
            data,
            do_insert=True,
            first_column_uuid=True
        )
