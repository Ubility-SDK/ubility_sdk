import requests
import json

APIversion = "2023-10"
url = "https://api.monday.com/v2"


def monday_create_board(cred,params):
    """
    Create a new board on Monday.com.

    :param str apiToken: The API key for authentication.
    :param dict params: Dictionary containing parameters.

        - :board_name: (str,required) - The name of the board to be created.
        - :board_kind: (str,required) - The kind of board to be created (share, private, public).

    Returns:
        dict: A dictionary containing the response from the Monday.com API.

    """
    try:
        creds=json.loads(cred)
        if "board_name" in params and "board_kind" in params and "apiToken" in creds:
            apiToken = creds["apiToken"]
            board_name = params["board_name"]
            board_kind = params["board_kind"]
            headers = {
                "Content-Type": "application/json",
                "Authorization": apiToken,
                "API-Version": APIversion
            }
            data = {
                "query": f"mutation {{ create_board (board_name: \"{board_name}\", board_kind: {board_kind}) {{ id }} }}"
            }
            response = requests.post(url=url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result['data']['create_board']
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def monday_move_item_to_board(cred,params):
    """
    Move an item to a different board in Monday.com.

    :param str apiToken: The API key for authentication.
    :param dict params: Dictionary containing parameters.

        - :board_id: (str,required) - The ID of the target board.
        - :group_id: (str,required) - The ID of the target group on the board.
        - :item_id: (int,required) - The ID of the item to be moved.

    Returns:
        dict: A dictionary containing the response data structure.

    """
    try:
        creds=json.loads(cred)
        if "board_id" in params and "group_id" in params and "item_id" in params and "apiToken" in creds:
            apiToken = creds["apiToken"]
            board_id = params["board_id"]
            group_id = params["group_id"]
            item_id = params["item_id"]
            headers = {
                "Content-Type": "application/json",
                "Authorization": apiToken,
                "API-Version": APIversion
            }
            data = {
                "query": f"mutation {{ move_item_to_board (board_id: {board_id}, group_id: \"{group_id}\", item_id: {item_id}) {{ id }} }}"
            }
            response = requests.post(url=url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result['data']['move_item_to_board']
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def monday_get_many_board(cred):
    """
    Get boards on Monday.com.

    :param str apiToken: The API key for authentication.

    Returns:
        list: A list containing dictionaries with details of the retrieved boards.

    """
    try:
        creds=json.loads(cred)
        if "apiToken" in creds:
            apiToken = creds["apiToken"]
            headers = {
                "Authorization": apiToken,
                "API-Version": APIversion
            }
            query = 'query { boards {id name description state board_folder_id board_kind owners{id} groups{id} items_count } }'
            data = {'query': query}
            response = requests.post(url=url, json=data, headers=headers)
            if response.status_code == 200:
                result = response.json()
                return result['data']['boards']
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def monday_archive_board(cred,params):
    """
    Archives a Monday.com board.

    :param str apiToken: The API key for authentication.
    :param dict params: Dictionary containing parameters.

        - :board_id: (str,required) - ID of the board to archive.

    Returns:
        dict: A dictionary containing the response from the Monday.com API.
    """
    try:
        creds=json.loads(cred)
        if "board_id" in params and "apiToken" in creds:
            apiToken = creds["apiToken"]
            board_id = params["board_id"]
            headers = {
                "Content-Type": "application/json",
                "Authorization": apiToken,
                "API-Version": APIversion
            }
            data = {
                "query": f"mutation {{ archive_board (board_id: {board_id}) {{ id name state }} }}"
            }
            response = requests.post(url=url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result['data']['archive_board']
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def monday_get_board(cred,params):
    """
    Get board information from the Monday.com API.

    :param str apiToken: The API key for authentication.
    :param dict params: Dictionary containing parameters.

        - :board_id: (str,required) - The board's unique identifier.

    Returns:
        dict: A dictionary containing information about the board retrieved from the API.
    """
    try:
        creds=json.loads(cred)
        if "board_id" in params and "apiToken" in creds:
            apiToken = creds["apiToken"]
            board_id = params["board_id"]
            headers = {
                "Authorization": apiToken,
                "API-Version": APIversion
            }
            query = f"{{ boards (ids : {board_id} ) {{ id  name  description state board_folder_id board_kind items_count }} }}"
            data = {'query': query}
            response = requests.post(url=url, json=data, headers=headers)
            if response.status_code == 200:
                result = response.json()
                return result['data']['boards'][0]
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def monday_create_item(cred,params):
    """
    Create a new item on Monday.com.

    :param str apiToken: The API key for authentication.
    :param dict params: Dictionary containing parameters.

        - :board_id: (str,required) - The board's unique identifier.
        - :group_id: (str,required) - The group's unique identifier.
        - :item_name: (str,required) - The new item's name.

    Returns:
        dict: A dictionary containing the response from the Monday.com API.

    """
    try:
        creds=json.loads(cred)
        if "board_id" in params and "group_id" in params and "item_name" in params and "apiToken" in creds:
            apiToken = creds["apiToken"]
            board_id = params["board_id"]
            group_id = params["group_id"]
            item_name = params["item_name"]
            headers = {
                "Content-Type": "application/json",
                "Authorization": apiToken,
                "API-Version": APIversion
            }
            data = {
                "query": f"mutation {{ create_item (board_id: {board_id}, group_id: \"{group_id}\", item_name: \"{item_name}\" ) {{ id }} }}"
            }
            response = requests.post(url=url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result['data']['create_item']
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def monday_get_item(cred,params):
    """
    Retrieve information about an item from Monday.com.

    :param str apiToken: The API key for authentication.
    :param dict params: Dictionary containing parameters.

        - :item_id: (str,required) - The ID of the item to retrieve.

    Returns:
        dict: A dictionary containing information about the item.
    """
    try:
        creds=json.loads(cred)
        if "item_id" in params and "apiToken" in creds:
            apiToken = creds["apiToken"]
            item_id = params["item_id"]
            headers = {
                "Content-Type": "application/json",
                "Authorization": apiToken,
                "API-Version": APIversion
            }
            data = {
                "query": f"{{items  (ids: {item_id} ) {{ id, name, created_at , state , column_values {{ id, text, type ,value, column {{ title ,archived ,description,settings_str}} }} }} }}"
            }
            response = requests.post(url=url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result['data']['items'][0]
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def monday_get_many_item(cred,params):
    """
    Retrieve multiple items from Monday.com for a specified board.

    :param str apiToken: The API key for authentication.
    :param dict params: Dictionary containing parameters.

        - :board_id: (str,required) - The ID of the board from which to retrieve items.

    Returns:
        dict: A dictionary containing the response from the Monday.com API.
    """
    try:
        creds=json.loads(cred)
        if "board_id" in params and "apiToken" in creds:
            apiToken = creds["apiToken"]
            board_id = params["board_id"]
            headers = {
                "Content-Type": "application/json",
                "Authorization": apiToken,
                "API-Version": APIversion
            }
            data = {
                "query": f"query {{ boards (ids: {board_id}) {{ items_page  {{ items {{ id name created_at state column_values {{ id, text, type ,value, column {{ title ,archived ,description,settings_str}} }} }} }}}}}}"
            }
            response = requests.post(url=url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result['data']['boards'][0]['items_page']['items']
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def monday_create_column(cred,params):
    """
    Create a new column on Monday.com.

    :param str apiToken: The API key for authentication.
    :param dict params: Dictionary containing parameters.

        - :board_id: (str, required): The unique identifier of the board where the column will be created.
        - :title: (str, required): The title or name of the new column.
        - :column_type: (str, required): The type of the column to be created. It can be one of the following:

            - :checkbox: A column for checkboxes.
            - :board_relation: A column to relate items between boards.
            - :country: A column for selecting countries.
            - :date: A column for dates.
            - :dependency: A column for dependencies.
            - :dropdown: A column for selecting options from a dropdown menu.
            - :email: A column for email addresses.
            - :file: A column for attaching files.
            - :hour: A column for hours.
            - :link: A column for linking URLs.
            - :location: A column for geographical locations.
            - :long_text: A column for longer text entries.
            - :name: A column for names.
            - :numbers: A column for numeric values.
            - :people: A column for selecting people.
            - :phone: A column for phone numbers.
            - :rating: A column for rating items.
            - :status: A column for status updates.
            - :tags: A column for tagging items.
            - :text: A column for short text entries.
            - :timeline: A column for creating timelines.
            - :week: A column for weeks.
            - :world_clock: A column for world clock times.

    Returns:
        dict: A dictionary containing the response from the Monday.com API.

    """
    try:
        creds=json.loads(cred)
        if "board_id" in params and "title" in params and "column_type" in params and "apiToken" in creds:
            apiToken = creds["apiToken"]
            board_id = params["board_id"]
            title = params["title"]
            column_type = params["column_type"]
            headers = {
                "Content-Type": "application/json",
                "Authorization": apiToken,
                "API-Version": APIversion
            }
            data = {
                "query": f"mutation {{ create_column (board_id: {board_id}, title:\"{title}\", column_type:{column_type}) {{ id  title }} }}"
            }
            response = requests.post(url=url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result['data']['create_column']
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def monday_get_many_column(cred,params):
    """
    Get columns from Monday.com for the specified board.

    :param str apiToken: The API key for authentication.
    :param dict params: Dictionary containing parameters.

        - :board_id: (str,required): The ID of the board for which columns are to be retrieved.

    Returns:
        dict: A dictionary containing the details of the retrieved columns.

    """
    try:
        creds=json.loads(cred)
        if "board_id" in params and "apiToken" in creds:
            apiToken = creds["apiToken"]
            board_id = params["board_id"]
            headers = {
                "Authorization": apiToken,
                "API-Version": APIversion
            }
            query = f"query {{ boards (ids: {board_id}) {{ columns {{ id title type settings_str archived}} }} }} "
            data = {'query': query}
            response = requests.post(url=url, json=data, headers=headers)
            if response.status_code == 200:
                result = response.json()
                return result['data']['boards'][0]
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def monday_get_many_group(cred,params):
    """
    Get groups from Monday.com for the specified board.

    :param str apiToken: The API key for authentication.
    :param dict params: Dictionary containing parameters.

        - :board_id: (str,required): The ID of the board for which groups are to be retrieved.

    Returns:
        dict: A dictionary containing the details of the retrieved groups.

    """
    try:
        creds=json.loads(cred)
        if "board_id" in params and "apiToken" in creds:
            apiToken = creds["apiToken"]
            board_id = params['board_id']
            headers = {
                "Authorization": apiToken,
                "API-Version": APIversion
            }
            query = f'query {{ boards (ids: {board_id}) {{ groups {{ id title color archived }}  }} }}'
            data = {'query': query}
            response = requests.post(url=url, json=data, headers=headers)
            if response.status_code == 200:
                result = response.json()
                return result['data']['boards'][0]
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def monday_create_group(cred,params):
    """
    Create a new group on Monday.com.

    :param str apiToken: The API key for authentication.
    :param dict params: Dictionary containing parameters.

        - :board_id: (str,required) - The board's unique identifier.
        - :group_name: (str,required) - The name of the group to be created.

    Returns:
        dict: A dictionary containing the response from the Monday.com API.

    """
    try:
        creds=json.loads(cred)
        if "board_id" in params and "group_name" in params and "apiToken" in creds:
            apiToken = creds["apiToken"]
            board_id = params["board_id"]
            group_name = params["group_name"]
            headers = {
                "Content-Type": "application/json",
                "Authorization": apiToken,
                "API-Version": APIversion
            }
            data = {
                "query": f"mutation {{ create_group (board_id: {board_id}, group_name: \"{group_name}\") {{ id title}} }}"
            }
            response = requests.post(url=url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result['data']['create_group']
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def monday_delete_group(cred,params):
    """
    Delete a group on Monday.com.

    :param str apiToken: The API key for authentication.
    :param dict params: Dictionary containing parameters.

        - :board_id: (str,required) - The board's unique identifier.
        - :group_id: (str,required) - The group's unique identifier.

    Returns:
        dict: A dictionary containing the response from the Monday.com API.

    """
    try:
        creds=json.loads(cred)
        if "board_id" in params and "group_id" in params and "apiToken" in creds:
            apiToken = creds["apiToken"]
            board_id = params["board_id"]
            group_id = params["group_id"]
            headers = {
                "Content-Type": "application/json",
                "Authorization": apiToken,
                "API-Version": APIversion
            }
            data = {
                "query": f"mutation {{ delete_group (board_id: {board_id}, group_id: \"{group_id}\") {{ id deleted}} }}"
            }
            response = requests.post(url=url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result['data']['delete_group']
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def monday_archive_group(cred,params):
    """
    Archives a Monday.com group.

    :param str apiToken: The API key for authentication.
    :param dict params: Dictionary containing parameters.

        - :board_id: (str,required) - The board's unique identifier.
        - :group_id: (str,required) - The group's unique identifier.

    Returns:
        dict: A dictionary containing the response from the Monday.com API.
    """
    try:
        creds=json.loads(cred)
        if "board_id" in params and "group_id" in params and "apiToken" in creds:
            apiToken = creds["apiToken"]
            board_id = params["board_id"]
            group_id = params["group_id"]
            headers = {
                "Content-Type": "application/json",
                "Authorization": apiToken,
                "API-Version": APIversion
            }
            data = {
                "query": f"mutation {{ archive_group (board_id: {board_id}, group_id: \"{group_id}\") {{ id archived }} }}"
            }
            response = requests.post(url=url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result['data']['archive_group']
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def monday_duplicate_group(cred,params):
    """
    Duplicate a group in Monday.com.

    :param str apiToken: The API key for authentication.
    :param dict params: Dictionary containing parameters.

        - :board_id: (str,required) - The board's unique identifier.
        - :group_id: (str,required) - The group's unique identifier.
        - :group_title: (str,required) - The title of the duplicated group.

    Returns:
        dict: A dictionary containing the response from the Monday.com API.
    """
    try:
        creds=json.loads(cred)
        if "board_id" in params and "group_id" in params and "group_title" in params and "apiToken" in creds:
            apiToken = creds["apiToken"]
            board_id = params["board_id"]
            group_id = params["group_id"]
            group_title = params["group_title"]
            headers = {
                "Content-Type": "application/json",
                "Authorization": apiToken,
                "API-Version": APIversion
            }
            data = {
                "query": f"mutation {{ duplicate_group (board_id: {board_id}, group_id: \"{group_id}\", group_title: \"{group_title}\") {{ id  }} }}"
            }
            response = requests.post(url=url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result['data']['duplicate_group']
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def monday_delete_item(cred,params):
    """
    Delete a item on Monday.com.

    :param str apiToken: The API key for authentication.
    :param dict params: Dictionary containing parameters.

        - :item_id: (str,required) - The ID of the item.

    Returns:
        dict: A dictionary containing information about the item.
    """
    try:
        creds=json.loads(cred)
        if "item_id" in params and "apiToken" in creds:
            apiToken = creds["apiToken"]
            item_id = params["item_id"]
            headers = {
                "Content-Type": "application/json",
                "Authorization": apiToken,
                "API-Version": APIversion
            }
            data = {
                "query": f"mutation {{ delete_item (item_id: {item_id}) {{ id }} }}"
            }
            response = requests.post(url=url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result['data']['delete_item']
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def monday_archive_item(cred,params):
    """
    Archives a Monday.com item.

    :param str apiToken: The API key for authentication.
    :param dict params: Dictionary containing parameters.

       - :item_id: (str,required) - The ID of the item.

    Returns:
        dict: A dictionary containing the response from the Monday.com API.
    """
    try:
        creds=json.loads(cred)
        if "item_id" in params and "apiToken" in creds:
            apiToken = creds["apiToken"]
            item_id = params["item_id"]
            headers = {
                "Content-Type": "application/json",
                "Authorization": apiToken,
                "API-Version": APIversion
            }
            data = {
                "query": f"mutation {{ archive_item (item_id: {item_id}) {{ id  }} }}"
            }
            response = requests.post(url=url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result['data']['archive_item']
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def monday_get_item_by_column_value(cred,params):
    """
    Retrieve items from Monday.com based on a specific column value.

    :param str apiToken: The API key for authentication.
    :param dict params: Dictionary containing parameters.

        - :board_id: (str, required) - The unique identifier of the board where the items are located.
        - :column_id: (str, required) - The unique identifier of the column to search for the specified value.
        - :column_values: (str, required) - The value to search for within the specified column.
        - :limit: (int, optional) - The maximum number of items to retrieve.

    Returns:
        dict: A dictionary containing the response from the Monday.com API. 
    """
    try:
        creds=json.loads(cred)
        if "board_id" in params and "column_id" in params and "column_values" in params and "apiToken" in creds:
            apiToken = creds["apiToken"]
            board_id = params["board_id"]
            column_id = params["column_id"]
            column_values = params["column_values"]
            limit = params.get("limit", 50)
            headers = {
                "Content-Type": "application/json",
                "Authorization": apiToken,
                "API-Version": APIversion
            }
            data = {
                "query": f"{{ items_page_by_column_values (limit: {limit}, board_id: {board_id}, columns: [{{column_id: \"{column_id}\", column_values: [\"{column_values}\"]}}, ]) {{ items {{ id, name, created_at , state , board {{id}} ,column_values {{ id, text, type ,value, column {{ title ,archived ,description,settings_str }} }} }} }} }}"
            }
            response = requests.post(url=url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result['data']['items_page_by_column_values']["items"]
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def monday_change_column_value(cred,params):
    """
    Change the value of a column for a specific item in Monday.com.

    :param str apiToken: The API key for authentication.
    :param dict params: Dictionary containing parameters.

       - :board_id: (str,required) - The ID of the board.
       - :item_id: (str,required) - The ID of the item for which the column value needs to be changed.
       - :column_id: (str,required) - The ID of the column for which the value needs to be changed.
       - :value: (str,required) - The new value for the specified column.

            e.g if column_id is status, value should be "{\"label\": \"Done\"}" 
                if column_id is date, value should be "{\"date\":\"2024-02-24\"}"
                if column_id is email, value should be "{\"text\":\"example email\",\"email\":\"example1@example.com\"}"
                if column_id is name or if type text , value should be "\"Sample text\""

    Returns:
        dict: A dictionary containing the response from the Monday.com API.
    """
    try:
        creds=json.loads(cred)
        if "board_id" in params and "item_id" in params and "column_id" in params and "value" in params and "apiToken" in creds:
            apiToken = creds["apiToken"]
            board_id = params["board_id"]
            item_id = params["item_id"]
            column_id = params["column_id"]
            if params["value"].startswith("{") or params["value"].startswith("\""):
                value = json.dumps(params["value"])
                headers = {
                    "Authorization": apiToken,
                    "Content-Type": "application/json",
                    "API-Version": APIversion
                }
                query = f"mutation {{ change_column_value (board_id: {board_id}, item_id: {item_id}, column_id: \"{column_id}\", value: {value}) {{ id name column_values {{ id, text, type ,value }}  }} }}"
                data = {"query": query}
                response = requests.post(url=url, json=data, headers=headers)
                if response.status_code == 200:
                    result = response.json()
                    return result['data']['change_column_value']
                else:
                    raise Exception(response.json())
            else:
                raise Exception("Custom Values must be a valid JSON")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def monday_create_subitem(cred,params):
    """
    Create a subitem for a item in Monday.com.

    :param str apiToken: The API key for authentication.
    :param dict params: Dictionary containing parameters.

        - :item_id: (str,required) - The unique identifier of the parent item.
        - :item_name: (str,required) - The name of the subitem to be created.

    Returns:
        dict: A dictionary containing the information about the created subitem.

    """
    try:
        creds=json.loads(cred)
        if "item_id" in params and "item_name" in params and "apiToken" in creds:
            apiToken = creds["apiToken"]
            item_id = params["item_id"]
            item_name = params["item_name"]
            headers = {
                "Content-Type": "application/json",
                "Authorization": apiToken,
                "API-Version": APIversion
            }
            data = {
                "query": f"mutation{{ create_subitem (parent_item_id: {item_id}, item_name: \"{item_name}\"){{ id }} }}"
            }
            response = requests.post(url=url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result['data']['create_subitem']
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def monday_get_many_subitem(cred,params):
    """
    Retrieve multiple subitems for a item in Monday.com.

    :param str apiToken: The API key for authentication.
    :param dict params: Dictionary containing parameters.

        - :item_id: (str,required): The unique identifier of the parent item.

    Returns:
        dict: A dictionary containing information about the retrieved subitems.

    """
    try:
        creds=json.loads(cred)
        if "item_id" in params and "apiToken" in creds:
            apiToken = creds["apiToken"]
            item_id = params['item_id']
            headers = {
                "Authorization": apiToken,
                "API-Version": APIversion
            }
            query = f"query {{items (ids: {item_id}) {{ subitems  {{ id name created_at state column_values {{ id, text, type ,value, column {{ title ,archived ,description,settings_str}} }} }} }} }} "
            data = {'query': query}
            response = requests.post(url=url, json=data, headers=headers)
            if response.status_code == 200:
                result = response.json()
                return result['data']['items'][0]
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def monday_add_update(cred,params):
    """
    Add an update to a specific item in Monday.com.

    :param str apiToken: The API key for authentication.
    :param dict params: Dictionary containing parameters.

        - :item_id: (str, required) - The unique identifier of the item to which the update will be added.
        - :body_text: (str, required) - The text content of the update.

    Returns:
        dict: A dictionary containing the response from the Monday.com API. 
    """
    try:
        creds=json.loads(cred)
        if "item_id" in params and "body_text" in params and "apiToken" in creds:
            apiToken = creds["apiToken"]
            item_id = params["item_id"]
            body_text = params["body_text"]
            headers = {
                "Content-Type": "application/json",
                "Authorization": apiToken,
                "API-Version": APIversion
            }
            data = {
                "query": f"mutation {{create_update (item_id: {item_id}, body: \"{body_text}\") {{id}} }}"
            }
            response = requests.post(url=url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result['data']['create_update']
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def monday_update_item_name(cred,params):
    """
    Update the name of an item in a Monday.com board.

    :param str apiToken: The API key for authentication.
    :param dict params: Dictionary containing parameters.

        - :board_id (str, required) - The unique identifier of the board containing the item.
        - :item_id (str, required) - The unique identifier of the item whose name will be updated.
        - :item_name (str, required) - The new name to set for the item.

    Returns:
        dict: A dictionary containing the response from the Monday.com API. 
    """
    try:
        creds=json.loads(cred)
        if "item_id" in params and "board_id" in params and "item_name" in params and "apiToken" in creds:
            apiToken = creds["apiToken"]
            item_id = params["item_id"]
            board_id = params["board_id"]
            item_name = params["item_name"]
            headers = {
                "Content-Type": "application/json",
                "Authorization": apiToken,
                "API-Version": APIversion
            }
            data = {
                "query": f"mutation {{change_multiple_column_values(item_id:{item_id}, board_id:{board_id}, column_values: \"{{\\\"name\\\" : \\\"{item_name}\\\"}}\") {{id}} }}"
            }
            response = requests.post(url=url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result['data']['change_multiple_column_values']
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def monday_change_multiple_column_values(cred,params):
    """
    Change multiple column values for an item on Monday.com.

    :param str apiToken: The API key for authentication.
    :param dict params: Dictionary containing parameters.

        - :board_id: (str,required) - The ID of the board.
        - :item_id: (str,required) - The ID of the item.
        - :column_values: (str,required) - JSON string representing column values to be changed.

            e.g "{\"project_status\": {\"label\": \"Done\"},\"name\":\"my items\",\"email\":{\"email\":\"example1@example.com\",\"text\":\"This is an example email\"}}"

    Returns:
        dict: A dictionary containing the response from the Monday.com API.
    """
    try:
        creds=json.loads(cred)
        if "item_id" in params and "board_id" in params and "column_values" in params and "apiToken" in creds:
            apiToken = creds["apiToken"]
            item_id = params["item_id"]
            board_id = params["board_id"]
            if params["column_values"].startswith("{"):
                column_values = json.dumps(params["column_values"])
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": apiToken,
                    "API-Version": APIversion
                }
                data = {
                    "query": f"mutation {{change_multiple_column_values(item_id:{item_id}, board_id:{board_id}, column_values: {column_values}) {{ id name column_values {{ id, value }}  }} }}"
                }
                response = requests.post(url=url, headers=headers, json=data)
                if response.status_code == 200:
                    result = response.json()
                    return result['data']['change_multiple_column_values']
                else:
                    raise Exception(response.json())
            else:
                raise Exception("Custom Values must be a valid JSON")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def monday_get_many_user(cred):
    """
    Get users from Monday.com for the specified board.

    :param str apiToken: The API key for authentication.

    Returns:
        dict: A dictionary containing the details of the retrieved users.

    """
    try:
        creds=json.loads(cred)
        if  "apiToken" in creds:
            apiToken = creds["apiToken"]
            headers = {
                "Authorization": apiToken,
                "API-Version": APIversion
            }
            query = f'query {{ users {{ created_at email account {{ name id }} }} }}'
            data = {'query': query}
            response = requests.post(url=url, json=data, headers=headers)
            if response.status_code == 200:
                result = response.json()
                return result['data']
            else:
                raise Exception(response.json())
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)