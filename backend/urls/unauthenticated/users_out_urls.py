import flask
import bcrypt
import hashlib

from helpers import users_helpers, dorms_helpers
from packages import au, db_aux, jwt_aux
from packages.db_connector import TableNames
from packages.log import logger


users_out = flask.Blueprint(f"{TableNames.USERS}_out", __name__)
# PROXY: /users


@users_out.post('/login/')
def login_user():
    data = au.get_request_body()

    query = db_aux.make_select(
        TableNames.USERS,
        conditions={
            "Email": data["Email"]
        }
    )

    try:
        result = db_aux.get_json_from_query(TableNames.USERS, query)[0]
    except IndexError:
        logger.error("Incorrect account email")
        return "This email does not have any account connected", 401
    combined_pass = data["Password"] + result["Salt"] + au.get_environ("PASSWORD_PEPPER")
    if hashlib.sha256(combined_pass.encode()).hexdigest() == result["Password"]:
        logger.info(f"Logging in to user: {result['UserId']} correctly completed")
        return jwt_aux.get_token(result["UserId"]), 200
    else:
        logger.error("Incorrect account password")
        return "Password did not match your email", 401


@users_out.post('/register/')
def register_user():
    data = au.get_request_body()

    users_helpers.make_nickname(data)
    data["Salt"] = bcrypt.gensalt().decode("utf-8")
    data["Password"] = au.encode_pass(data["Password"], data["Salt"])
    data["DormId"] = dorms_helpers.get_dorm_id_by_code(data["DormCode"])
    del data["DormCode"]
    users_helpers.default_settings(data)

    if db_aux.insertify_list(
        TableNames.USERS,
        data,
        do_insert=True,
        first_column_uuid=True,
        add_date="RegistrationDate"
    ) == "INTEGRITY_ERROR":
        return "This email already has an account linked to it", 409
    token = jwt_aux.get_token(data["UserId"])
    saved = jwt_aux.save_token(token)
    if type(saved) == tuple:
        logger.info(f"An error has occurred while registering user: {data['UserId']}")
        return saved
    logger.info(f"User: {data['UserId']} has been correctly registered")
    return token
