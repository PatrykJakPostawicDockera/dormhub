import flask

from packages import scraper, db_aux, db_connector, ftp_aux
from packages.log import logger
from helpers import dorms_helpers
from packages.db_connector import TableNames

inner_auth = flask.Blueprint(f"inner_auth", __name__)
# PROXY: /inner


@inner_auth.post("/update/dorms/")
def update_dorms():
    scrap = scraper.scrap_data()
    dorm_list = dorms_helpers.get_all_dorm_names()
    if len(scrap) > 0:
        for dorm in scrap:
            if dorm["Name"] in dorm_list:
                query = db_aux.put_from_json(
                    TableNames.DORMS,
                    dorm,
                    {
                        "Name": dorm["Name"]
                    }
                )
            else:
                dorm["DormCode"] = dorms_helpers.generate_dorm_code()
                query = db_aux.insertify_list(
                    TableNames.DORMS,
                    dorm,
                    first_column_uuid=True
                )
                db_connector.Connector.chain_queries(query)
        logger.info("Dorm table has been updated")
        return scrap, 200
    logger.error("Dorm server returned 0 rows")
    return "An error has occurred", 500


@inner_auth.delete("/photos/<path:file_url>/remove/")
def delete_photo(file_url):
    if ftp_aux.delete_files([file_url]):
        return f"Image: {file_url} has been deleted", 200
    else:
        return f"Image: {file_url} removal has been unsuccessful", 500
