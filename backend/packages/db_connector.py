import pymysql
import packages.au as aux
from packages.log import logger


class Connector:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.get_connection()
        self.get_cursor()

    def get_connection(self):
        try:
            connection = pymysql.connect(
                host="db",
                port=3306,
                user=aux.get_environ("DB_USER"),
                password=aux.get_environ("DB_PASSWORD"),
                database=aux.get_environ("DB_NAME"),
            )
            logger.debug("Connected to the database")
            self.conn = connection
        except Exception as e:
            logger.error("Error connecting to the database:", e)

    def get_cursor(self):
        if self.conn is not None:
            # noinspection PyBroadException
            try:
                self.cursor = self.conn.cursor()
                logger.info("Created new database cursor")
            except Exception:
                logger.error(
                    "An error has occurred while creating database cursor")
        else:
            logger.error("Connection was null while creating cursor")

    def execute_query(self, q):
        out = None
        try:
            ret = self.cursor.execute(q)
            out = self.cursor.fetchall()
            logger.debug(f"Query: {q} executed correctly, output: {out}, ret: {ret}")
        except Exception as ex:
            logger.error(f"Error while trying to execute the query: {q}")
            raise ex
        return out

    def commit_conn(self):
        try:
            self.conn.commit()
            logger.debug("Connection to the database has been committed")
        except Exception as ex:
            logger.error(
                "An error has occurred while attempting to commit the connection")
            raise ex

    def close_conn(self):
        self.commit_conn()
        try:
            self.conn.close()
            self.cursor.close()
            logger.debug("Connection to the database has been closed")
        except Exception as ex:
            logger.error(
                "An error has occurred while attempting to close the connection to the database")
            raise ex

    def start_transaction(self):
        self.conn.begin()

    def rollback_transaction(self):
        self.conn.rollback()

    @staticmethod
    def chain_queries(queries):
        db = Connector()
        try:
            db.start_transaction()
            ret = []
            if type(queries) == list:
                for q in queries:
                    ret.append(db.execute_query(q))
            else:
                ret = db.execute_query(queries)
        except pymysql.IntegrityError:
            logger.error("An integrity error has occurred")
            return "INTEGRITY_ERROR"
        except pymysql.Error as e:
            logger.error("Error occurred during transaction:", e)
            db.rollback_transaction()
        finally:
            db.close_conn()
        return ret


class TableNames:
    COMMENTS = "comments"
    DORMS = "dorms"
    NATIONALITIES = "nationalities"
    COMMENT_REPORTS = "commentreports"
    POSTS_PHOTOS = "postsphotos"
    COMMENT_REACTIONS = "commentreactions"
    USERS = "users"
    POSTS = "posts"
    REACTIONS_TYPE = "reactionstype"
    POST_REACTIONS = "postreactions"
    POST_TYPES = "posttypes"
    POST_REPORTS = "postreports"
    SESSIONS = "sessions"
    TASKS_SCHEDULE = "taskschedule"
    TASK_ASSIGNEE = "taskassignee"
