import flask
import base64

from packages import au, ftp_aux, scraper
from packages.log import logger

inner_out = flask.Blueprint(f"inner_out", __name__)
# PROXY: /inner


@inner_out.post("/photos/upload/")
def upload_photo():
    body = au.get_request_body()
    image_parts = body["PhotoData"].split(",")
    image_format = image_parts[0].split(";")[0].split(":")[1].split("/")[1]
    image_content = image_parts[1]
    image_data = base64.b64decode(image_content)
    image_url = ftp_aux.upload_to_ftp(image_data, image_format)
    return flask.jsonify({
        "PhotoUrl": image_url
    })
