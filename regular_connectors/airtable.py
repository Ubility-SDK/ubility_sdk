import json
from pyairtable import Api, retry_strategy


def create_api_instance(access_token):
    """
    Returns an instance of a connection to Airtable API using the provided Access Token
    
    :param str access_token: Used for authentication purposes.
    
    :return: instance of a connection to Airtable API
    :rtype: API object
    """
    try:
        api = Api(access_token, retry_strategy=retry_strategy(total=10))
        return api
    except Exception as e:
        raise Exception(
            f"failed to create api instance using the provided token with error: {e}"
        )


def create_table_instance(cred, base_id, table_id):
    """
    Returns an instance of the Table class which is used to perform operations on the specified table
    
    :param json cred: Used for authentication purposes.
    :param str base_id: Used to specify the base containing the table the user needs to interact with.
    :param str table_id: Used to specify the table the user needs to interact with.
    
    :return: instance of the Table class representing the selected table
    :rtype: Table object
    """
    try:
        creds=json.loads(cred)
        access_token = creds['accesstoken']
        if 'accesstoken' in creds and base_id and table_id:
            api = create_api_instance(access_token)
            table = api.table(base_id, table_id)
            return table
        else:
            raise Exception("Missing required input data")
    except Exception as e:
        raise Exception(
            f"failed to create table instance using the provided data with error: {e}"
        )


########################## here comes the code ####################################


########################## records ####################################


def airtable_list_records(cred, params):
    """
    Retrieve all matching records in a single list.
    
    :cred: JSON String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :base_id: (str,required) - Used to specify the base containing the table the user needs to interact with.
    - :table_id: (str,required) - Used to specify the table the user needs to interact with.
    - :view: (str,optional) - The name or ID of a view. If set, only the records in that view will be returned.
    - :page_size: (int,optional) - The number of records returned in each request. Must be less than or equal to 100. If no value given, Airtable's default is 100.
    - :max_records: (int,optional) - The maximum total number of records that will be returned.
    - :fields: (list of str,optional) - List containing the name or ID of field or fields to be retrieved. Default is all fields.
    - :sort: (list of str,optional) - List of fields to sort by. This parameter specifies how the records will be ordered. Sorting Direction is ascending by default, but can be reversed by prefixing the column name with a minus sign -.
    - :formula: (str,optional) - An Airtable formula. The formula will be evaluated for each record, and if the result is not false, the record will be included in the response.
    - :cell_format: (str,optional) - The cell format to request from the Airtable API (json, string).
    - :user_locale: (str,optional) - The user locale that should be used to format dates when using string as the cell_format. See `the documentation <https://support.airtable.com/hc/en-us/articles/220340268-Supported-locale-modifiers-for-SET-LOCALE>`_ for valid values.
    - :time_zone: (str,optional) - The time zone that should be used to format dates when using string as the cell_format. See `the documentation <https://support.airtable.com/hc/en-us/articles/216141558-Supported-timezones-for-SET-TIMEZONE>`_ for valid values .
    - :return_fields_by_field_id: (bool,optional) - An optional boolean value that lets you return field objects where the key is the field id. This defaults to false, which returns field objects where the key is the field name.

    :return: List of record dictionaries with each dictionary representing a record
    :rtype: List[RecordDict]
    """
    try:
        base_id = params.get("base_id", None)
        table_id = params.get("table_id", None)

        table = create_table_instance(cred, base_id, table_id)

        ignore_keys = ["base_id", "table_id"]
        data = {
            key: value
            for (key, value) in params.items()
            if value
            if key not in ignore_keys
        }

        response = table.all(**data)
        return response
    except Exception as e:
        raise Exception({e})


def airtable_create_record(cred, params):
    """
    Create a new record.
    
    :cred: JSON String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :base_id: (str,required) - Used to specify the base containing the table the user needs to interact with.
    - :table_id: (str,required) - Used to specify the table the user needs to interact with.
    - :fields: (dict,optional) - Fields to insert. Must be a dict with field names or IDs as keys. It can be an empty dictionary or contain one or more key-value pairs based on user input. Example usage:

        - An empty 'fields' dictionary:
            {}

        - 'fields' dictionary with key-value pairs:
            {'field1': 'value1', 'field2': 42}
    
    - :typecast: (bool,optional) - The Airtable API will perform best-effort automatic data conversion from string values. Defaults to false.
    - :return_fields_by_field_id: (bool,optional) - An optional boolean value that lets you return field objects where the key is the field id. This defaults to false, which returns field objects where the key is the field name.

    :return: RecordDict describing the created record
    :rtype: RecordDict
    """
    try:
        if "fields" in params:
            base_id = params.get("base_id", None)
            table_id = params.get("table_id", None)

            table = create_table_instance(cred, base_id, table_id)

            ignore_keys = ["base_id", "table_id"]
            data = {
                key: value
                for (key, value) in params.items()
                if value
                if key not in ignore_keys
            }

            response = table.create(**data)
            return response
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception({e})


def airtable_batch_create_records(cred, params):
    """
    Batch create new records.
    
    :cred: JSON String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :base_id: (str,required) - Used to specify the base containing the table the user needs to interact with.
    - :table_id: (str,required) - Used to specify the table the user needs to interact with.
    - :records: (list of dict,optional) - Iterable of dicts representing records to be created.
        Each dictionary can be empty or contain dynamic field-value pairs based on user input.
        Example usage:

        [
            {'field1': 'value1', 'field2': 42, ...},
            {'field1': 'value3', ...},
            {},
            ...
        ]
    
    - :typecast: (bool,optional) - The Airtable API will perform best-effort automatic data conversion from string values. Defaults to false.
    - :return_fields_by_field_id: (bool,optional) - An optional boolean value that lets you return field objects where the key is the field id. This defaults to false, which returns field objects where the key is the field name.

    :return: List of RecordDict with each one describing a created record
    :rtype: List[RecordDict]
    """
    try:
        if params.get("records", None):
            base_id = params.get("base_id", None)
            table_id = params.get("table_id", None)

            table = create_table_instance(cred, base_id, table_id)

            ignore_keys = ["base_id", "table_id"]
            data = {
                key: value
                for (key, value) in params.items()
                if value
                if key not in ignore_keys
            }

            response = table.batch_create(**data)
            return response
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception({e})


def airtable_update_record(cred, params):
    """
    Update a particular record ID with the given fields.
    
    :cred: JSON String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :base_id: (str,required) - Used to specify the base containing the table the user needs to interact with.
    - :table_id: (str,required) - Used to specify the table the user needs to interact with.
    - :record_id: (str,required) - An Airtable record id
    - :fields: (dict,optional) - Fields to update. Must be a dict with field names or IDs as keys. It can be an empty dictionary or contain one or more key-value pairs based on user input. Example usage:

        - An empty 'fields' dictionary:
            {}

        - 'fields' dictionary with key-value pairs:
            {'field1': 'value1', 'field2': 42, ...}
    
    - :replace: (bool,optional) - If True, record is replaced in its entirety by provided fields; if a field is not included its value will bet set to null. If False, only provided fields are updated.
    - :typecast: (bool,optional) - The Airtable API will perform best-effort automatic data conversion from string values. Defaults to false.
    - :return_fields_by_field_id: (bool,optional) - An optional boolean value that lets you return field objects where the key is the field id. This defaults to false, which returns field objects where the key is the field name.

    :return: RecordDict describing the created record
    :rtype: RecordDict
    """
    try:
        if "fields" in params and "record_id" in params:
            base_id = params.get("base_id", None)
            table_id = params.get("table_id", None)

            table = create_table_instance(cred, base_id, table_id)

            ignore_keys = ["base_id", "table_id"]
            data = {
                key: value
                for (key, value) in params.items()
                if value
                if key not in ignore_keys
            }

            response = table.update(**data)
            return response
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception({e})


def airtable_batch_update_records(cred, params):
    """
    Update several records in batches.
    
    :cred: JSON String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :base_id: (str,required) - Used to specify the base containing the table the user needs to interact with.
    - :table_id: (str,required) - Used to specify the table the user needs to interact with.
    - :records: (list of dict,optional) - Iterable of dicts representing records to be updated.
        Each dictionary must have:
            - :id: (str,required) - The ID of the record to be updated.
            - :fields: (dict,required) - A dictionary of fields to be updated for the record.

        Example usage:

        [
            {
                "id": "recAdw9EjV90xbW",
                "fields": {
                    "Email": "alice@example.com"
                }
            },
            {
                "id": "recAdw9EjV90xbX",
                "fields": {
                    "Email": "bob@example.com"
                }
            },
            {},
            ...
        ]
    
    - :replace: (bool,optional) - If True, record is replaced in its entirety by provided fields; if a field is not included its value will bet set to null. If False, only provided fields are updated.
    - :typecast: (bool,optional) - The Airtable API will perform best-effort automatic data conversion from string values. Defaults to false.
    - :return_fields_by_field_id: (bool,optional) - An optional boolean value that lets you return field objects where the key is the field id. This defaults to false, which returns field objects where the key is the field name.

    :return: List of RecordDict with each one describing an updated record
    :rtype: List[RecordDict]
    """
    try:
        cond = True
        if "records" in params:
            for record in params["records"]:
                if not ("id" in record and "fields" in record):
                    cond = False

        if cond:
            base_id = params.get("base_id", None)
            table_id = params.get("table_id", None)

            table = create_table_instance(cred, base_id, table_id)

            ignore_keys = ["base_id", "table_id"]
            data = {
                key: value
                for (key, value) in params.items()
                if value
                if key not in ignore_keys
            }

            response = table.batch_update(**data)
            return response
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception({e})


def airtable_batch_update_or_create_records(cred, params):
    """
    Update or create records in batches, either using id (if given) or using a set of fields (key_fields) to look for matches.
    
    :cred: JSON String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :base_id: (str,required) - Used to specify the base containing the table the user needs to interact with.
    - :table_id: (str,required) - Used to specify the table the user needs to interact with.
    - :records: (list of dict,optional) - Iterable of dicts representing records to be updated or created.
        Each dictionary must have:
            - :id: (str,optional) - The ID of the record to be updated.
            - :fields: (dict,optional) - A dictionary of fields to be updated for the record.

        Example usage:

        [
            {
                "id": "recAdw9EjV90xbW",
                "fields": {
                    "Email": "alice@example.com"
                }
            },
            {
                "id": "recAdw9EjV90xbX",
                "fields": {
                    "Email": "bob@example.com"
                }
            },
            {},
            ...
        ]
    
    - :key_fields: (list of str,optional) - List of field names that Airtable should use to match records in the input with existing records on the server.
    - :replace: (bool,optional) - If True, record is replaced in its entirety by provided fields; if a field is not included its value will bet set to null. If False, only provided fields are updated.
    - :typecast: (bool,optional) - The Airtable API will perform best-effort automatic data conversion from string values. Defaults to false.
    - :return_fields_by_field_id: (bool,optional) - An optional boolean value that lets you return field objects where the key is the field id. This defaults to false, which returns field objects where the key is the field name.

    :return: List of RecordDict with each one describing an updated or created record
    :rtype: List[RecordDict]
    """
    try:
        cond_field = True
        if "records" in params:
            for record in params["records"]:
                if "fields" not in record:
                    cond_field = False


        if cond_field and "key_fields" in params:
            base_id = params.get("base_id", None)
            table_id = params.get("table_id", None)

            table = create_table_instance(cred, base_id, table_id)

            ignore_keys = ["base_id", "table_id"]
            data = {
                key: value
                for (key, value) in params.items()
                if value
                if key not in ignore_keys
            }

            response = table.batch_upsert(**data)
            return response
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception({e})


def airtable_delete_record(cred, params):
    """
    Delete the given record.
    
    :cred: JSON String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :base_id: (str,required) - Used to specify the base containing the table the user needs to interact with.
    - :table_id: (str,required) - Used to specify the table the user needs to interact with.
    - :record_id: (str,required) - An Airtable record id
    
    :return: Confirmation that the record was deleted.
    :rtype: RecordDeletedDict
    """
    try:
        record_id = params.get("record_id", None)
        if record_id:
            base_id = params.get("base_id", None)
            table_id = params.get("table_id", None)

            table = create_table_instance(cred, base_id, table_id)

            data = {"record_id": record_id}

            response = table.delete(**data)
            return response
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception({e})


def airtable_batch_delete_records(cred, params):
    """
    Delete the given records, operating in batches.
    
    :cred: JSON String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :base_id: (str,required) - Used to specify the base containing the table the user needs to interact with.
    - :table_id: (str,required) - Used to specify the table the user needs to interact with.
    - :record_ids: (list of str,required) - Record IDs to delete
    
    :return: Confirmation that the records were deleted.
    :rtype: List[RecordDeletedDict]
    """
    try:
        record_ids = params.get("record_ids", [])
        if record_ids:
            base_id = params.get("base_id", None)
            table_id = params.get("table_id", None)

            table = create_table_instance(cred, base_id, table_id)

            data = {"record_ids": record_ids}

            response = table.batch_delete(**data)
            return response
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception({e})


def airtable_get_record(cred, params):
    """
    Retrieve a record by its ID.
    
    :cred: JSON String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :base_id: (str,required) - Used to specify the base containing the table the user needs to interact with.
    - :table_id: (str,required) - Used to specify the table the user needs to interact with.
    - :record_id: (str,required) - An Airtable record id
    - :cell_format: (str,optional) - The cell format to request from the Airtable API (json, string).
    - :user_locale: (str,optional) - The user locale that should be used to format dates when using string as the cell_format. See `the documentation <https://support.airtable.com/hc/en-us/articles/220340268-Supported-locale-modifiers-for-SET-LOCALE>`_ for valid values.
    - :time_zone: (str,optional) - The time zone that should be used to format dates when using string as the cell_format. See `the documentation <https://support.airtable.com/hc/en-us/articles/216141558-Supported-timezones-for-SET-TIMEZONE>`_ for valid values .
    - :return_fields_by_field_id: (bool,optional) - An optional boolean value that lets you return field objects where the key is the field id. This defaults to false, which returns field objects where the key is the field name.

    :return: RecordDict describing the created record
    :rtype: RecordDict
    """
    try:
        record_id = params.get("record_id", None)
        if record_id:
            base_id = params.get("base_id", None)
            table_id = params.get("table_id", None)

            table = create_table_instance(cred, base_id, table_id)

            ignore_keys = ["base_id", "table_id"]
            data = {
                key: value
                for (key, value) in params.items()
                if value
                if key not in ignore_keys
            }

            response = table.get(**data)
            return response
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception({e})