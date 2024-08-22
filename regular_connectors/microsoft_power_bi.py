import requests
import json

def microsoft_power_bi_refresh_access_token(cred):
    try:
        creds = json.loads(cred)
        token_endpoint = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
        scopes = ['https://analysis.windows.net/powerbi/api/Dataset.ReadWrite.All', 'https://analysis.windows.net/powerbi/api/Report.ReadWrite.All', 'https://analysis.windows.net/powerbi/api/Workspace.ReadWrite.All', 'https://analysis.windows.net/powerbi/api/Tenant.Read.All', 'offline_access']
        request_body = {
            "client_id": creds["clientId"],
            "client_secret": creds["clientSecret"],
            "scope": ' '.join(scopes),
            "grant_type": "refresh_token",
            "refresh_token": creds["refreshToken"]
        }
        response = requests.post(token_endpoint, data=request_body)
        response_json = response.json()
        if "access_token" in response_json:
            return response_json["access_token"]
        else:
            return {"access_token": "Invalid access_token"}
    except Exception as error:
        raise Exception(error)

def microsoft_power_bi_get_many_report(accessToken):
    """
    Returns a list of reports from My workspace.

    :param str accessToken: The access token used for authenticating the API request.

    Returns:
        list: A list of dictionaries, each containing details of a report.
    """
    try:
        url = "https://api.powerbi.com/v1.0/myorg/reports"
        headers = {
            "Authorization": f"Bearer {accessToken}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()["value"]
            return result
        else:
            raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
    except Exception as error:
        raise Exception(error)

def microsoft_power_bi_get_report(accessToken, params):
    """
    Returns the specified report from My workspace.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict params: A dictionary containing parameters for the request.

        - :reportId: (string,required) - The report ID

    Returns:
        dict: A dictionary containing details of the specified report.
    """
    try:
        if "reportId" in params:
            reportId = params["reportId"]
            url = f"https://api.powerbi.com/v1.0/myorg/reports/{reportId}"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.get(url=url, headers=headers)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_power_bi_get_many_report_in_group(accessToken, params):
    """
    Returns a list of reports from the specified workspace.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict params: A dictionary containing parameters for the request.

        - :groupId: (string,required) - The workspace ID

    Returns:
        list: A list of dictionaries, each containing details of a report.
    """
    try:
        if "groupId" in params:
            groupId = params["groupId"]
            url = f"https://api.powerbi.com/v1.0/myorg/groups/{groupId}/reports"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.get(url=url, headers=headers)
            if response:
                result = response.json()["value"]
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_power_bi_get_report_in_group(accessToken, params):
    """
    Returns the specified report from the specified workspace.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict params: A dictionary containing parameters for the request.

        - :groupId: (string,required) - The workspace ID
        - :reportId: (string,required) - The report ID

    Returns:
        dict: A dictionary containing details of the specified report.
    """
    try:
        if "groupId" in params and "reportId" in params:
            groupId = params["groupId"]
            reportId = params["reportId"]
            url = f"https://api.powerbi.com/v1.0/myorg/groups/{groupId}/reports/{reportId}"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.get(url=url, headers=headers)
            if response:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_power_bi_clone_report(accessToken, params):
    """
    Clones the specified report from My workspace.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict params: A dictionary containing parameters for the request.

        - :reportId: (string,required) - The report ID
        - :name: (string,required) - The new report name

    Returns:
        dict: A dictionary containing details of the cloned report.
    """
    try:
        if "reportId" in params:
            reportId = params["reportId"]
            url = f'https://api.powerbi.com/v1.0/myorg/reports/{reportId}/Clone'
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_power_bi_delete_report(accessToken, params):
    """
    Deletes the specified report from My workspace.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict params: A dictionary containing parameters for the request.

        - :reportId: (string,required) - The report ID

    Returns:
        dict: Confirmation message after successful deletion.
    """
    try:
        if "reportId" in params:
            reportId = params["reportId"]
            url = f'https://api.powerbi.com/v1.0/myorg/reports/{reportId}'
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            response = requests.delete(url, headers=headers)
            if response.status_code == 200:
                return {"message": "Report deleted successfully!"}
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_power_bi_rebind_report(accessToken, params):
    """
    Rebinds the specified report from My workspace to the specified dataset.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict params: A dictionary containing parameters for the request.

        - :reportId: (string,required) - The report ID
        - :datasetId: The new dataset for the rebound report. If the dataset resides in a different workspace than the report, a shared dataset will be created in the report's workspace.

    Returns:
        dict: A dictionary containing a success message.
    """
    try:
        if "reportId" in params and "datasetId" in params:
            reportId = params["reportId"]
            url = f'https://api.powerbi.com/v1.0/myorg/reports/{reportId}/Rebind'
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            data = {}
            for key, value in params.items():
                skip_keys = ["reportId"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                return {"message": "Report successfully rebound to dataset."}
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_power_bi_get_many_report_page(accessToken, params):
    """
    Returns a list of pages within the specified report from My workspace.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict params: A dictionary containing parameters for the request.

        - :reportId: (string,required) - The report ID

    Returns:
        dict: A dictionary containing information about the report pages
    """
    try:
        if "reportId" in params:
            reportId = params["reportId"]
            url = f'https://api.powerbi.com/v1.0/myorg/reports/{reportId}/pages'
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_power_bi_get_report_page(accessToken, params):
    """
    Returns the specified page within the specified report from My workspace.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict params: A dictionary containing parameters for the request.

        - :reportId: (string,required) - The report ID
        - :pageName: (string,required) - The page name

    Returns:
        dict: A dictionary containing information about the report page
    """
    try:
        if "reportId" in params and "pageName" in params:
            reportId = params["reportId"]
            pageName = params["pageName"]
            url = f'https://api.powerbi.com/v1.0/myorg/reports/{reportId}/pages/{pageName}'
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_power_bi_get_import(accessToken, params):
    """
    Returns the specified import from My workspace.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict params: A dictionary containing parameters for the request.

        - :importId: (string,required) - The import ID

    Returns:
        dict: A dictionary containing details of the specified import.
    """
    try:
        if "importId" in params:
            importId = params["importId"]
            url = f"https://api.powerbi.com/v1.0/myorg/imports/{importId}"
            headers = {
                "Authorization": f"Bearer {accessToken}",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)


def microsoft_power_bi_get_many_import(accessToken):
    """
    Returns a list of imports for the organization.

    :param str accessToken: The access token used for authenticating the API request.

    Returns:
        list: A list of dictionaries, each containing details of a import.
    """
    try:
        url = "https://api.powerbi.com/v1.0/myorg/admin/imports"
        headers = {
            "Authorization": f"Bearer {accessToken}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()["value"]
            return result
        else:
            raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
    except Exception as error:
        raise Exception(error)

def microsoft_power_bi_get_import_in_group(accessToken, params):
    """
    Returns the specified import from the specified workspace.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict params: A dictionary containing parameters for the request.

        - :importId: (string,required) - The import ID
        - :groupId: (string,required) - The group ID

    Returns:
        dict: A dictionary containing details of the specified import.
    """
    try:
        if "groupId" in params and "importId" in params:
            groupId = params["groupId"]
            importId = params["importId"]
            url = f"https://api.powerbi.com/v1.0/myorg/groups/{groupId}/imports/{importId}"
            headers = {
                "Authorization": f"Bearer {accessToken}",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_power_bi_get_dataset(accessToken, params):
    """
    Returns the specified dataset from My workspace.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict params: A dictionary containing parameters for the request.

        - :datasetId: (string,required) - The dataset ID

    Returns:
        dict: A dictionary containing details of the specified dataset.
    """
    try:
        if "datasetId" in params:
            datasetId = params["datasetId"]
            url = f"https://api.powerbi.com/v1.0/myorg/datasets/{datasetId}"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)


def microsoft_power_bi_get_many_dataset(accessToken):
    """
    Returns a list of datasets from My workspace.

    :param str accessToken: The access token used for authenticating the API request.

    Returns:
        list: A list of dictionaries, each containing details of a dataset.
    """
    try:
        url = "https://api.powerbi.com/v1.0/myorg/datasets"
        headers = {
            "Authorization": f"Bearer {accessToken}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()["value"]
            return result
        else:
            raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
    except Exception as error:
        raise Exception(error)

def microsoft_power_bi_get_dataset_in_group(accessToken, params):
    """
    Returns the specified dataset from the specified workspace.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict params: A dictionary containing parameters for the request.

        - :groupId: (string,required) - The workspace ID
        - :datasetId: (string,required) - The dataset ID

    Returns:
        dict: A dictionary containing details of the specified dataset.
    """
    try:
        if "groupId" in params and "datasetId" in params:
            groupId = params["groupId"]
            datasetId = params["datasetId"]
            url = f"https://api.powerbi.com/v1.0/myorg/groups/{groupId}/datasets/{datasetId}"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_power_bi_get_many_dataset_in_group(accessToken, params):
    """
    Returns a list of datasets from the specified workspace.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict params: A dictionary containing parameters for the request.

        - :groupId: (string,required) - The workspace ID

    Returns:
        list: A list of dictionaries, each containing details of a dataset.
    """
    try:
        if "groupId" in params:
            groupId = params["groupId"]
            url = f"https://api.powerbi.com/v1.0/myorg/groups/{groupId}/datasets"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                result = response.json()["value"]
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_power_bi_get_dataset_users(accessToken, params):
    """
    Returns a list of principals that have access to the specified dataset.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict params: A dictionary containing parameters for the request.

        - :datasetId: (string,required) - The dataset ID

    Returns:
        list: A list of dictionaries, each containing details of a principal that has access to the dataset.
    """
    try:
        if "datasetId" in params:
            datasetId = params["datasetId"]
            url = f"https://api.powerbi.com/v1.0/myorg/datasets/{datasetId}/users"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                result = response.json()["value"]
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_power_bi_get_datasources(accessToken, params):
    """
    Returns a list of data sources for the specified dataset from My workspace.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict params: A dictionary containing parameters for the request.

        - :datasetId: (string,required) - The dataset ID

    Returns:
        list: A list of dictionaries, each containing details of a data source.
    """
    try:
        if "datasetId" in params:
            datasetId = params["datasetId"]
            url = f"https://api.powerbi.com/v1.0/myorg/datasets/{datasetId}/datasources"
            headers = {
                "Authorization": "Bearer " + accessToken,
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                result = response.json()["value"]
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_power_bi_create_dataset(accessToken, params):
    """
    Creates a new dataset on My workspace.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict params: A dictionary containing parameters for the request.
    
        - :name: (str, required) - The dataset name
        - :tables: (list, required) - The dataset tables.
        
            Each table dictionary should contain:
            
            - :name: (str, required) - The table name
            - :description: (str, optional) - The table description
            - :columns: (list, required) - The column schema for this table
            
                Each column dictionary should contain:
                
                - :name: (str, required) - The column name
                - :dataType: (str, required) - The column data type

    Returns:
        dict: A dictionary containing details of the created dataset.
    """
    try:
        if "name" in params and "tables" in params:
            url = f"https://api.powerbi.com/v1.0/myorg/datasets"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {accessToken}'
            }
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 201:
                result = response.json()
                return result
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_power_bi_get_dataset_tables(accessToken, params):
    """
    Returns a list of tables within the specified dataset from My workspace.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict params: A dictionary containing parameters for the request.

        - :datasetId: (string,required) - The dataset ID

    Returns:
        dict: A dictionary containing the details of the tables in the specified dataset.
    """
    try:
        if "datasetId" in params:
            datasetId = params["datasetId"]
            url = f"https://api.powerbi.com/v1.0/myorg/datasets/{datasetId}/tables"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {accessToken}'
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()["value"]
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_power_bi_update_dataset_table(accessToken, params):
    """
    Updates the metadata and schema for the specified table within the specified dataset from My workspace.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict params: A dictionary containing parameters for the request.

        - :datasetId: (string,required) - The dataset ID
        - :name: (string,required) - The table name
        - :description: (string,optional) - The table description
        - :columns: (list,required) - The column schema for this table
        
            Each column dictionary should contain:
            
            - :name: (str, required) - The column name
            - :dataType: (str, required) - The column data type
            
    Returns:
        dict: A dictionary containing the details of the updated table.
    """
    try:
        if "datasetId" in params and "name" in params and "columns" in params:
            datasetId = params["datasetId"]
            name = params["name"]
            url = f"https://api.powerbi.com/v1.0/myorg/datasets/{datasetId}/tables/{name}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {accessToken}'
            }
            data = {}
            for key, value in params.items():
                skip_keys = ["datasetId"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            response = requests.put(url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_power_bi_add_rows_to_table(accessToken,params):
    """
    Adds new data rows to the specified table within the specified dataset from My workspace.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict params: A dictionary containing parameters for the request.

        - :datasetId: (string,required) - The dataset ID
        - :name: (string,required) - The table name
        - :rows: (list,required) - An array of data rows pushed to a dataset table. Each element is a collection of properties represented using key-value format.

    Returns:
        dict: A dictionary containing success message.
    """
    try:
        if "datasetId" in params and "name" in params and "rows" in params :
            datasetId = params["datasetId"]
            name = params["name"]
            url = f"https://api.powerbi.com/v1.0/myorg/datasets/{datasetId}/tables/{name}/rows"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {accessToken}'
            }
            data = {}
            for key, value in params.items():
                skip_keys = ["datasetId","name"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                return {"message":"Rows successfully added to the table."}
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)

def microsoft_power_bi_delete_rows(accessToken,params):
    """
    Deletes all rows from the specified table within the specified dataset from My workspace.

    :param str accessToken: The access token used for authenticating the API request.
    :param dict params: A dictionary containing parameters for the request.

        - :datasetId: (string,required) - The dataset ID
        - :name: (string,required) - The table name

    Returns:
        dict: Confirmation message after successful deletion.
    """
    try:
        if "datasetId" in params and "name" in params:
            datasetId = params["datasetId"]
            name = params["name"]
            url = f"https://api.powerbi.com/v1.0/myorg/datasets/{datasetId}/tables/{name}/rows"
            headers = {
                "Authorization": "Bearer " + accessToken,
            }
            response = requests.delete(url=url, headers=headers)
            if response:
                return {"message": "Rows deleted successfully!"}
            else:
                raise Exception(f"Status code: {response.status_code}. Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)