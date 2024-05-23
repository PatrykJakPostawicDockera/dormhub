from packages import db_connector
from packages.db_connector import TableNames
from packages.log import logger


def get_photos_by_post(post_id):
    query = f"""
        SELECT PhotoUrl 
        FROM {TableNames.POSTS_PHOTOS}
        WHERE PostId='{post_id}';
    """
    return [elem[0] for elem in db_connector.Connector.chain_queries(query)]


def delete_postphotos_by_post(post_id):
    query = f"""
        DELETE FROM {TableNames.POSTS_PHOTOS}
        WHERE PostId='{post_id}';
    """
    db_connector.Connector.chain_queries(query)
    return True
