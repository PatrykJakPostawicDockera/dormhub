import flask
from packages import db_aux, jwt_aux, au, db_connector

from packages.db_connector import TableNames
from packages.log import logger

comments_auth = flask.Blueprint(f"{TableNames.COMMENTS}_auth", __name__)
# PROXY:


@comments_auth.get('/comments/')
def get_posts():
    query = db_aux.make_select(
        TableNames.COMMENTS,
        order_newest=True
    )

    result = db_aux.get_json_from_query(TableNames.COMMENTS, query)
    return result


# noinspection SqlResolve
@comments_auth.get('/posts/<uuid:post_id>/comments/')
def get_comments_by_post(post_id):
    query = f"""
        SELECT c.*, u.Nickname
        FROM {TableNames.COMMENTS} c
        JOIN {TableNames.USERS} u on c.UserId = u.UserId
        WHERE c.PostId='{post_id}'
        ORDER BY c.Date DESC ;
    """

    result = db_aux.get_json_from_query(
        TableNames.COMMENTS,
        query,
        ("Nickname",)
    )

    return result


@comments_auth.get('/users/<uuid:user_id>/comments/')
def get_comments_by_user(user_id):
    query = db_aux.make_select(
        TableNames.COMMENTS,
        conditions={
            "UserId": user_id
        },
        order_newest=True
    )

    result = db_aux.get_json_from_query(TableNames.COMMENTS, query)
    return result


@comments_auth.delete('/comments/<uuid:comment_id>/')
def delete_comment_by_id(comment_id):
    query = db_aux.make_delete_primary_key(TableNames.COMMENTS, comment_id)
    db_connector.Connector.chain_queries(query)
    return "Query OK", 200


@comments_auth.put('/comments/<uuid:comment_id>/')
def put_comment(comment_id):
    body = au.get_request_body()
    db_aux.put_from_json(
        TableNames.COMMENTS,
        body,
        {"CommentId": comment_id}
    )
    return "Query OK", 200


@comments_auth.post('/posts/<uuid:post_id>/comments/create/')
def create_comment(post_id):
    data = au.get_request_body()

    data["UserId"] = flask.g.token["UserId"]
    data["PostId"] = post_id

    db_aux.insertify_list(
        TableNames.COMMENTS,
        data,
        do_insert=True,
        first_column_uuid=True,
        add_date="Date"
    )

    return "Query OK"
