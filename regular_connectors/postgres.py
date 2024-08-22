import psycopg2
from psycopg2 import OperationalError
import json, datetime, decimal

def create_connection(creds):
    try:
        con = psycopg2.connect(
            host=creds["host"],
            database=creds["database"],
            user=creds["username"],
            password=creds["password"],
            port=creds['port'],
            sslmode = creds.get("sslMode","disable")
        )
        return con
    except OperationalError  as error:
        raise Exception(f"Error while connecting to postgreSQL: {error}")
    
def fetch_data_as_dict(cursor):
    """
    Fetch data from the cursor and convert it to a list of dictionaries.
    
    :param cursor: psycopg2 cursor object.
    :return: List of dictionaries where each dictionary represents a row of data.
    :rtype: list
    """
    column_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    
    result = []
    for row in rows:
        row_dict = dict(zip(column_names, row))
        result.append(row_dict)
    
    return result


def format_data(record):
    """
    Format data in the record to ensure it is JSON serializable.
    
    :param record: Dictionary representing a row of data.
    :return: Dictionary with formatted fields.
    :rtype: dict
    """
    formatted_record = {}
    for key, value in record.items():
        if isinstance(value, datetime.datetime):
            formatted_record[key] = value.strftime("%Y-%m-%d %H:%M:%S %z")
        elif isinstance(value, datetime.date):
            formatted_record[key] = value.strftime("%Y-%m-%d")
        elif isinstance(value, decimal.Decimal):
            formatted_record[key] = float(value)  
        elif isinstance(value, bytes):
            formatted_record[key] = value.decode('utf-8')  
        elif isinstance(value, set):
            formatted_record[key] = list(value)  
        elif isinstance(value, (int, float, str, bool)) or value is None:
            formatted_record[key] = value  
        else:
            formatted_record[key] = str(value) 
            
    return formatted_record

def postgres_create_table(creds, params):
    """
    Create a table in a PostgreSQL database.

    :param creds: Dictionary containing PostgreSQL database credentials.
    :type creds: dict
    :param params: Dictionary containing parameters.
    
        - :table_name: (str, required) - The name of the table to be created.
        - :fields: (dict, required) - A dictionary specifying the table fields and their data types.

    :return: A message indicating successful table creation.
    :rtype: str
    :raises Exception: If there is an issue with the PostgreSQL database or missing input data.
    """
    cursor = None
    con = None
    try:
        credentials=json.loads(creds)
        con = create_connection(credentials)
        cursor = con.cursor()
        if (
            "table_name" in params
            and params["table_name"]
            and params["table_name"] != ""
            and "fields" in params
            and params["fields"]
            and params["fields"] != {}
        ):
            table_name = params["table_name"]
            fields = params["fields"]
            string_fields = ""
            for field in fields.keys():
                string_fields += f"{field} {fields[field]}, "
            string_fields = string_fields[:-2]
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({string_fields})"
            cursor.execute(query)
            con.commit()
            return "Table created successfully"
        else:
            raise Exception("Missing input data")
    except Exception as e:
        if con:
            con.rollback()
        raise Exception(e)
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()



def postgres_insert_row(creds, params):
    """
    Insert a row into a table in a PostgreSQL database.

    :param creds: Dictionary containing PostgreSQL database credentials.
    :type creds: dict
    :param params: Dictionary containing parameters.

        - :table_name: (str, required) - The name of the table where the row will be inserted.
        - :data: (dict, required) - A dictionary specifying the data for the new row.

    :return: A message indicating successful row insertion.
    :rtype: str
    :raises Exception: If there is an issue with the PostgreSQL database or missing input data.
    """
    cursor = None
    con = None
    try:
        credentials=json.loads(creds)
        con = create_connection(credentials)
        cursor = con.cursor()
        if (
            "table_name" in params
            and params["table_name"]
            and params["table_name"] != ""
            and "data" in params
            and params["data"]
            and params["data"] != {}
        ):
            table_name = params["table_name"]
            data = params["data"]
            string_fields = ""
            string_values = ""
            for field in data.keys():
                string_fields += f"{field}, "
                string_values += f"'{data[field]}', "
            string_fields = string_fields[:-2]
            string_values = string_values[:-2]
            query = (
                f"INSERT INTO {table_name} ({string_fields}) VALUES ({string_values})"
            )
            cursor.execute(query)
            con.commit()
            return "Row inserted successfully"
        else:
            if con:
                con.rollback()
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()



def postgres_update_row(creds, params):
    """
    Update rows in a table in a PostgreSQL database based on specified conditions.

    :param creds: Dictionary containing PostgreSQL database credentials.
    :type creds: dict
    :param params: Dictionary containing parameters.

        - :table_name: (str, required) - The name of the table to be updated.
        - :data: (dict, required) - A dictionary specifying the data to update in the rows.
        - :conditions: (dict, required) - A dictionary specifying the conditions for updating rows.

            - :type: (str, required) - The type of conditions ("AND", "OR", or "custom").
            - :conditions: (list or str, required) - Conditions for updating rows.

    :return: A message indicating successful row update.
    :rtype: str
    :raises Exception: If there is an issue with the PostgreSQL database or missing input data.
    """
    con = None
    cursor = None
    try:
        credentials=json.loads(creds)
        con = create_connection(credentials)
        cursor = con.cursor()
        if (
            "table_name" in params
            and params["table_name"]
            and params["table_name"] != ""
            and "data" in params
            and params["data"]
            and params["data"] != {}
            and "conditions" in params
            and params["conditions"]
            and params["conditions"] != {}
        ):
            table_name = params["table_name"]
            data = params["data"]
            conditions = params["conditions"]
            condition_type = conditions["type"]
            condition_string = "WHERE "
            if condition_type == "AND":
                for condition in conditions["conditions"]:
                    condition_string += f"{condition} AND "
                condition_string = condition_string[:-4]
            elif condition_type == "OR":
                for condition in conditions["conditions"]:
                    condition_string += f"{condition} OR "
                condition_string = condition_string[:-3]
            elif condition_type == "custom":
                condition_string += conditions["conditions"]
            else:
                raise Exception("Invalid condition type")
            string_fields = ""
            for field in data.keys():
                string_fields += f"{field} = '{data[field]}', "
            string_fields = string_fields[:-2]
            query = f"UPDATE {table_name} SET {string_fields} {condition_string}"
            cursor.execute(query)
            con.commit()
            return "Row updated successfully"
        else:
            raise Exception("Missing input data")
    except Exception as e:
        if con:
            con.rollback()
        raise Exception(e)
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()



def postgres_delete_row(creds, params):
    """
    Delete rows from a table in a PostgreSQL database based on specified conditions.

    :param creds: Dictionary containing PostgreSQL database credentials.
    :type creds: dict
    :param params: Dictionary containing parameters.

        - :table_name: (str, required) - The name of the table from which rows will be deleted.
        - :conditions: (dict, optional) - A dictionary specifying the conditions for deleting rows.

            - :type: (str, required) - The type of conditions ("AND", "OR", or "custom").
            - :conditions: (list or str, required) - Conditions for deleting rows.

    :return: A message indicating successful row deletion.
    :rtype: str
    :raises Exception: If there is an issue with the PostgreSQL database or missing input data.
    """
    cursor = None
    con = None
    try:
        credentials=json.loads(creds)
        con = create_connection(credentials)
        cursor = con.cursor()
        if (
            "table_name" in params
            and params["table_name"]
            and params["table_name"] != ""
        ):
            table_name = params["table_name"]
            conditions = None
            condition_string = ""
            if (
                "conditions" in params
                and params["conditions"]
                and params["conditions"] != {}
            ):
                conditions = params["conditions"]
                condition_type = conditions["type"]
                condition_string = "WHERE "
                if condition_type == "AND":
                    for condition in conditions["conditions"]:
                        condition_string += f"{condition} AND "
                    condition_string = condition_string[:-4]
                elif condition_type == "OR":
                    for condition in conditions["conditions"]:
                        condition_string += f"{condition} OR "
                    condition_string = condition_string[:-3]
                elif condition_type == "custom":
                    condition_string += conditions["conditions"]
                else:
                    raise Exception("Invalid condition type")

            query = f"DELETE FROM {table_name} {condition_string}"
            cursor.execute(query)
            con.commit()
            return "Row deleted successfully"
        else:
            raise Exception("Missing input data")
    except Exception as e:
        if con:
            con.rollback()
        raise Exception(e)
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()



def postgres_delete_table(creds, params):
    """
    Delete a PostgreSQL table based on specified conditions.

    :param creds: Dictionary containing PostgreSQL database credentials.
    :type creds: dict
    :param params: Dictionary containing parameters.

        - :table_name: (str, required) - The name of the table to be deleted.
        - :type: (str, required) - The type of deletion ("clear" or "drop").

    :return: A message indicating successful table deletion.
    :rtype: str
    :raises Exception: If there is an issue with the PostgreSQL database or missing input data.
    """
    cursor= None
    con = None
    try:
        credentials=json.loads(creds)
        con = create_connection(credentials)
        cursor = con.cursor()
        if (
            "table_name" in params
            and params["table_name"]
            and params["table_name"] != ""
            and "type" in params
            and params["type"]
            and params["type"] != ""
        ):
            table_name = params["table_name"]
            delete_type = params["type"]
            if delete_type == "clear":
                query = f"Delete from {table_name}"
            elif delete_type == "drop":
                query = f"DROP TABLE {table_name}"
            else:
                raise Exception("Invalid delete type")
            cursor.execute(query)
            con.commit()
            return f"Table {delete_type}ed successfully"
        else:
            raise Exception("Missing input data")
    except Exception as e:
        if con:
            con.rollback()
        raise Exception(e)
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()



def postgres_execute_custom_query(creds, params):
    """
    Execute a custom SQL query in a PostgreSQL database.

    :param creds: Dictionary containing PostgreSQL database credentials.
    :type creds: dict
    :param params: Dictionary containing parameters.

        - :query: (str, required) - The custom SQL query to be executed.

    :return: Result of the query execution or a message indicating success.
    :rtype: list or str
    :raises Exception: If there is an issue with the PostgreSQL database or missing input data.
    """
    cursor = None
    con = None
    try:
        credentials=json.loads(creds)
        con = create_connection(credentials)
        cursor = con.cursor()
        
        if "query" not in params or not params['query']:
            raise Exception("Missing or empty query")
        query = params["query"]
        cursor.execute(query)
        if query.strip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
            con.commit()
            return "Query executed successfully"
        else:
            result = fetch_data_as_dict(cursor)
            result = [format_data(record) for record in result]
            return result
        
    except Exception as e:
        raise Exception(e)
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()



def postgres_select_row(creds, params):
    """
    Select rows from a table in a PostgreSQL database based on specified conditions.

    :param creds: Dictionary containing PostgreSQL database credentials.
    :type creds: dict
    :param params: Dictionary containing parameters.

        - :table_name: (str, required) - The name of the table from which rows will be selected.
        - :count: (int, optional) - The number of rows to retrieve.
        - :conditions: (dict, optional) - A dictionary specifying the conditions for selecting rows.

            - :type: (str, required) - The type of conditions ("AND", "OR", or "custom").
            - :conditions: (list or str, required) - Conditions for selecting rows.

    :return: Selected rows from the specified table.
    :rtype: list
    :raises Exception: If there is an issue with the PostgreSQL database or missing input data.
    """
    cursor = None
    con = None
    try:
        credentials=json.loads(creds)
        con = create_connection(credentials)
        cursor = con.cursor()
        count = None
        if (
            "table_name" in params
            and params["table_name"]
            and params["table_name"] != ""
        ):
            if "count" in params and params["count"] and params["count"] != 0:
                count = params["count"]
            table_name = params["table_name"]
            # data = params["data"]
            conditions = None
            condition_string = ""
            if (
                "conditions" in params
                and params["conditions"]
                and params["conditions"] != {}
            ):
                conditions = params["conditions"]
                condition_type = conditions["type"]
                condition_string = "WHERE "
                if condition_type == "AND":
                    for condition in conditions["conditions"]:
                        condition_string += f"{condition} AND "
                    condition_string = condition_string[:-4]
                elif condition_type == "OR":
                    for condition in conditions["conditions"]:
                        condition_string += f"{condition} OR "
                    condition_string = condition_string[:-3]
                elif condition_type == "custom":
                    condition_string += conditions["conditions"]
                else:
                    raise Exception("Invalid condition type")

            query = f"SELECT * FROM {table_name} {condition_string}"
            if count:
                query += f" LIMIT {count}"
            cursor.execute(query)
            result = fetch_data_as_dict(cursor)
            result = [format_data(record) for record in result]
            return result
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()
