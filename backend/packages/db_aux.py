import datetime
import uuid

import packages.db_connector as db_connector
from packages.db_connector import TableNames

from packages.log import logger


# noinspection PyTypeChecker
def querify_value(elem):
    try:
        _ = float(elem)
        return elem
    except (TypeError, ValueError):
        return f"'{elem}'"


def insertify_list(table, json_data: list[dict], **kwargs):
    ret_uuid = []
    skipped = kwargs["skip"] if "skip" in kwargs else []
    if type(json_data) == dict or type(json_data[0]) != list and type(json_data[0]) != dict:
        json_data = [json_data]
    query = f"INSERT INTO {table}{kwargs['additional'] if 'additional' in kwargs.keys() else ''}\nVALUES\n"
    if "skip_table" in kwargs and kwargs["skip_table"]:
        columns = []
    else:
        columns = get_columns(table)
    if "cols" in kwargs:
        columns += kwargs["cols"]
    key: str = get_primary_key(table)
    for obj in json_data:
        if obj in skipped:
            continue
        temp = []
        if "add_date" in kwargs.keys():
            obj[kwargs["add_date"]] = datetime.datetime.now()
        if "add_empty" in kwargs.keys() and kwargs["add_empty"]:
            obj[key] = 0
        elif 'first_column' in kwargs.keys():
            obj[key] = kwargs['first_column']
        elif 'first_column_uuid' in kwargs.keys() and kwargs['first_column_uuid']:
            generated = uuid.uuid4()
            obj[key] = generated
            ret_uuid.append(generated)
        if 'skip_key' in kwargs.keys() and kwargs['skip_key']:
            columns = columns[1:]
        for col in columns:
            elem = obj[col]
            temp.append(querify_value(elem))
        temp = list(map(str, temp))
        split = ",".join(temp)
        query += f"({split}),\n"
    query = query[:-2] + ";"
    if "do_insert" in kwargs.keys() and kwargs["do_insert"]:
        if db_connector.Connector.chain_queries(query) == "INTEGRITY_ERROR":
            return "INTEGRITY_ERROR"
    return (query, ret_uuid) if "return_uuid" in kwargs and kwargs["return_uuid"] else query


def get_columns(table):
    ret = db_connector.Connector.chain_queries(f"SHOW COLUMNS FROM {table};")
    cols = tuple(row[0] for row in ret)
    return cols


def get_json_from_query(table, query, additional_cols=()):
    res = db_connector.Connector.chain_queries(query)
    cols = get_columns(table) if table is not None else []
    cols += additional_cols
    result_dicts = []
    for record in res:
        record_dict = {}
        for col, value in zip(cols, record):
            record_dict[col] = value
        result_dicts.append(record_dict)
    return result_dicts


def get_primary_key(table):
    ret = db_connector.Connector.chain_queries(f"""
        SHOW COLUMNS 
        FROM {table} 
        WHERE `Key`='PRI';
    """)
    return ret[0][0]


def make_select(table, **kwargs):
    conditions_sql = ""
    order_sql = ""
    if "order_newest" in kwargs.keys() and kwargs["order_newest"]:
        order_sql += "ORDER BY Date DESC"
    elif "order_by" in kwargs.keys():
        order_sql += f"ORDER BY {kwargs['order_by']}"
    if "conditions" in kwargs.keys():
        conditions_list = []
        conditions_sql = "WHERE"
        for condition in kwargs["conditions"].items():
            conditions_list.append(f" {condition[0]}={querify_value(condition[1])}")
        conditions_sql += " AND".join(conditions_list)
    return f"""
        Select * 
        FROM {table}
        {conditions_sql}
        {order_sql};
        """


def get_relation_list(json_list, table_one, table_many, field, join_field_table_one, join_field_table_many, key):
    for elem in json_list:
        query = f"""
            SELECT tmany.{field}
            FROM {table_many} tmany
            JOIN {table_one} tone on tmany.{join_field_table_many}=tone.{join_field_table_one}
            WHERE tone.{get_primary_key(table_one)}='{elem[get_primary_key(table_one)]}';
        """
        elem[key] = [el[0] for el in db_connector.Connector.chain_queries(query)]


def put_from_json(table, data, conditions, skip=()):
    changes = ""
    conditions_list = []
    conditions_sql = ""
    for key in skip:
        if key in data.keys():
            del data[key]
    for condition in conditions.items():
        conditions_list.append(f" {condition[0]}={querify_value(condition[1])}")
    conditions_sql += " AND".join(conditions_list)
    if len(data) > 0:
        changes += ', '.join([f"{key} = {querify_value(value)}" for key, value in data.items()])
        query = f"""
            UPDATE {table}
            SET {changes}
            WHERE {conditions_sql}
        """
        db_connector.Connector.chain_queries(query)
        return "Query ok", 200
    else:
        return "No changes made", 200


def make_delete_primary_key(table_name, primary_key_id):
    primary_key = get_primary_key(table_name)

    return f"""
        DELETE FROM {table_name}
        WHERE {primary_key}='{primary_key_id}'
    """


def truncate(table_name):
    return f"""
        TRUNCATE TABLE {table_name}
    """
