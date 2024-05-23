import flask

from packages.log import logger
from packages import jwt_aux
from urls.authenticated.dorms_auth_ulrs import dorms_auth
from urls.authenticated.nationalities_auth_urls import nationalities_auth
from urls.authenticated.comments_auth_urls import comments_auth
from urls.authenticated.posts_auth_urls import posts_auth
from urls.authenticated.users_auth_ulrs import users_auth
from urls.authenticated.post_types_auth_urls import post_types_auth
from urls.authenticated.inner_auth_urls import inner_auth
from urls.authenticated.tasks_auth_urls import tasks_auth


authenticated = flask.Blueprint("authenticated", __name__)


@authenticated.before_request
def authentication():
    token = jwt_aux.read_token()
    if jwt_aux.verify_token(token):
        flask.g.token = jwt_aux.decode_token(token)
        if type(flask.g.token) == tuple:
            flask.abort(flask.g.token[1])
    else:
        logger.warning(token)
        flask.abort(401)


authenticated.register_blueprint(dorms_auth, url_prefix="/dorms")
authenticated.register_blueprint(nationalities_auth, url_prefix="/nationalities")
authenticated.register_blueprint(comments_auth)
authenticated.register_blueprint(posts_auth)
authenticated.register_blueprint(users_auth, url_prefix="/users")
authenticated.register_blueprint(post_types_auth, url_prefix="/posts/types")
authenticated.register_blueprint(inner_auth, url_prefix="/inner")
authenticated.register_blueprint(tasks_auth, url_prefix="/tasks")
