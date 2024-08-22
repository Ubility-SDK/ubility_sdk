import requests
import base64
import json

def bamboohr_get_report(cred,params):
    """
    Get company report from BambooHR.

    :param str apiKey: The API key for authenticating with BambooHR.
    :param str subdomain: The subdomain of your BambooHR account.
    :param dict params: Dictionary containing parameters.

        - :id: (str,required) - Id is a report ID.
        - :format: (str,required) - The output format for the report. Supported formats: pdf,json,xls,xml,csv
        - :onlyCurrent: (bool,optional) - Setting to false will return future dated values from history table fields.
        - :fd: (str,optional) - duplicate field filtering, no=return the raw results with no duplicate filtering. Default value is "yes"

    Returns:
        dict or str: The report data in the specified format.
    """
    try:
        creds=json.loads(cred)
        if (
            "id" in params
            and "format" in params
            and "subdomain" in creds
            and "apiKey" in creds
        ):
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            id = params["id"]
            report_format = params["format"]
            base_url = (
                f"https://api.bamboohr.com/api/gateway.php/{subdomain}/v1/reports/{id}"
            )
            apiKey = f"{apiKey}:"
            encoded_api_key = base64.b64encode(apiKey.encode()).decode()
            data = {}
            for key, value in params.items():
                skip_keys = ["id", "format"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            report_format = params["format"]
            content_type = ""
            if report_format == "pdf" or report_format == "json":
                content_type = f"application/{report_format}"
            elif report_format == "xls":
                content_type = "application/vnd.ms-excel"
            elif report_format == "csv" or report_format == "xml":
                content_type = f"text/{report_format}"
            headers = {
                "Authorization": f"Basic {encoded_api_key}",
                "Accept": content_type,
            }
            response = requests.get(
                base_url,
                json=data,
                headers=headers,
            )
            if response:
                if report_format == "json":
                    report_data = response.json()
                else:
                    report_data = response.text
                return report_data
            else:
                raise Exception(
                    f"Failed to retrieve report. Status code: {response.status_code}{response.text}"
                )
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)


def bamboohr_create_employee(cred,params):
    """
    create an employee to BambooHR.

    :param str apiKey: The API key for authenticating with BambooHR.
    :param str subdomain: The subdomain of your BambooHR account.
    :param dict params: Dictionary containing parameters.

        - :firstName: (str,required) - The first name of the employee.
        - :lastName: (str,required) - The last name of the employee.
        - :department: (str,optional) - The department of the employee.
        - :jobTitle: (str,optional) - The job title of the employee.
        - :workPhone: (str,optional) - The work phone number of the employee.
        - :mobilePhone: (str,optional) - The mobile phone number of the employee.
        - :workEmail: (str,optional) - The work email address of the employee.
        - :location: (str,optional) - The location of the employee.
        - :division: (str,optional) - The division of the employee.
        - :linkedIn: (str,optional) - The LinkedIn profile URL of the employee.
        - :instagram: (str,optional) - The Instagram username of the employee.
        - :pronouns: (str,optional) - The pronouns of the employee.
        - :workPhoneExtension: (str,optional) - The work phone extension of the employee.
        - :supervisor: (str,optional) - The supervisor of the employee.

    Returns:
        dict: Information about the created employee.
    """
    try:
        creds=json.loads(cred)
        if (
            "firstName" in params
            and "lastName" in params
            and "subdomain" in creds
            and "apiKey" in creds
        ):
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            base_url = (
                f"https://api.bamboohr.com/api/gateway.php/{subdomain}/v1/employees/"
            )
            apiKey = f"{apiKey}:"
            encoded_api_key = base64.b64encode(apiKey.encode()).decode()
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            headers = {
                "content-type": "application/json",
                "Authorization": f"Basic {encoded_api_key}",
            }
            response = requests.post(base_url, json=data, headers=headers)
            if response.status_code == 201:
                data = response.headers["Location"]
                parts = data.split("/")
                id = parts[-1]
                return {"id": id}
            else:
                raise Exception(
                    {
                        "error": f"Failed to create employee. Status code: {response.status_code}{response.text}"
                    }
                )
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)


def bamboohr_get_employee_by_id(cred,params):
    """
    Get employee information from BambooHR by employee ID.

    :param str apiKey: The API key for authenticating with BambooHR.
    :param str subdomain: The subdomain of your BambooHR account.
    :param dict params: Dictionary containing parameters.

        - :id: (str,required) - The employee ID.
        - :fields: (str,optional): A comma-separated list of fields to include in the response.
            Available fields: employeeNumber, firstName, lastName, department, jobTitle, workPhone,mobilePhone, workEmail, location, division, linkedIn, displayName, preferredName,instagram, pronouns, workPhoneExtension, supervisor, photoUploaded, canUploadPhoto.

    Returns:
        dict: The employee details.
    """
    try:
        creds=json.loads(cred)
        if "id" in params and "subdomain" in creds and "apiKey" in creds:
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            id = params["id"]
            base_url = f"https://api.bamboohr.com/api/gateway.php/{subdomain}/v1/employees/{id}/"
            apiKey = f"{apiKey}:"
            encoded_api_key = base64.b64encode(apiKey.encode()).decode()
            data = {}
            for key, value in params.items():
                skip_keys = ["id"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            headers = {
                "Accept": "application/json",
                "Authorization": f"Basic {encoded_api_key}",
            }
            response = requests.get(
                base_url,
                params=data,
                headers=headers,
            )
            if response.status_code == 200:
                employee_data = response.json()
                return employee_data
            else:
                raise Exception(
                    {
                        "error": f"Failed to get employee. Status code: {response.status_code}{response.text}"
                    }
                )
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)


def bamboohr_get_employee_directory(cred):
    """
    Get the employee directory from BambooHR.

    :param str apiKey: The API key for authenticating with BambooHR.
    :param str subdomain: The subdomain of your BambooHR account.

    Returns:
        list: List of employees
    """
    try:
        creds=json.loads(cred)
        if "subdomain" in creds and "apiKey" in creds:
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            base_url = f"https://api.bamboohr.com/api/gateway.php/{subdomain}/v1/employees/directory"
            apiKey = f"{apiKey}:"
            encoded_api_key = base64.b64encode(apiKey.encode()).decode()
            headers = {
                "Accept": "application/json",
                "Authorization": f"Basic {encoded_api_key}",
            }
            response = requests.get(
                base_url,
                headers=headers,
            )
            if response.status_code == 200:
                employee_data = response.json()
                return employee_data
            else:
                raise Exception(
                    {
                        "error": f"Request failed with status code: {response.status_code} {response.text}"
                    }
                )
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)


def bamboohr_update_employee(cred,params):
    """
    Update employee information in BambooHR.

    :param str apiKey: The API key for authenticating with BambooHR.
    :param str subdomain: The subdomain of your BambooHR account.
    :param dict params: Dictionary containing parameters.

        - :id: (str,required) - Id is an employee ID.
        - :firstName: (str,optional) - The first name of the employee.
        - :lastName: (str,optional) - The last name of the employee.
        - :department: (str,optional) - The department of the employee.
        - :jobTitle: (str,optional) - The job title of the employee.
        - :workPhone: (str,optional) - The work phone number of the employee.
        - :mobilePhone: (str,optional) - The mobile phone number of the employee.
        - :workEmail: (str,optional) - The work email address of the employee.
        - :location: (str,optional) - The location of the employee.
        - :division: (str,optional) - The division of the employee.
        - :linkedIn: (str,optional) - The LinkedIn profile URL of the employee.
        - :instagram: (str,optional) - The Instagram username of the employee.
        - :pronouns: (str,optional) - The pronouns of the employee.
        - :workPhoneExtension: (str,optional) - The work phone extension of the employee.
        - :supervisor: (str,optional) - The supervisor of the employee.

    Returns:
        dict: The updated employee information.
    """
    try:
        creds=json.loads(cred)
        if "id" in params and "subdomain" in creds and "apiKey" in creds:
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            id = params["id"]
            base_url = f"https://api.bamboohr.com/api/gateway.php/{subdomain}/v1/employees/{id}/"
            apiKey = f"{apiKey}:"
            encoded_api_key = base64.b64encode(apiKey.encode()).decode()
            data = {}
            headers = {
                "content-type": "application/json",
                "Authorization": f"Basic {encoded_api_key}",
            }
            for key, value in params.items():
                skip_keys = ["id"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            if data:
                response = requests.post(base_url, json=data, headers=headers)
                if response.status_code == 200:
                    return {
                        "message": "Employee information has been successfully updated"
                    }
                else:
                    raise Exception(
                        {
                            "error": f"Unable to update employee. Status code {response.status_code} {response.text}"
                        }
                    )
            else:
                raise Exception({"error": "At least one field must be updated"})
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)


def bamboohr_get_employee_file(cred,params):
    """
    List employee files and categories in BambooHR.

    :param str apiKey: The API key for authenticating with BambooHR.
    :param str subdomain: The subdomain of your BambooHR account.
    :param dict params: Dictionary containing parameters.

        - :id: (str,required) - The employee ID.

    Returns:
        list: List of employee files and categories.
    """
    try:
        creds=json.loads(cred)
        if "id" in params and "subdomain" in creds and "apiKey" in creds:
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            id = params["id"]
            base_url = f"https://api.bamboohr.com/api/gateway.php/{subdomain}/v1/employees/{id}/files/view/"
            apiKey = f"{apiKey}:"
            encoded_api_key = base64.b64encode(apiKey.encode()).decode()
            headers = {
                "Accept": "application/json",
                "Authorization": f"Basic {encoded_api_key}",
            }
            response = requests.get(
                base_url,
                headers=headers,
            )
            if response.status_code == 200:
                file_data = response.json()
                return file_data
            else:
                raise Exception(
                    {
                        "error": f"Request failed with status code: {response.status_code}  {response.text}"
                    }
                )
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)


def bamboohr_delete_employee_file(cred,params):
    """
    Delete an employee file in BambooHR.

    :param str apiKey: The API key for authenticating with BambooHR.
    :param str subdomain: The subdomain of your BambooHR account.
    :param dict params: Dictionary containing parameters.

        - :id: (str,required) - The employee ID.
        - :fileId: (str,required) - The ID of the employee file being deleted.

    Returns:
        dict: A confirmation message indicating successful deletion.
    """
    try:
        creds=json.loads(cred)
        if "id" in params and "fileId" in params and "subdomain" in creds and "apiKey" in creds:
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            id = params["id"]
            fileId = params["fileId"]
            base_url = f"https://api.bamboohr.com/api/gateway.php/{subdomain}/v1/employees/{id}/files/{fileId}"
            apiKey = f"{apiKey}:"
            encoded_api_key = base64.b64encode(apiKey.encode()).decode()
            headers = {
                "Authorization": f"Basic {encoded_api_key}",
            }
            response = requests.delete(
                base_url,
                headers=headers,
            )
            if response.status_code == 200:
                return {"message": "File deleted successfully"}
            else:
                raise Exception(
                    {
                        "error": f"Request failed with status code: {response.status_code}   {response.text}"
                    }
                )
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)


def bamboohr_update_employee_file(cred,params):
    """
    Update Employee File in BambooHR.

    :param str apiKey: The API key for authenticating with BambooHR.
    :param str subdomain: The subdomain of your BambooHR account.
    :param dict params: Dictionary containing parameters.

        - :id: (str,required) - The employee ID.
        - :fileId: (str,required) - The ID of the employee file being updated.
        - :shareWithEmployee: (str,optional) - Update whether this file is shared or not ( 'yes' or 'no' ).
        - :categoryId: (str,optional) - move the file to a different category.
        - :name: (str,optional) - rename the file.

    Returns:
        dict: A confirmation message indicating successful of the update.
    """
    try:
        creds=json.loads(cred)
        if  "id" in params   and "fileId" in params and "subdomain" in creds and "apiKey" in creds:
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            id = params["id"]
            fileId = params["fileId"]
            base_url = f"https://api.bamboohr.com/api/gateway.php/{subdomain}/v1/employees/{id}/files/{fileId}"
            apiKey = f"{apiKey}:"
            encoded_api_key = base64.b64encode(apiKey.encode()).decode()
            data = {}
            for key, value in params.items():
                skip_keys = ["id", "fileId"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            headers = {
                "content-type": "application/json",
                "Authorization": f"Basic {encoded_api_key}",
            }
            response = requests.post(base_url, json=data, headers=headers)
            if response.status_code == 200:
                return {"message": "File details updated successfully"}
            else:
                raise Exception(
                    {
                        "error": f"Request failed with status code: {response.status_code}   {response.text}"
                    }
                )
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)


def bamboohr_upload_employee_file(cred,params):
    """
    Upload Employee File in BambooHR.

    :param str apiKey: The API key for authenticating with BambooHR.
    :param str subdomain: The subdomain of your BambooHR account.
    :param dict params: Dictionary containing parameters.

        - :id: (str,required) - The employee ID.
        - :category: (str,required) - The category ID to place the new file in.
        - :fileName: (str,required) - The file name to associate with the file.
        - :share: (str,optional) - Whether to make the file available to the employee (options are "yes" and "no").
        - :binary_data: (bytes,optional) - Binary content of the attachment. (if 'file_url' is not provided)
        - :file_url: (str,optional) - URL of the file to attach. (if 'binary_data' is not provided)

    Returns:
        dict: A confirmation message indicating successful of the upload.
    """

    try:
        creds=json.loads(cred)
        if "category" in params and "fileName" in params and "id" in params and "subdomain" in creds and "apiKey" in creds:
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            id = params["id"]
            base_url = f"https://api.bamboohr.com/api/gateway.php/{subdomain}/v1/employees/{id}/files"
            apiKey = f"{apiKey}:"
            encoded_api_key = base64.b64encode(apiKey.encode()).decode()
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            headers = {
                "Authorization": f"Basic {encoded_api_key}",
            }
            if "binary_data" in params:
                file_content = params["binary_data"]
                files = {
                    "file": (
                        params["fileName"],
                        file_content,
                    )
                }
            elif "file_url" in params:
                file_url = params["file_url"]
                response = requests.get(file_url)
                file_content = response.content
                files = {
                    "file": (
                        params["fileName"],
                        file_content,
                    )
                }
            else:
                raise Exception({"error": "Invalid file data provided."})
            response = requests.post(
                base_url,
                headers=headers,
                data=data,
                files=files,
            )
            if response.status_code == 201:
                return {"message": "File uploaded successfully."}
            else:
                raise Exception(
                    {
                        "error": f"Error uploading file. Status code: {response.status_code}, Response: {response.text}"
                    }
                )
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)


def bamboohr_view_company_files(cred):
    """
    Get multiple company files and categories from BambooHR.

    :param str apiKey: The API key for authenticating with BambooHR.
    :param str subdomain: The subdomain of your BambooHR account.

    Returns:
        dict: Company files and category list
    """

    try:
        creds=json.loads(cred)
        if "subdomain" in creds and "apiKey" in creds:
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            base_url = (
                f"https://api.bamboohr.com/api/gateway.php/{subdomain}/v1/files/view/"
            )
            apiKey = f"{apiKey}:"
            encoded_api_key = base64.b64encode(apiKey.encode()).decode()
            headers = {
                "Authorization": f"Basic {encoded_api_key}",
                "Accept": "application/json",
            }
            response = requests.get(base_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                raise Exception(
                    {
                        "error": f"Request failed with status code: {response.status_code}  {response.text}"
                    }
                )
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)


def bamboohr_delete_company_file(cred,params):
    """
    Delete a company file in BambooHR.

    :param str apiKey: The API key for authenticating with BambooHR.
    :param str subdomain: The subdomain of your BambooHR account.
    :param dict params: Dictionary containing parameters.

        - :fileId: (str,required) - The ID of the company file being deleted.

    Returns:
        dict: A confirmation message indicating successful deletion.
    """
    try:
        creds=json.loads(cred)
        if "fileId" in params and "subdomain" in creds and "apiKey" in creds:
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            fileId = params["fileId"]
            base_url = f"https://api.bamboohr.com/api/gateway.php/{subdomain}/v1/files/{fileId}"
            apiKey = f"{apiKey}:"
            encoded_api_key = base64.b64encode(apiKey.encode()).decode()
            headers = {
                "Authorization": f"Basic {encoded_api_key}",
            }
            response = requests.delete(
                base_url,
                headers=headers,
            )
            if response.status_code == 200:
                return {"message": "File deleted successfully"}
            else:
                raise Exception(
                    {
                        "error": f"Request failed with status code: {response.status_code}   {response.text}"
                    }
                )
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)


def bamboohr_update_company_file(cred,params):
    """
    Update Employee File in BambooHR.

    :param str apiKey: The API key for authenticating with BambooHR.
    :param str subdomain: The subdomain of your BambooHR account.
    :param dict params: Dictionary containing parameters.

        - :fileId: (str,required) - The ID of the employee file being updated.
        - :name: (str,optional) - rename the file.
        - :categoryId: (str,optional) - move the file to a different category.
        - :shareWithEmployee: (str,optional) - Update whether this file is shared or not ( 'yes' or 'no' )

    Returns:
        dict: A confirmation message indicating successful of the update.
    """
    try:
        creds=json.loads(cred)
        if "fileId" in params and "subdomain" in creds and "apiKey" in creds:
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            fileId = params["fileId"]
            base_url = f"https://api.bamboohr.com/api/gateway.php/{subdomain}/v1/files/{fileId}"
            apiKey = f"{apiKey}:"
            encoded_api_key = base64.b64encode(apiKey.encode()).decode()
            data = {}
            for key, value in params.items():
                skip_keys = ["fileId"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            headers = {
                "content-type": "application/json",
                "Authorization": f"Basic {encoded_api_key}",
            }
            response = requests.post(base_url, json=data, headers=headers)
            if response.status_code == 200:
                return {"message": "File details updated successfully"}
            else:
                raise Exception(
                    {
                        "error": f"Request failed with status code: {response.status_code} {response.text}"
                    }
                )
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)


def bamboohr_upload_company_file(cred,params):
    """
    Upload Company File in BambooHR.

    :param str apiKey: The API key for authenticating with BambooHR.
    :param str subdomain: The subdomain of your BambooHR account.
    :param dict params: Dictionary containing parameters.

        - :category: (str,required) - The category ID to place the new file in.
        - :fileName: (str,required) - The file name to associate with the file.
        - :share: (str,optional) - Whether to make the file available to the employee (options are "yes" and "no").
        - :binary_data: (bytes,optional) - Binary content of the attachment. (if 'file_url' is not provided)
        - :file_url: (str,optional) - URL of the file to attach. (if 'binary_data' is not provided)

    Returns:
        dict: A confirmation message indicating successful of the upload.
    """
    try:
        creds=json.loads(cred)
        if "category" in params and "fileName" in params and "subdomain" in creds and "apiKey" in creds:
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            base_url = f"https://api.bamboohr.com/api/gateway.php/{subdomain}/v1/files"
            apiKey = f"{apiKey}:"
            encoded_api_key = base64.b64encode(apiKey.encode()).decode()
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            headers = {
                "Authorization": f"Basic {encoded_api_key}",
            }
            if "binary_data" in params:
                file_content = params["binary_data"]
                files = {
                    "file": (
                        params["fileName"],
                        file_content,
                    )
                }
            elif "file_url" in params:
                file_url = params["file_url"]
                response = requests.get(file_url)
                file_content = response.content
                files = {
                    "file": (
                        params["fileName"],
                        file_content,
                    )
                }
            else:
                raise Exception({"error": "Invalid file data provided."})
            response = requests.post(base_url, headers=headers, data=data, files=files)
            if response.status_code == 201:
                return {"message": "File uploaded successfully."}
            else:
                raise Exception(
                    {
                        "error": f"Error uploading file. Status code: {response.status_code}, Response: {response.text}"
                    }
                )
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)


def bamboohr_get_whos_out(cred,params):
    """
    Get information about employees out of the office in BambooHR.

    :param str apiKey: The API key for authenticating with BambooHR.
    :param str subdomain: The subdomain of your BambooHR account.
    :param dict params: Dictionary containing parameters.

        - :start: (date,optional) - A date in the form YYYY-MM-DD - defaults to the current date.
        - :end: (date,optional) - A date in the form YYYY-MM-DD - defaults to 14 days from the start date.

    Returns:
        list: list, sorted by date, of employees who will be out, and company holidays, for a period of time
    """
    try:
        creds=json.loads(cred)
        if "subdomain" in creds and "apiKey" in creds:
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            base_url = f"https://api.bamboohr.com/api/gateway.php/{subdomain}/v1/time_off/whos_out/"
            apiKey = f"{apiKey}:"
            encoded_api_key = base64.b64encode(apiKey.encode()).decode()
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            headers = {
                "Accept": "application/json",
                "Authorization": f"Basic {encoded_api_key}",
            }
            response = requests.get(
                base_url,
                params=data,
                headers=headers,
            )
            if response.status_code == 200:
                whos_out_data = response.json()
                return whos_out_data
            else:
                raise Exception(
                    {
                        "error": f"Failed to fetch 'Who's Out' data. Status code: {response.status_code} {response.text}"
                    }
                )
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)


def bamboohr_respond_to_timeoff_request(cred,params):
    """
    Respond to a time-off request in BambooHR.

    :param str apiKey: The API key for authenticating with BambooHR.
    :param str subdomain: The subdomain of your BambooHR account.
    :param dict params: Dictionary containing parameters.

        - :requestId: (str,required) - The ID of the time-off request to respond to.
        - :status: (str,required) - One of approved, cancelled, denied.
        - :note: (str,optional) - A note to attach to the change in status.

    Returns:
        dict: A message indicating the success of the time-off request response.
    """
    try:
        creds=json.loads(cred)
        if "requestId" in params and "status" in params and "subdomain" in creds and "apiKey" in creds :
            subdomain = creds["subdomain"]
            apiKey = creds["apiKey"]
            requestId = params["requestId"]
            base_url = f"https://api.bamboohr.com/api/gateway.php/{subdomain}/v1/time_off/requests/{requestId}/status"
            apiKey = f"{apiKey}:"
            encoded_api_key = base64.b64encode(apiKey.encode()).decode()
            data = {}
            for key, value in params.items():
                skip_keys = ["requestId"]
                if key in skip_keys:
                    continue
                if value:
                    data[key] = value
            headers = {
                "Accept": "application/json",
                "Authorization": f"Basic {encoded_api_key}",
            }
            response = requests.put(
                base_url,
                json=data,
                headers=headers,
            )
            if response.status_code == 200:
                return {"message": "Successfully responded to the time-off request"}
            else:
                raise Exception(
                    {
                        "error": f"Failed to fetch time-off requests. Status code: {response.status_code}{response.text}"
                    }
                )
        else:
            raise Exception("Missing input data")
    except Exception as error:
        raise Exception(error)
