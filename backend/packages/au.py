import os
from dotenv import dotenv_values
import flask
import hashlib


def get_config():
    return {
        **dotenv_values("../.env"),
        **os.environ,
    }


def get_environ(*keys):
    ret = [get_config()[key] for key in keys]
    return ret[0] if len(keys) == 1 else ret


def get_request_body():
    if flask.request.is_json:
        return flask.request.json
    else:
        return flask.request.form.to_dict()


def encode_pass(user_pass, salt):
    combined_pass = user_pass + salt + get_environ("PASSWORD_PEPPER")
    return hashlib.sha256(combined_pass.encode()).hexdigest()
