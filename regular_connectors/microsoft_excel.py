import requests
import json
status = [200, 201, 202, 204, 206, 207, 208]
    
def ref_token(creds):   
    try:
        cred=json.loads(creds)
        token_endpoint = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
        request_body = {
            'client_id': cred['clientId'],
            'client_secret': cred['clientSecret'],
            'scope': ' '.join(['https://graph.microsoft.com/.default'] +['offline_access']),
            'refresh_token': cred['refreshToken'],
            "grant_type": "refresh_token",
        }
        response = requests.post(token_endpoint, data=request_body)
        if response.status_code in status:
            return response.json()['access_token']
        else:
             raise Exception(f"Token request failed with status code {response.status_code}: {response.text}")
    except Exception as e:
        raise Exception(e)
    
#################################################################################################

def excel_get_many_workbooks(accessToken):
    """
    Retrieve information about Excel workbooks using Microsoft Graph API.

    :param str accessToken: Microsoft Graph API access token. (required)


    :return: Information about the Excel workbooks obtained from the Microsoft Graph API.
    :rtype: dict
    """
    try:
        if accessToken:
            search_endpoint = "https://graph.microsoft.com/v1.0/me/drive/root/search(q='.xlsx')"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {accessToken}",
            }
            response = requests.get(search_endpoint, headers=headers)
            if response.status_code in status:
                search_results = response.json()
                return search_results
            else:
                raise Exception({response.text})
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)


def excel_get_many_worksheets(accessToken,params):
    """
    Retrieve information about worksheets in a specific Excel workbook using Microsoft Graph API.

    :param str accessToken: Microsoft Graph API access token. (required)
    :param dict params:
        - workbookId (str): ID of the Excel workbook. (required)


    :return: Information about the worksheets in the specified Excel workbook obtained from the Microsoft Graph API.
    :rtype: dict
    """
    try:
        if "workbookId" in params and accessToken:
            graph_endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{params['workbookId']}/workbook/worksheets"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {accessToken}",
            }
            response = requests.get(graph_endpoint, headers=headers)
            if response.status_code in status:
                workbooks = response.json()
                return workbooks
            else:
                raise Exception({response.text})
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)

   
def excel_add_worksheet_to_workbook(accessToken,params):
    """
    Add a new worksheet to a specific Excel workbook using Microsoft Graph API.

    :param str accessToken: Microsoft Graph API access token. (required)
    :param dict params:
        - workbookId (str): ID of the Excel workbook. (required)
        - name (str): Name of the new worksheet. (optional)


    :return: Information about the added worksheet obtained from the Microsoft Graph API.
    :rtype: dict
    """
    try:
        if accessToken and 'workbookId' in params:
            worksheet_endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{params['workbookId']}/workbook/worksheets"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {accessToken}",
            }
            data = {}
            if 'name' in params:
                data['name'] = params['name']
            response = requests.post(worksheet_endpoint, headers=headers, json=data)
            if response.status_code in status:
                worksheet_info = response.json()
                return worksheet_info
            else:
                raise Exception({response.text})
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)
    
def excel_delete_workbook(accessToken,params):
    """
    Delete a specific Excel workbook using Microsoft Graph API.

    :param str accessToken: Microsoft Graph API access token. (required)
    :param dict params:
        - workbookId (str): ID of the Excel workbook. (required)


    :return: Success message indicating that the workbook has been deleted.
    :rtype: str
    """
    try:
        if accessToken and 'workbookId' in params:
            workbook_endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{params['workbookId']}"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {accessToken}",
            }
            response = requests.delete(workbook_endpoint, headers=headers)
            if response.status_code in status:
                return 'Workbook deleted successfully.'
            else:
                raise Exception({response.text})
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)
  
def excel_delete_worksheet(accessToken,params):
    """
    Delete a specific worksheet from an Excel workbook using Microsoft Graph API.

    :param str accessToken: Microsoft Graph API access token. (required)
    :param dict params:
        - workbookId (str): ID of the Excel workbook. (required)
        - worksheetId (str): ID of the worksheet to be deleted. (required)


    :return: Success message indicating that the worksheet has been deleted.
    :rtype: str
    """
    try:
        if accessToken and 'workbookId' in params and 'worksheetId' in params:
            worksheet_endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{params['workbookId']}/workbook/worksheets/{params['worksheetId']}"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {accessToken}",
            }
            response = requests.delete(worksheet_endpoint, headers=headers)
            if response.status_code in status:
                return 'Worksheet deleted successfully.'
            else:
                raise Exception({response.text})
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)
  
def excel_clear_worksheet(accessToken,params):
    """
    Clear data from a specified range or the entire worksheet in an Excel workbook using Microsoft Graph API.

    :param str accessToken: Microsoft Graph API access token. (required)
    :param dict params:
        - workbookId (str): ID of the Excel workbook. (required)
        - worksheetId (str): ID of the worksheet to be cleared. (required)
        - applyTo (str): Specifies what to clear, e.g., Formats or Contents. (required)
        - range (str): Address of the range to be cleared. If not provided, the entire worksheet is cleared. (optional)


    :return: Success message indicating that the worksheet has been cleared.
    :rtype: str
    """
    try:
        if accessToken and 'workbookId' in params and 'worksheetId' in params:
            if "range" in params:
                range=params['range']
                worksheet_endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{params['workbookId']}/workbook/worksheets/{params['worksheetId']}/range(address='{range}')/clear"
            else:
                worksheet_endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{params['workbookId']}/workbook/worksheets/{params['worksheetId']}/range/clear"
            headers = {
                "Authorization": f"Bearer {accessToken}",
                "Content-Type": "application/json",
            }
            data = {}
            if 'applyTo' in params:
                data['applyTo'] = params['applyTo']
            response = requests.post(worksheet_endpoint, headers=headers, json=data)
            if response.status_code in status:
                return "Worksheet cleared successfully."
            else:
                raise Exception({response.text})
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)

     
def excel_get_all_rows_in_table(accessToken,params):
    """
    Retrieve all rows from a specified table in an Excel workbook using Microsoft Graph API.

    :param str accessToken: Microsoft Graph API access token. (required)
    :param dict params:
        - workbookId (str): ID of the Excel workbook. (required)
        - worksheetId (str): ID of the worksheet containing the table. (required)
        - tableID (str): ID of the table from which to retrieve rows. (required)
        - limit (str): Limit the number of rows to retrieve (optional).


    :return: JSON data containing information about the retrieved rows.
    :rtype: dict
    """
    try:
        if accessToken and 'workbookId' in params and 'worksheetId' in params and 'tableID' in params:
            rows_endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{params['workbookId']}/workbook/worksheets/{params['worksheetId']}/tables/{params['tableID']}/rows"
            if 'limit' in params:
                rows_endpoint += f"?$top={params['limit']}"
            headers = {
                "Authorization": f"Bearer {accessToken}",
                "Content-Type": "application/json",
            }
            response = requests.get(rows_endpoint, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception({response.text})
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)
     
def excel_get_all_columns_in_table(accessToken,params):
    """
    Retrieve all columns from a specified table in an Excel workbook using Microsoft Graph API.

    :param str accessToken: Microsoft Graph API access token. (required)
    :param dict params:
        - workbookId (str): ID of the Excel workbook. (required)
        - worksheetId (str): ID of the worksheet containing the table. (required)
        - tableID (str): ID of the table from which to retrieve columns. (required)
        - limit (str): Limit the number of columns to retrieve (optional).


    :return: JSON data containing information about the retrieved columns.
    :rtype: dict
    """
    try:
        if accessToken and 'workbookId' in params and 'worksheetId' in params and 'tableID' in params:
            columns_endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{params['workbookId']}/workbook/worksheets/{params['worksheetId']}/tables/{params['tableID']}/columns"
            if 'limit' in params:
                columns_endpoint += f"?$top={params['limit']}"
            headers = {
                "Authorization": f"Bearer {accessToken}",
                "Content-Type": "application/json",
            }
            response = requests.get(columns_endpoint, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception({response.text})
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)
   
def excel_add_table(accessToken,params):
    """
    Add a table to a specified range in an Excel worksheet using Microsoft Graph API.

    :param str accessToken: Microsoft Graph API access token. (required)
    :param dict params:
        - workbookId (str): ID of the Excel workbook. (required)
        - worksheetId (str): ID of the worksheet to which the table will be added. (required)
        - address (str): Address of the range to be converted into a table (e.g., 'D3:F4'). (required)
        - hasHeaders (bool): Indicates whether the table has header. (optional)


    :return: JSON data containing information about the added table.
    :rtype: dict
    """
    try:
        if accessToken and 'workbookId' in params and 'worksheetId' in params and 'address' in params:
            table_endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{params['workbookId']}/workbook/worksheets/{params['worksheetId']}/tables/add"
            headers = {
                "Authorization": f"Bearer {accessToken}",
                "Content-Type": "application/json",
            }
            data={}
            if 'hasHeaders' in params:
                data['hasHeaders'] = params['hasHeaders']
            if 'address' in params:
                data['address'] = params['address'] 
            response = requests.post(table_endpoint, headers=headers,json=data)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception({response.text})
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)
  
def excel_delete_table(accessToken,params):
    """
    Delete a table from a specified worksheet in an Excel workbook using Microsoft Graph API.

    :param str accessToken: Microsoft Graph API access token. (required)
    :param dict params:
        - workbookId (str): ID of the Excel workbook. (required)
        - worksheetId (str): ID of the worksheet containing the table. (required)
        - tableID (str): ID of the table to be deleted. (required)


    :return: Message indicating the success of the table deletion.
    :rtype: str
    """
    try:
        if accessToken and 'workbookId' in params and 'worksheetId' in params and 'tableID' in params:
            table_endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{params['workbookId']}/workbook/worksheets/{params['worksheetId']}/tables/{params['tableID']}"
            headers = {
                "Authorization": f"Bearer {accessToken}",
                "Content-Type": "application/json",
            }
            response = requests.delete(table_endpoint, headers=headers)
            if response.status_code in status:
                return "Table Deleted successfully."
            else:
                raise Exception({response.text})
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)
    
     
def excel_append_rows_table(accessToken,params):
    """
    Append rows to a specified table in an Excel worksheet using Microsoft Graph API.

    :param str accessToken: Microsoft Graph API access token. (required)
    :param dict params:
        - workbookId (str): ID of the Excel workbook. (required)
        - worksheetId (str): ID of the worksheet containing the table. (required)
        - tableID (str): ID of the table to which rows will be appended. (required)
        - type (str): Type of data to append ('raw' or 'columns'). (required)
        - columnsid (list): List of column IDs for the 'columns' type. (required for 'columns' type)
        - value (list): List of values corresponding to column for 'columns' type. (required for 'columns' type)
        - values (list): List of lists containing row values for 'raw' type. (required for 'raw' type)
        - index (int): Index at which to append the rows. (optional)


    :return: Information about the appended rows.
    :rtype: dict
    """
    try:
        if accessToken and 'workbookId' in params and 'worksheetId' in params and 'tableID' in params:
            table_endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{params['workbookId']}/workbook/worksheets/{params['worksheetId']}/tables/{params['tableID']}/rows"
            headers = {
                "Authorization": f"Bearer {accessToken}",
                "Content-Type": "application/json",
            }
            if params['type']=='columns':
                columns_endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{params['workbookId']}/workbook/worksheets/{params['worksheetId']}/tables/{params['tableID']}/columns"
                res = requests.get(columns_endpoint, headers=headers)
                if res.status_code in status:
                    columns_data = res.json()
                    column_count = len(columns_data['value'])
                    if 'value' in params:
                        new_values_list = [None] * column_count
                        for i in range(len(params['columnsid'])):
                            col_id = params['columnsid'][i]
                            value = params['value'][i]
                            index_to_update = int(col_id) - 1
                            new_values_list[index_to_update] = value
                        params['values'] = []
                        params['values'].append(new_values_list)
            data={}
            if 'index' in params:
                data['index'] = params['index']
            if 'values' in params:
                data['values'] = params['values'] 
            response = requests.post(table_endpoint, headers=headers,json=data)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception({response.text})
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)
    
def excel_convert_table_to_range(accessToken,params):
    """
    Convert a table in an Excel worksheet to a range using Microsoft Graph API.

    :param str accessToken: Microsoft Graph API access token. (required)
    :param dict params:
        - workbookId (str): ID of the Excel workbook. (required)
        - worksheetId (str): ID of the worksheet containing the table. (required)
        - tableID (str): ID of the table to be converted. (required)


    :return: Information about the converted table range.
    :rtype: dict
    """
    try:
        if accessToken and 'workbookId' in params and 'worksheetId' in params and 'tableID' in params:
            endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{params['workbookId']}/workbook/worksheets/{params['worksheetId']}/tables/{params['tableID']}/range"
            headers = {
                "Authorization": f"Bearer {accessToken}",
                "Content-Type": "application/json",
            }
            response = requests.get(endpoint, headers=headers)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(response.text)
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)
    
   
def excel_lookup_table(accessToken,params):
    """
    Lookup data in a table in an Excel worksheet using Microsoft Graph API.

    :param str accessToken: Microsoft Graph API access token. (required)
    :param dict params:
        - workbookId (str): ID of the Excel workbook. (required)
        - worksheetId (str): ID of the worksheet containing the table. (required)
        - tableID (str): ID of the table to perform the lookup. (required)
        - columnValue (str): Name of the column to search for. (required)
        - rowvalue (str): Value to search for in the specified column. (required)
        - returnAll (bool): Flag indicating whether to return all matching rows or only the first. (optional)


    :return: List of matching rows if returnAll is True, otherwise a single row or an error message.
    :rtype: dict
    """
    try:
        if accessToken and 'workbookId' in params and 'worksheetId' in params and 'tableID' in params and  'columnValue' in params and 'rowvalue' in params:
            headers = {
                "Authorization": f"Bearer {accessToken}",
                "Content-Type": "application/json",
            }
            columns_endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{params['workbookId']}/workbook/worksheets/{params['worksheetId']}/tables/{params['tableID']}/columns"
            res = requests.get(columns_endpoint, headers=headers)
            if res.status_code in status:
                columns_data = res.json()
                column_index = None
                for i, column in enumerate(columns_data['value']):
                    if column['name'] == params['columnValue']:
                        column_index = i
                        break
                if column_index is not None:
                    index = None
                    rows = []
                    for j, cell_value in enumerate(columns_data['value'][column_index]['values']):
                        if params['rowvalue'] in cell_value and j != 0:
                            index = j
                            table_endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{params['workbookId']}/workbook/worksheets/{params['worksheetId']}/tables/{params['tableID']}/rows/ItemAt(index={index-1})"
                            response = requests.get(table_endpoint, headers=headers)
                            if response.status_code in status:
                                rows.append(response.json())
                                if params['returnAll']==False:
                                    return rows
                            else:
                                raise Exception(response.text)
                    if index is None:
                        raise Exception("Row not found.")
                    if params['returnAll']==True:
                        return rows
                else:
                    raise Exception("Column not found.")
            else:
                raise  Exception(res.text)
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)

def excel_update_sheet_range(accessToken,params):
    """
    Update a range in an Excel worksheet using Microsoft Graph API.

    :param str accessToken: Microsoft Graph API access token. (required)
    :param dict params:
        - workbookId (str): ID of the Excel workbook. (required)
        - worksheetId (str): ID of the worksheet containing the range. (required)
        - range (str): Range to update (e.g., "A1:B1"). (required)
        - values (list): List of lists containing values to update in the specified range. (required)


    :return: Information about the updated range.
    :rtype: dict
    """
    try:
        if accessToken and 'workbookId' in params and 'worksheetId' in params and 'range' in params and 'values' in params:
            headers = {
                "Authorization": f"Bearer {accessToken}",
                "Content-Type": "application/json",
            }
            update_endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{params['workbookId']}/workbook/worksheets/{params['worksheetId']}/range(address='{params['range']}')"
            data = {
                "values": params['values']
            }
            response = requests.patch(update_endpoint, headers=headers, json=data)
            if response.status_code in status:
                return response.json()
            else:
                raise Exception(response.text)
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)
    
def excel_insert_range(accessToken,params):
    """
    Insert a range in an Excel worksheet using Microsoft Graph API.

    :param str accessToken: Microsoft Graph API access token. (required)
    :param dict params:
        - workbookId (str): ID of the Excel workbook. (required)
        - worksheetId (str): ID of the worksheet where the range will be inserted. (required)
        - range (str): Range to insert (e.g., "A1:B1"). (required)
        - shift (str): Direction to shift cells. Possible values: "down", "right". (required)
        - values (list): List of lists containing values to update in the specified range. (optional)


    :return: Information about the inserted range.
    :rtype: dict
    """
    try:
        if accessToken and 'workbookId' in params and 'worksheetId' in params and 'range' in params and 'shift' in params:
            headers = {
                "Authorization": f"Bearer {accessToken}",
                "Content-Type": "application/json",
            }
            insert_endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{params['workbookId']}/workbook/worksheets/{params['worksheetId']}/range(address='{params['range']}')/insert"
            data = {
                "shift": params['shift']
            }
            response = requests.post(insert_endpoint, headers=headers, json=data)
            if 'values' in params:
                update_endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{params['workbookId']}/workbook/worksheets/{params['worksheetId']}/range(address='{params['range']}')"
                data = {
                "values": params['values']
                }
                response2 = requests.patch(update_endpoint, headers=headers, json=data)
                if response2.status_code in status:
                    return response2.json()
                else:
                    raise Exception(response2.text)
            else:
                if response.status_code in status:
                    return response.json()
                else:
                    raise Exception(response.text)
        else:
            raise Exception('Missing parameters')
    except requests.exceptions.RequestException as e:
        raise Exception(e)
    except Exception as e:
        raise Exception(e)
