import flask

from urls.unauthenticated.nationalities_out_urls import nationalities_out
from urls.unauthenticated.users_out_urls import users_out
from urls.unauthenticated.inner_out_urls import inner_out

unauthenticated = flask.Blueprint("unauthenticated", __name__)

unauthenticated.register_blueprint(nationalities_out, url_prefix="/nationalities")
unauthenticated.register_blueprint(users_out, url_prefix="/users")
unauthenticated.register_blueprint(inner_out, url_prefix="/inner")
