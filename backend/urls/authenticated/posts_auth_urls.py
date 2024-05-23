import flask
from packages import au, db_aux, ftp_aux, db_connector

from helpers import posts_helpers
from packages.db_connector import TableNames
from packages.log import logger

posts_auth = flask.Blueprint(f"{TableNames.POSTS}_auth", __name__)
# PROXY:


# noinspection SqlResolve
@posts_auth.get('/posts/')
def get_posts():

    query = f"""
        SELECT p.*, u.Nickname
        FROM {TableNames.POSTS} p
        LEFT JOIN {TableNames.USERS} u on u.UserId = p.UserId
        ORDER BY p.Date DESC;
    """

    result = db_aux.get_json_from_query(TableNames.POSTS, query, ("Nickname",))
    db_aux.get_relation_list(
        result,
        TableNames.POSTS,
        TableNames.POSTS_PHOTOS,
        "PhotoUrl",
        "PostId",
        "PostId",
        "Photos"
    )
    return result


@posts_auth.get('/posts/<uuid:post_id>/')
def get_post_by_id(post_id):

    query = db_aux.make_select(
        TableNames.POSTS,
        conditions={
            "PostId": post_id
        }
    )

    result = db_aux.get_json_from_query(TableNames.POSTS, query)
    return result


@posts_auth.get('/users/<uuid:user_id>/posts/')
def get_posts_by_user(user_id):
    query = db_aux.make_select(
        TableNames.POSTS,
        conditions={
            "UserId": user_id
        },
        order_newest=True
    )

    result = db_aux.get_json_from_query(TableNames.POSTS, query)
    return result


@posts_auth.route('/dorms/<uuid:dorm_id>/posts/')
def get_posts_by_dorm(dorm_id):
    query = db_aux.make_select(
        TableNames.POSTS,
        conditions={
            "DormId": dorm_id
        },
        order_newest=True
    )

    result = db_aux.get_json_from_query(TableNames.POSTS, query)
    return result


@posts_auth.delete('/posts/<uuid:post_id>/')
def delete_post_by_id(post_id):
    query = db_aux.make_delete_primary_key(TableNames.POSTS, post_id)
    photo_urls = posts_helpers.get_photos_by_post(post_id)
    if ftp_aux.delete_files(photo_urls):
        posts_helpers.delete_postphotos_by_post(post_id)
        return db_aux.get_json_from_query(TableNames.POSTS, query)
    else:
        return "FTP error has occurred", 500


@posts_auth.put('/posts/<uuid:post_id>/')
def put_post(post_id):
    body = au.get_request_body()
    if "Photos" in body.keys():
        old_photos = posts_helpers.get_photos_by_post(post_id)
        photos_to_remove = [file for file in old_photos if file not in body["Photos"]]
        if not ftp_aux.delete_files(photos_to_remove):
            return "Error while deleting files", 500

        queries = []
        for photo in photos_to_remove:
            key = photo.split(".")[0]
            queries.append(db_aux.make_delete_primary_key(TableNames.POSTS_PHOTOS, key))
        db_connector.Connector.chain_queries(queries)

    db_aux.put_from_json(
        TableNames.POSTS,
        body,
        {"PostId": post_id},
        ("Photos",)
    )
    return "Query OK", 200


@posts_auth.post('/posts/create/')
def create_post():
    data = au.get_request_body()

    data["DormId"] = flask.g.token["DormId"]
    data["UserId"] = flask.g.token["UserId"]
    data["ReactionCount"] = 0

    post_uuid = db_aux.insertify_list(
        TableNames.POSTS,
        data,
        do_insert=True,
        add_date="Date",
        first_column_uuid=True,
        return_uuid=True
    )[1][0]

    photo_data_source = []
    for photo in data["Photos"]:
        photo_data_source.append({
            "PostId": post_uuid,
            "PhotoUrl": photo
        })

    if len(photo_data_source) > 0:
        db_aux.insertify_list(
            TableNames.POSTS_PHOTOS,
            photo_data_source,
            do_insert=True,
            add_empty=True
        )

    return "Post created"
