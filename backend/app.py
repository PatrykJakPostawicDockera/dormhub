import flask
from flask_cors import CORS

from packages import db_connector, db_aux
from packages.log import logger, start_logging
from urls.authenticated_urls import authenticated
from urls.unauthenticated_urls import unauthenticated

app = flask.Flask(__name__)
CORS(app)

app.register_blueprint(authenticated)
app.register_blueprint(unauthenticated)

start_logging()
logger.debug(app.url_map)


@app.route("/")
def hello_world():
    return db_aux.get_primary_key(db_connector.TableNames.TASKS_SCHEDULE)


# noinspection SqlResolve
@app.route("/debugdb/")
def debug_db():
    val = db_connector.Connector.chain_queries([
        "DROP TABLE IF EXISTS test;",
        "CREATE TABLE test(i int primary key, v varchar(255))",
        "INSERT INTO test VALUES(1,'a');",
        "SELECT * FROM test;",
        "DROP TABLE test;"
    ])
    if val[3] == ((1, 'a'),):
        return "Database connection tested successfully"
    else:
        return f"Database connection tested unsuccessfully, test tuple: {val}"


if __name__ == '__main__':
    app.run(debug=True)
