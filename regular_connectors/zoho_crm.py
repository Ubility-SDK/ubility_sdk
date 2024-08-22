import requests
import json

######################     Generate Access Token      ######################

def zohoCRM_refresh_access_token(cred):
    """
    Refresh the Zoho CRM access token using a refresh token.

    :client_id: (str) - The client ID of the Zoho CRM connected app.
    :client_secret: (str) - The client secret of the Zoho CRM connected app.
    :refresh_token: (str) - The refresh token obtained during the initial authorization.

    Returns:
      str: The refreshed Zoho CRM access token.

    """
    try:
        credentials=json.loads(cred)
        refresh_token=credentials['refreshToken']
        client_id=credentials['clientID']
        client_secret=credentials['clientSecret']
        url = f"https://accounts.zoho.com/oauth/v2/token?refresh_token={refresh_token}&client_id={client_id}&client_secret={client_secret}&grant_type=refresh_token"
        response = requests.post(url)
        response_json = response.json()
        if "access_token" in response_json:
            return response_json["access_token"]
        else:
            raise Exception({"access_token": "Invalid access_token"})

    except Exception as error:
        raise Exception(error)
   
###########################################################################################################################
# Contact Actions


def zohoCRM_list_contacts(access_token, params):
    """
    List contacts based on specified parameters.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing optional parameters for filtering and pagination:

    - :fields: (str) - Comma-separated list of fields to be retrieved.
    - :converted: (str) - To include only converted contacts.

            (Values: 'true' or 'false')

    - :per_page: (int) - Number of contacts to be retrieved per page. Default is 200.
    - :sort_by: (str) - Field by which contacts should be sorted.

        (Options: id, Created_Time, Modified_Time)

    - :sort_order: (str) - Sorting order, either "asc" or "desc".
    - :include_child: (str) - To include child records.

            (Values: 'true' or 'false')

    - :territory_id: (str) - Filter contacts by territory ID.

    Returns:
      dict: A dictionary containing a list of contacts retrieved from Zoho CRM.

    """
    try:
        url = f"https://www.zohoapis.com/crm/v5/Contacts?"
        fields = "Owner,Full_Name,$currency_symbol,$field_states,Last_Activity_Time,$state,$process_flow,$locked_for_me,id,Created_Time,$editable,Created_By,$zia_owner_assignment,Description,$review_process,Record_Image,Modified_By,$review,Phone,Account_Name,Modified_Time,$orchestration,$in_merge,Locked__s,Tag,Fax,$approval_state"

        for key, value in params.items():
            if key == "fields":
                fields = value
                continue
            if value:
                url += f"&{key}={value}"

        url += f"&fields={fields}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 204:
            return {"Result": "No Contacts Yet!"}
        response_json = response.json()
        if "code" in response_json:
            if response_json["code"] == "UNABLE_TO_PARSE_DATA_TYPE":
                raise Exception("One of the parameters is in wrong format")
            else:
               raise Exception(response_json)
        return {"Contacts": response_json["data"]}

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


def zohoCRM_get_contact(access_token, params):
    """
    Retrieve information about a specific contact.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :contact_id: (str, required) - The ID of the contact to be retrieved.

    Returns:
      dict: A dictionary containing the information of the specified contact.

    """
    try:
        if "contact_id" in params and params["contact_id"]:
            id = params["contact_id"]
            url = f"https://www.zohoapis.com/crm/v5/Contacts/{id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            return {"Contact": response_json["data"]}

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("ID Not Found")
        else:
            raise Exception(e)


def zohoCRM_delete_contact(access_token, params):
    """
    Delete a contact.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :contact_id: (str, required) - The ID of the contact to be deleted.

    Returns:
      dict: A dictionary containing information about the status of the deletion.

    """
    try:
        if "contact_id" in params and params["contact_id"]:
            id = params["contact_id"]
            url = f"https://www.zohoapis.com/crm/v5/Contacts/{id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.delete(url, headers=headers)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("ID Not Found")
        else:
            raise Exception(e)


def zohoCRM_create_contact(access_token, params):
    """
    Create a new contact.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :Last_Name: (str, required) - The last name of the contact.
    - :Title: (str, optional) - The title of the contact.
    - ... (other parameters): Additional parameters that can be included in the params.

    Returns:
      dict: A dictionary containing information about the created contact.

    """
    try:
        if "Last_Name" in params and params["Last_Name"]:
            url = f"https://www.zohoapis.com/crm/v5/Contacts"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            paylod = {"data": [data]}
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers, json=paylod)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            if response_json["data"] and "code" in response_json["data"][0] and response_json["data"][0]["code"] != "SUCCESS":
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


def zohoCRM_update_contact(access_token, params):
    """
    Update an existing contact.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters:

    - :contact_id: (str, required) - The ID of the contact to be updated.
    - (Additional parameters): Other parameters to be updated, such as First_Name, Last_Name, etc.
        
    Returns:
      dict: A dictionary containing information about the updated contact.

    """
    try:
        if "contact_id" in params and params["contact_id"]:
            id = params["contact_id"]
            url = f"https://www.zohoapis.com/crm/v5/Contacts/{id}"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            paylod = {"data": [data]}
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.put(url, headers=headers, json=paylod)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            if response_json["data"] and "code" in response_json["data"][0] and response_json["data"][0]["code"] != "SUCCESS":
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


###########################################################################################################################
# Account Actions


def zohoCRM_list_accounts(access_token, params):
    """
    List accounts based on specified parameters.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing optional parameters for filtering and pagination:

    - :fields: (str) - Comma-separated list of fields to be retrieved.
    - :converted: (str) - To include only converted accounts.

            (Values: 'true' or 'false')

    - :per_page: (int) - Number of accounts to be retrieved per page. Default is 200.
    - :sort_by: (str) - Field by which accounts should be sorted.

        (Options: id, Created_Time, Modified_Time)

    - :sort_order: (str) - Sorting order, either "asc" or "desc".
    - :include_child: (str) - To include child records.

            (Values: 'true' or 'false')

    - :territory_id: (str) - Filter accounts by territory ID.

    Returns:
      dict: A dictionary containing a list of accounts retrieved from Zoho CRM.

    """
    try:
        url = f"https://www.zohoapis.com/crm/v5/Accounts?"
        fields = "Owner,$currency_symbol,$field_states,Account_Type,SIC_Code,Last_Activity_Time,Industry,Account_Site,$state,$process_flow,Billing_Country,$locked_for_me,$approval,Billing_Street,Created_Time,$wizard_connection_path,$editable,Billing_Code,Shipping_City,Shipping_Country,Shipping_Code,Billing_City,Created_By,$zia_owner_assignment,Annual_Revenue,Shipping_Street,Ownership,Description,Rating,Shipping_State,$review_process,Website,Employees,Record_Image,Modified_By,$review,Phone,Account_Name,$zia_visions,Account_Number,Ticker_Symbol,Modified_Time,$orchestration,Parent_Account,$in_merge,Locked__s,Billing_State,Tag,Fax,$approval_state"

        for key, value in params.items():
            if key == "fields":
                fields = value
                continue
            if value:
                url += f"&{key}={value}"

        url += f"&fields={fields}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 204:
            return {"Result": "No Accounts Yet!"}
        response_json = response.json()
        if "code" in response_json:
            if response_json["code"] == "UNABLE_TO_PARSE_DATA_TYPE":
                raise Exception("One of the parameters is in wrong format")
            else:
               raise Exception(response_json)
        return {"Accounts": response_json["data"]}

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


def zohoCRM_get_account(access_token, params):
    """
    Retrieve information about a specific account.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :account_id: (str, required) - The ID of the account to be retrieved.

    Returns:
      dict: A dictionary containing the information of the specified account.

    """
    try:
        if "account_id" in params and params["account_id"]:
            id = params["account_id"]
            url = f"https://www.zohoapis.com/crm/v5/Accounts/{id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            return {"Account": response_json["data"]}

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("ID Not Found")
        else:
            raise Exception(e)


def zohoCRM_delete_account(access_token, params):
    """
    Delete an account.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :account_id: (str, required) - The ID of the account to be deleted.

    Returns:
      dict: A dictionary containing information about the status of the deletion.

    """
    try:
        if "account_id" in params and params["account_id"]:
            id = params["account_id"]
            url = f"https://www.zohoapis.com/crm/v5/Accounts/{id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.delete(url, headers=headers)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("ID Not Found")
        else:
            raise Exception(e)


def zohoCRM_create_account(access_token, params):
    """
    Create a new account.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :Account_Name: (str, required) - The name of the account.
    - :Account_Type: (str, optional) - The type of the account.

        (Options: Analyst, Competitor, Customer, Distributor, Integrator, Investor, Partner, Press, Prospect, Reseller, Supplier, Vendor, or any other type)

    - ... (other parameters): Additional parameters that can be included in the params.

    Returns:
      dict: A dictionary containing information about the created account.

    """
    try:
        if "Account_Name" in params and params["Account_Name"]:
            url = f"https://www.zohoapis.com/crm/v5/Accounts"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            paylod = {"data": [data]}
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers, json=paylod)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            if response_json["data"] and "code" in response_json["data"][0] and response_json["data"][0]["code"] != "SUCCESS":
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


def zohoCRM_update_account(access_token, params):
    """
    Update an existing account.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters:

    - :account_id: (str, required) - The ID of the account to be updated.
    - (Additional parameters): Other parameters to be updated, such as Account_Name, Industry, etc.
        
    Returns:
      dict: A dictionary containing information about the updated account.

    """
    try:
        if "account_id" in params and params["account_id"]:
            id = params["account_id"]
            url = f"https://www.zohoapis.com/crm/v5/Accounts/{id}"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            paylod = {"data": [data]}
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.put(url, headers=headers, json=paylod)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            if response_json["data"] and "code" in response_json["data"][0] and response_json["data"][0]["code"] != "SUCCESS":
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


###########################################################################################################################
# Deal Actions


def zohoCRM_list_deals(access_token, params):
    """
    List deals based on specified parameters.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing optional parameters for filtering and pagination:

    - :fields: (str) - Comma-separated list of fields to be retrieved.
    - :converted: (str) - To include only converted deals.

            (Values: 'true' or 'false')

    - :per_page: (int) - Number of deals to be retrieved per page. Default is 200.
    - :sort_by: (str) - Field by which deals should be sorted.

        (Options: id, Created_Time, Modified_Time)

    - :sort_order: (str) - Sorting order, either "asc" or "desc".
    - :include_child: (str) - To include child records.

            (Values: 'true' or 'false')

    - :territory_id: (str) - Filter deals by territory ID.

    Returns:
      dict: A dictionary containing a list of deals retrieved from Zoho CRM.

    """
    try:
        url = f"https://www.zohoapis.com/crm/v5/Deals?"
        fields = "Owner,Description,$currency_symbol,Campaign_Source,$field_states,$review_process,Closing_Date,Reason_For_Loss__s,Last_Activity_Time,Modified_By,$review,Lead_Conversion_Time,$state,$process_flow,Deal_Name,Expected_Revenue,Overall_Sales_Duration,Stage,$locked_for_me,Account_Name,$zia_visions,$approval,Modified_Time,Created_Time,Amount,Next_Step,Probability,$wizard_connection_path,$editable,$orchestration,Contact_Name,Sales_Cycle_Duration,Type,$in_merge,Locked__s,Lead_Source,Created_By,Tag,$zia_owner_assignment,$approval_state,$pathfinder"

        for key, value in params.items():
            if key == "fields":
                fields = value
                continue
            if value:
                url += f"&{key}={value}"

        url += f"&fields={fields}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 204:
            return {"Result": "No Deals Yet!"}
        response_json = response.json()
        if "code" in response_json:
            if response_json["code"] == "UNABLE_TO_PARSE_DATA_TYPE":
                raise Exception("One of the parameters is in wrong format")
            else:
               raise Exception(response_json)
        return {"Deals": response_json["data"]}

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


def zohoCRM_get_deal(access_token, params):
    """
    Retrieve information about a specific deal.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :deal_id: (str, required) - The ID of the deal to be retrieved.

    Returns:
      dict: A dictionary containing the information of the specified deal.

    """
    try:
        if "deal_id" in params and params["deal_id"]:
            id = params["deal_id"]
            url = f"https://www.zohoapis.com/crm/v5/Deals/{id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            return {"Deal": response_json["data"]}

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("ID Not Found")
        else:
            raise Exception(e)


def zohoCRM_delete_deal(access_token, params):
    """
    Delete a deal.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :deal_id: (str, required) - The ID of the deal to be deleted.

    Returns:
      dict: A dictionary containing information about the status of the deletion.

    """
    try:
        if "deal_id" in params and params["deal_id"]:
            id = params["deal_id"]
            url = f"https://www.zohoapis.com/crm/v5/Deals/{id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.delete(url, headers=headers)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("ID Not Found")
        else:
            raise Exception(e)


def zohoCRM_create_deal(access_token, params):
    """
    Create a new deal.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :Deal_Name: (str, required) - The name of the deal.
    - :Stage: (str, required) - The stage of the deal.

        (Options: Qualification, Needs Analysis, Value Proposition, Identify Decision Makers, Proposal/Price Quote, Negotiation/Review, Closed Won, Closed Lost to Competition, or any other stage  )

    - ... (other parameters): Additional parameters that can be included in the params.

    Returns:
      dict: A dictionary containing information about the created deal.

    """
    try:
        if "Deal_Name" in params and params["Deal_Name"] and "Stage" in params and params["Stage"]:
            url = f"https://www.zohoapis.com/crm/v5/Deals"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            paylod = {"data": [data]}
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers, json=paylod)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            if response_json["data"] and "code" in response_json["data"][0] and response_json["data"][0]["code"] != "SUCCESS":
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


def zohoCRM_update_deal(access_token, params):
    """
    Update an existing deal.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters:

    - :deal_id: (str, required) - The ID of the deal to be updated.
    - (Additional parameters): Other parameters to be updated, such as Deal_Name, Stage, etc.
        
    Returns:
      dict: A dictionary containing information about the updated deal.

    """
    try:
        if "deal_id" in params and params["deal_id"]:
            id = params["deal_id"]
            url = f"https://www.zohoapis.com/crm/v5/Deals/{id}"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            paylod = {"data": [data]}
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.put(url, headers=headers, json=paylod)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            if response_json["data"] and "code" in response_json["data"][0] and response_json["data"][0]["code"] != "SUCCESS":
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


###########################################################################################################################
# Lead Actions


def zohoCRM_list_leads(access_token, params):
    """
    List leads based on specified parameters.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing optional parameters for filtering and pagination:

    - :fields: (str) - Comma-separated list of fields to be retrieved.
    - :per_page: (int) - Number of leads to be retrieved per page. Default is 200.
    - :sort_by: (str) - Field by which leads should be sorted.

        (Options: id, Created_Time, Modified_Time)

    - :sort_order: (str) - Sorting order, either "asc" or "desc".
    - :territory_id: (str) - Filter leads by territory ID.

    Returns:
      dict: A dictionary containing a list of leads retrieved from Zoho CRM.

    """
    try:
        url = f"https://www.zohoapis.com/crm/v5/Leads?"
        fields = "Owner,Company,Email,$currency_symbol,$field_states,Last_Activity_Time,Industry,$state,Unsubscribed_Mode,Street,Zip_Code,$approval,Created_Time,$editable,City,No_of_Employees,Converted__s,Converted_Date_Time,Converted_Account,State,Country,Created_By,Annual_Revenue,Secondary_Email,Description,Rating,Website,Twitter,Salutation,First_Name,Full_Name,Lead_Status,Record_Image,Modified_By,Converted_Deal,$review,Lead_Conversion_Time,Skype_ID,Phone,Email_Opt_Out,Designation,Modified_Time,Unsubscribed_Time,Converted_Contact,Mobile,Last_Name,Locked__s,Lead_Source,Tag,Fax"

        for key, value in params.items():
            if key == "fields":
                fields = value
                continue
            if value:
                url += f"&{key}={value}"

        url += f"&fields={fields}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 204:
            return {"Result": "No Leads Yet!"}
        response_json = response.json()
        if "code" in response_json:
            if response_json["code"] == "UNABLE_TO_PARSE_DATA_TYPE":
                raise Exception("One of the parameters is in wrong format")
            else:
               raise Exception(response_json)
        return {"Leads": response_json["data"]}

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


def zohoCRM_get_lead(access_token, params):
    """
    Retrieve information about a specific lead.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :lead_id: (str, required) - The ID of the lead to be retrieved.

    Returns:
      dict: A dictionary containing the information of the specified lead.

    """
    try:
        if "lead_id" in params and params["lead_id"]:
            id = params["lead_id"]
            url = f"https://www.zohoapis.com/crm/v5/Leads/{id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            return {"Lead": response_json["data"]}

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("ID Not Found")
        else:
            raise Exception(e)


def zohoCRM_delete_lead(access_token, params):
    """
    Delete a lead.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :lead_id: (str, required) - The ID of the lead to be deleted.

    Returns:
      dict: A dictionary containing information about the status of the deletion.

    """
    try:
        if "lead_id" in params and params["lead_id"]:
            id = params["lead_id"]
            url = f"https://www.zohoapis.com/crm/v5/Leads/{id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.delete(url, headers=headers)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("ID Not Found")
        else:
            raise Exception(e)


def zohoCRM_create_lead(access_token, params):
    """
    Create a new lead.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :Last_Name: (str, required) - The last name of the lead.
    - :Company: (str, required) - The name of the company associated with the lead.
    - ... (other parameters): Additional parameters that can be included in the params.

    Returns:
      dict: A dictionary containing information about the created lead.

    """
    try:
        if "Last_Name" in params and params["Last_Name"] and "Company" in params and params["Company"]:
            url = f"https://www.zohoapis.com/crm/v5/Leads"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            paylod = {"data": [data]}
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers, json=paylod)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            if response_json["data"] and "code" in response_json["data"][0] and response_json["data"][0]["code"] != "SUCCESS":
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


def zohoCRM_update_lead(access_token, params):
    """
    Update an existing lead.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters:

    - :lead_id: (str, required) - The ID of the lead to be updated.
    - (Additional parameters): Other parameters to be updated, such as Last_Name, Company, etc.
        
    Returns:
      dict: A dictionary containing information about the updated lead.

    """
    try:
        if "lead_id" in params and params["lead_id"]:
            id = params["lead_id"]
            url = f"https://www.zohoapis.com/crm/v5/Leads/{id}"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            paylod = {"data": [data]}
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.put(url, headers=headers, json=paylod)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            if response_json["data"] and "code" in response_json["data"][0] and response_json["data"][0]["code"] != "SUCCESS":
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


###########################################################################################################################
# Product Actions


def zohoCRM_list_products(access_token, params):
    """
    List products based on specified parameters.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing optional parameters for filtering and pagination:

    - :fields: (str) - Comma-separated list of fields to be retrieved.
    - :converted: (str) - To include only converted products.

            (Values: 'true' or 'false')

    - :per_page: (int) - Number of products to be retrieved per page. Default is 200.
    - :sort_by: (str) - Field by which products should be sorted.

        (Options: id, Created_Time, Modified_Time)

    - :sort_order: (str) - Sorting order, either "asc" or "desc".
    - :include_child: (str) - To include child records.

            (Values: 'true' or 'false')

    Returns:
      dict: A dictionary containing a list of products retrieved from Zoho CRM.

    """
    try:
        url = f"https://www.zohoapis.com/crm/v5/Products?"
        fields = "Product_Category,Qty_in_Demand,Owner,Description,Vendor_Name,Sales_Start_Date,Tax,Product_Active,Record_Image,Modified_By,Product_Code,Manufacturer,Support_Expiry_Date,$approval,Modified_Time,Created_Time,Commission_Rate,Product_Name,Handler,Support_Start_Date,Usage_Unit,Qty_Ordered,Qty_in_Stock,Created_By,Tag,Sales_End_Date,Unit_Price,Taxable,Reorder_Level,$currency_symbol,$review_process,$sharing_permission,$state,$approval_state"

        for key, value in params.items():
            if key == "fields":
                fields = value
                continue
            if value:
                url += f"&{key}={value}"

        url += f"&fields={fields}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 204:
            return {"Result": "No Products Yet!"}
        response_json = response.json()
        if "code" in response_json:
            if response_json["code"] == "UNABLE_TO_PARSE_DATA_TYPE":
                raise Exception("One of the parameters is in wrong format")
            else:
               raise Exception(response_json)
        return {"Products": response_json["data"]}

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


def zohoCRM_get_product(access_token, params):
    """
    Retrieve information about a specific product.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :product_id: (str, required) - The ID of the product to be retrieved.

    Returns:
      dict: A dictionary containing the information of the specified product.

    """
    try:
        if "product_id" in params and params["product_id"]:
            id = params["product_id"]
            url = f"https://www.zohoapis.com/crm/v5/Products/{id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            return {"Product": response_json["data"]}

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("ID Not Found")
        else:
            raise Exception(e)


def zohoCRM_delete_product(access_token, params):
    """
    Delete a product.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :product_id: (str, required) - The ID of the product to be deleted.

    Returns:
      dict: A dictionary containing information about the status of the deletion.

    """
    try:
        if "product_id" in params and params["product_id"]:
            id = params["product_id"]
            url = f"https://www.zohoapis.com/crm/v5/Products/{id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.delete(url, headers=headers)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("ID Not Found")
        else:
            raise Exception(e)


def zohoCRM_create_product(access_token, params):
    """
    Create a new product.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :Product_Name: (str, required) - The name of the product.
    - ... (other parameters): Additional parameters that can be included in the params.

    Returns:
      dict: A dictionary containing information about the created product.

    """
    try:
        if "Product_Name" in params and params["Product_Name"]:
            url = f"https://www.zohoapis.com/crm/v5/Products"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            paylod = {"data": [data]}
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers, json=paylod)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            if response_json["data"] and "code" in response_json["data"][0] and response_json["data"][0]["code"] != "SUCCESS":
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


def zohoCRM_update_product(access_token, params):
    """
    Update an existing product.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters:

    - :product_id: (str, required) - The ID of the product to be updated.
    - (Additional parameters): Other parameters to be updated, such as Product_Name, Unit_Price, etc.
        
    Returns:
      dict: A dictionary containing information about the updated product.

    """
    try:
        if "product_id" in params and params["product_id"]:
            id = params["product_id"]
            url = f"https://www.zohoapis.com/crm/v5/Products/{id}"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            paylod = {"data": [data]}
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.put(url, headers=headers, json=paylod)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            if response_json["data"] and "code" in response_json["data"][0] and response_json["data"][0]["code"] != "SUCCESS":
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


###########################################################################################################################
# Purchase Order Actions


def zohoCRM_list_purchase_orders(access_token, params):
    """
    List purchase orders based on specified parameters.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing optional parameters for filtering and pagination:

    - :fields: (str) - Comma-separated list of fields to be retrieved.
    - :converted: (str) - To include only converted purchase orders.

            (Values: 'true' or 'false')

    - :per_page: (int) - Number of purchase orders to be retrieved per page. Default is 200.
    - :sort_by: (str) - Field by which purchase orders should be sorted.

        (Options: id, Created_Time, Modified_Time)

    - :sort_order: (str) - Sorting order, either "asc" or "desc".
    - :include_child: (str) - To include child records.

            (Values: 'true' or 'false')

    Returns:
      dict: A dictionary containing a list of purchase orders retrieved from Zoho CRM.

    """
    try:
        url = f"https://www.zohoapis.com/crm/v5/Purchase_Orders?"
        fields = "Owner,Tax,PO_Date,Billing_Country,Carrier,Status,Grand_Total,$approval,PO_Number,Billing_Street,Adjustment,Created_Time,Billing_Code,Tracking_Number,Excise_Duty,Shipping_City,Shipping_Country,Shipping_Code,Billing_City,Requisition_No,Created_By,Shipping_Street,Description,Discount,Vendor_Name,Shipping_State,Modified_By,Purchase_Items,Sales_Commission,Modified_Time,Due_Date,Terms_and_Conditions,Sub_Total,Subject,Contact_Name,Locked__s,Billing_State,Tag"

        for key, value in params.items():
            if key == "fields":
                fields = value
                continue
            if value:
                url += f"&{key}={value}"

        url += f"&fields={fields}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 204:
            return {"Result": "No Purchase Orders Yet!"}
        response_json = response.json()
        if "code" in response_json:
            if response_json["code"] == "UNABLE_TO_PARSE_DATA_TYPE":
                raise Exception("One of the parameters is in wrong format")
            else:
               raise Exception(response_json)
        return {"Purchase Orders": response_json["data"]}

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


def zohoCRM_get_purchase_order(access_token, params):
    """
    Retrieve information about a specific purchase order.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :purchase_order_id: (str, required) - The ID of the purchase order to be retrieved.

    Returns:
      dict: A dictionary containing the information of the specified purchase order.

    """
    try:
        if "purchase_order_id" in params and params["purchase_order_id"]:
            id = params["purchase_order_id"]
            url = f"https://www.zohoapis.com/crm/v5/Purchase_Orders/{id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            return {"Purchase Order": response_json["data"]}

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("ID Not Found")
        else:
            raise Exception(e)


def zohoCRM_delete_purchase_order(access_token, params):
    """
    Delete a purchase order.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :purchase_order_id: (str, required) - The ID of the purchase order to be deleted.

    Returns:
      dict: A dictionary containing information about the status of the deletion.

    """
    try:
        if "purchase_order_id" in params and params["purchase_order_id"]:
            id = params["purchase_order_id"]
            url = f"https://www.zohoapis.com/crm/v5/Purchase_Orders/{id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.delete(url, headers=headers)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("ID Not Found")
        else:
            raise Exception(e)


def zohoCRM_create_purchase_order(access_token, params):
    """
    Create a new purchase order.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :Subject: (str, required) - The subject of the purchase order.
    - :Vendor_Name: (dict, required) - The vendor information, including the vendor ID.
    - :Purchase_Items: (list of dict, required) - A list of purchase items, each containing product details.

            - :Product_Name: (dict, required) - The product information, including the product ID.
            - (Additional fields): Other optional fields for the purchase item, such as List_Price, Description, etc.
            
    - :Status: (str, optional) - The status of the purchase order.

        (Options: Created, Approved, Delivered, Cancelled)

    - ... (other parameters): Additional parameters that can be included in the params.

    Returns:
      dict: A dictionary containing information about the created purchase order.

    """
    try:
        if "Subject" in params and params["Subject"] and "Vendor_Name" in params and params["Vendor_Name"] and "Purchase_Items" in params and params["Purchase_Items"]:
            url = f"https://www.zohoapis.com/crm/v5/Purchase_Orders"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            paylod = {"data": [data]}
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers, json=paylod)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            if response_json["data"] and "code" in response_json["data"][0] and response_json["data"][0]["code"] != "SUCCESS":
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


def zohoCRM_update_purchase_order(access_token, params):
    """
    Update an existing purchase order.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters:

    - :purchase_order_id: (str, required) - The ID of the purchase order to be updated.
    - (Additional parameters): Other parameters to be updated, such as Subject, Vendor_Name, etc.
        
    Returns:
      dict: A dictionary containing information about the updated purchase order.

    """
    try:
        if "purchase_order_id" in params and params["purchase_order_id"]:
            id = params["purchase_order_id"]
            url = f"https://www.zohoapis.com/crm/v5/Purchase_Orders/{id}"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            paylod = {"data": [data]}
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.put(url, headers=headers, json=paylod)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            if response_json["data"] and "code" in response_json["data"][0] and response_json["data"][0]["code"] != "SUCCESS":
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


###########################################################################################################################
# Quote Actions


def zohoCRM_list_quotes(access_token, params):
    """
    List quotes based on specified parameters.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing optional parameters for filtering and pagination:

    - :fields: (str) - Comma-separated list of fields to be retrieved.
    - :per_page: (int) - Number of quotes to be retrieved per page. Default is 200.
    - :sort_by: (str) - Field by which quotes should be sorted.

        (Options: id, Created_Time, Modified_Time)

    - :sort_order: (str) - Sorting order, either "asc" or "desc".

    Returns:
      dict: A dictionary containing a list of quotes retrieved from Zoho CRM.

    """
    try:
        url = f"https://www.zohoapis.com/crm/v5/Quotes?"
        fields = "Owner,Tax,Deal_Name,Billing_Country,Carrier,Grand_Total,Billing_Street,Adjustment,Created_Time,Billing_Code,Shipping_City,Shipping_Country,Shipping_Code,Billing_City,Quote_Number,Created_By,Shipping_Street,Description,Discount,Shipping_State,Modified_By,Valid_Till,Team,Account_Name,Quote_Stage,Modified_Time,Terms_and_Conditions,Sub_Total,Subject,Contact_Name,Locked__s,Billing_State,Tag"

        for key, value in params.items():
            if key == "fields":
                fields = value
                continue
            if value:
                url += f"&{key}={value}"

        url += f"&fields={fields}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 204:
            return {"Result": "No Quotes Yet!"}
        response_json = response.json()
        if "code" in response_json:
            if response_json["code"] == "UNABLE_TO_PARSE_DATA_TYPE":
                raise Exception("One of the parameters is in wrong format")
            else:
               raise Exception(response_json)
        return {"Quotes": response_json["data"]}

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


def zohoCRM_get_quote(access_token, params):
    """
    Retrieve information about a specific quote.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :quote_id: (str, required) - The ID of the quote to be retrieved.

    Returns:
      dict: A dictionary containing the information of the specified quote.

    """
    try:
        if "quote_id" in params and params["quote_id"]:
            id = params["quote_id"]
            url = f"https://www.zohoapis.com/crm/v5/Quotes/{id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            return {"Quote": response_json["data"]}

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("ID Not Found")
        else:
            raise Exception(e)


def zohoCRM_delete_quote(access_token, params):
    """
    Delete a quote.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :quote_id: (str, required) - The ID of the quote to be deleted.

    Returns:
      dict: A dictionary containing information about the status of the deletion.

    """
    try:
        if "quote_id" in params and params["quote_id"]:
            id = params["quote_id"]
            url = f"https://www.zohoapis.com/crm/v5/Quotes/{id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.delete(url, headers=headers)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("ID Not Found")
        else:
            raise Exception(e)


def zohoCRM_create_quote(access_token, params):
    """
    Create a new quote.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :Subject: (str, required) - The subject of the quote.
    - :Quoted_Items: (list of dict, required) - A list of quoted items, each containing product details.

        - :Product_Name: (dict, required) - The product information, including the product ID.
        - (Additional fields): Other optional fields for the quoted item, such as Description, Quantity, Tax, etc.

    - :Quote_Stage: (str, optional) - The stage of the quote.

        (Options: Draft, Negotiation, Delivered, On Hold, Confirmed, Closed Won, Closed Lost)

    - ... (other parameters): Additional parameters that can be included in the params.

    Returns:
      dict: A dictionary containing information about the created quote.

    """
    try:
        if "Subject" in params and params["Subject"] and "Quoted_Items" in params and params["Quoted_Items"]:
            url = f"https://www.zohoapis.com/crm/v5/Quotes"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            paylod = {"data": [data]}
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers, json=paylod)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            if response_json["data"] and "code" in response_json["data"][0] and response_json["data"][0]["code"] != "SUCCESS":
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


def zohoCRM_update_quote(access_token, params):
    """
    Update an existing quote.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters:

    - :quote_id: (str, required) - The ID of the quote to be updated.
    - (Additional parameters): Other parameters to be updated, such as Subject, Billing_Address, etc.
        
    Returns:
      dict: A dictionary containing information about the updated quote.

    """
    try:
        if "quote_id" in params and params["quote_id"]:
            id = params["quote_id"]
            url = f"https://www.zohoapis.com/crm/v5/Quotes/{id}"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            paylod = {"data": [data]}
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.put(url, headers=headers, json=paylod)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            if response_json["data"] and "code" in response_json["data"][0] and response_json["data"][0]["code"] != "SUCCESS":
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


###########################################################################################################################
# Sales Order Actions


def zohoCRM_list_sales_orders(access_token, params):
    """
    List sales orders based on specified parameters.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing optional parameters for filtering and pagination:

    - :fields: (str) - Comma-separated list of fields to be retrieved.
    - :per_page: (int) - Number of sales orders to be retrieved per page. Default is 200.
    - :sort_by: (str) - Field by which sales orders should be sorted.

        (Options: id, Created_Time, Modified_Time)

    - :sort_order: (str) - Sorting order, either "asc" or "desc".

    Returns:
      dict: A dictionary containing a list of sales orders retrieved from Zoho CRM.

    """
    try:
        url = f"https://www.zohoapis.com/crm/v5/Sales_Orders?"
        fields = "Owner,Customer_No,Tax,Deal_Name,Billing_Country,Carrier,Quote_Name,Status,Grand_Total,Billing_Street,Adjustment,Created_Time,Billing_Code,Excise_Duty,Shipping_City,Shipping_Country,Shipping_Code,Billing_City,Purchase_Order,Created_By,Shipping_Street,Description,Discount,Shipping_State,Modified_By,Account_Name,Sales_Commission,Modified_Time,Due_Date,Terms_and_Conditions,Sub_Total,Subject,Contact_Name,SO_Number,Locked__s,Billing_State,Tag,Pending"

        for key, value in params.items():
            if key == "fields":
                fields = value
                continue
            if value:
                url += f"&{key}={value}"

        url += f"&fields={fields}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 204:
            return {"Result": "No Sales Orders Yet!"}
        response_json = response.json()
        if "code" in response_json:
            if response_json["code"] == "UNABLE_TO_PARSE_DATA_TYPE":
                raise Exception("One of the parameters is in wrong format")
            else:
               raise Exception(response_json)
        return {"Sales Orders": response_json["data"]}

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


def zohoCRM_get_sales_order(access_token, params):
    """
    Retrieve information about a specific sales order.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :sales_order_id: (str, required) - The ID of the sales order to be retrieved.

    Returns:
      dict: A dictionary containing the information of the specified sales order.

    """
    try:
        if "sales_order_id" in params and params["sales_order_id"]:
            id = params["sales_order_id"]
            url = f"https://www.zohoapis.com/crm/v5/Sales_Orders/{id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            return {"Sales Order": response_json["data"]}

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("ID Not Found")
        else:
            raise Exception(e)


def zohoCRM_delete_sales_order(access_token, params):
    """
    Delete a sales order.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :sales_order_id: (str, required) - The ID of the sales order to be deleted.

    Returns:
      dict: A dictionary containing information about the status of the deletion.

    """
    try:
        if "sales_order_id" in params and params["sales_order_id"]:
            id = params["sales_order_id"]
            url = f"https://www.zohoapis.com/crm/v5/Sales_Orders/{id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.delete(url, headers=headers)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("ID Not Found")
        else:
            raise Exception(e)


def zohoCRM_create_sales_order(access_token, params):
    """
    Create a new sales order.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :Subject: (str, required) - The subject of the sales order.
    - :Ordered_Items: (list of dict, required) - A list of ordered items, each containing product details.

        - :Product_Name: (dict, required) - The product information, including the product ID.
        - (Additional fields): Other optional fields for the ordered item, such as Description, Quantity, Tax, etc.
            
    - :Status: (str, optional) - The status of the sales order.

        (Options: Created, Approved, Delivered, Cancelled)

    - ... (other parameters): Additional parameters that can be included in the params.

    Returns:
      dict: A dictionary containing information about the created sales order.

    """
    try:
        if "Subject" in params and params["Subject"] and "Ordered_Items" in params and params["Ordered_Items"]:
            url = f"https://www.zohoapis.com/crm/v5/Sales_Orders"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            paylod = {"data": [data]}
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers, json=paylod)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            if response_json["data"] and "code" in response_json["data"][0] and response_json["data"][0]["code"] != "SUCCESS":
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


def zohoCRM_update_sales_order(access_token, params):
    """
    Update an existing sales order.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters:

    - :sales_order_id: (str, required) - The ID of the sales order to be updated.
    - (Additional parameters): Other parameters to be updated, such as Subject, Adjustment, etc.
        
    Returns:
      dict: A dictionary containing information about the updated sales order.

    """
    try:
        if "sales_order_id" in params and params["sales_order_id"]:
            id = params["sales_order_id"]
            url = f"https://www.zohoapis.com/crm/v5/Sales_Orders/{id}"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            paylod = {"data": [data]}
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.put(url, headers=headers, json=paylod)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            if response_json["data"] and "code" in response_json["data"][0] and response_json["data"][0]["code"] != "SUCCESS":
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


###########################################################################################################################
# Vendor Actions


def zohoCRM_list_vendors(access_token, params):
    """
    List vendors based on specified parameters.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing optional parameters for filtering and pagination:

    - :fields: (str) - Comma-separated list of fields to be retrieved.
    - :converted: (str) - To include only converted vendors.

            (Values: 'true' or 'false')

    - :per_page: (int) - Number of vendors to be retrieved per page. Default is 200.
    - :sort_by: (str) - Field by which vendors should be sorted.

        (Options: id, Created_Time, Modified_Time)

    - :sort_order: (str) - Sorting order, either "asc" or "desc".
    - :include_child: (str) - To include child records.

            (Values: 'true' or 'false')

    Returns:
      dict: A dictionary containing a list of vendors retrieved from Zoho CRM.

    """
    try:
        url = f"https://www.zohoapis.com/crm/v5/Vendors?"
        fields = "Owner,Email,Category,Description,Vendor_Name,Website,Record_Image,Modified_By,Phone,Street,Zip_Code,Modified_Time,Created_Time,City,State,GL_Account,Locked__s,Country,Created_By,Tag"

        for key, value in params.items():
            if key == "fields":
                fields = value
                continue
            if value:
                url += f"&{key}={value}"

        url += f"&fields={fields}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 204:
            return {"Result": "No Vendors Yet!"}
        response_json = response.json()
        if "code" in response_json:
            if response_json["code"] == "UNABLE_TO_PARSE_DATA_TYPE":
                raise Exception("One of the parameters is in wrong format")
            else:
               raise Exception(response_json)
        return {"Vendors": response_json["data"]}

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


def zohoCRM_get_vendor(access_token, params):
    """
    Retrieve information about a specific vendor.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :vendor_id: (str, required) - The ID of the vendor to be retrieved.

    Returns:
      dict: A dictionary containing the information of the specified vendor.

    """
    try:
        if "vendor_id" in params and params["vendor_id"]:
            id = params["vendor_id"]
            url = f"https://www.zohoapis.com/crm/v5/Vendors/{id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            return {"Vendor": response_json["data"]}

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("ID Not Found")
        else:
            raise Exception(e)


def zohoCRM_delete_vendor(access_token, params):
    """
    Delete a vendor.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :vendor_id: (str, required) - The ID of the vendor to be deleted.

    Returns:
      dict: A dictionary containing information about the status of the deletion.

    """
    try:
        if "vendor_id" in params and params["vendor_id"]:
            id = params["vendor_id"]
            url = f"https://www.zohoapis.com/crm/v5/Vendors/{id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.delete(url, headers=headers)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("ID Not Found")
        else:
            raise Exception(e)


def zohoCRM_create_vendor(access_token, params):
    """
    Create a new vendor.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :Vendor_Name: (str, required) - The name of the vendor.
    - ... (other parameters): Additional parameters that can be included in the params.

    Returns:
      dict: A dictionary containing information about the created vendor.

    """
    try:
        if "Vendor_Name" in params and params["Vendor_Name"]:
            url = f"https://www.zohoapis.com/crm/v5/Vendors"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            paylod = {"data": [data]}
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers, json=paylod)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            if response_json["data"] and "code" in response_json["data"][0] and response_json["data"][0]["code"] != "SUCCESS":
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


def zohoCRM_update_vendor(access_token, params):
    """
    Update an existing vendor.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters:

    - :vendor_id: (str, required) - The ID of the vendor to be updated.
    - (Additional parameters): Other parameters to be updated, such as Vendor_Name, Address, Category, etc.
        
    Returns:
      dict: A dictionary containing information about the updated vendor.

    """
    try:
        if "vendor_id" in params and params["vendor_id"]:
            id = params["vendor_id"]
            url = f"https://www.zohoapis.com/crm/v5/Vendors/{id}"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            paylod = {"data": [data]}
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.put(url, headers=headers, json=paylod)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            if response_json["data"] and "code" in response_json["data"][0] and response_json["data"][0]["code"] != "SUCCESS":
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


###########################################################################################################################
# Invoice Actions


def zohoCRM_list_invoices(access_token, params):
    """
    List invoices based on specified parameters.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing optional parameters for filtering and pagination:

    - :fields: (str) - Comma-separated list of fields to be retrieved.
    - :converted: (str) - To include only converted invoices.

            (Values: 'true' or 'false')

    - :per_page: (int) - Number of invoices to be retrieved per page. Default is 200.
    - :sort_by: (str) - Field by which invoices should be sorted.

        (Options: id, Created_Time, Modified_Time)

    - :sort_order: (str) - Sorting order, either "asc" or "desc".
    - :include_child: (str) - To include child records.

            (Values: 'true' or 'false')

    Returns:
      dict: A dictionary containing a list of invoices retrieved from Zoho CRM.

    """
    try:
        url = f"https://www.zohoapis.com/crm/v5/Invoices?"
        fields = "Owner,Tax,Billing_Country,Status,Grand_Total,Billing_Street,Adjustment,Created_Time,Billing_Code,Excise_Duty,Shipping_City,Shipping_Country,Shipping_Code,Billing_City,Purchase_Order,Created_By,Shipping_Street,Description,Discount,Shipping_State,Invoice_Date,Modified_By,Account_Name,Sales_Order,Deal_Name__s,Sales_Commission,Modified_Time,Due_Date,Terms_and_Conditions,Sub_Total,Invoice_Number,Subject,Contact_Name,Locked__s,Billing_State,Tag"

        for key, value in params.items():
            if key == "fields":
                fields = value
                continue
            if value:
                url += f"&{key}={value}"

        url += f"&fields={fields}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 204:
            return {"Result": "No Invoices Yet!"}
        response_json = response.json()
        if "code" in response_json:
            if response_json["code"] == "UNABLE_TO_PARSE_DATA_TYPE":
                raise Exception("One of the parameters is in wrong format")
            else:
               raise Exception(response_json)
        return {"Invoices": response_json["data"]}

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


def zohoCRM_get_invoice(access_token, params):
    """
    Retrieve information about a specific invoice.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :invoice_id: (str, required) - The ID of the invoice to be retrieved.

    Returns:
      dict: A dictionary containing the information of the specified invoice.

    """
    try:
        if "invoice_id" in params and params["invoice_id"]:
            id = params["invoice_id"]
            url = f"https://www.zohoapis.com/crm/v5/Invoices/{id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            return {"Invoice": response_json["data"]}

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("ID Not Found")
        else:
            raise Exception(e)


def zohoCRM_delete_invoice(access_token, params):
    """
    Delete an invoice.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :invoice_id: (str, required) - The ID of the invoice to be deleted.

    Returns:
      dict: A dictionary containing information about the status of the deletion.

    """
    try:
        if "invoice_id" in params and params["invoice_id"]:
            id = params["invoice_id"]
            url = f"https://www.zohoapis.com/crm/v5/Invoices/{id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.delete(url, headers=headers)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("ID Not Found")
        else:
            raise Exception(e)


def zohoCRM_create_invoice(access_token, params):
    """
    Create a new invoice.

    :access_token: The Zoho CRM access token for authentication..
    :params: A dictionary containing parameters:

    - :Subject: (str, required) - The subject of the invoice.
    - :Invoiced_Items: (list of dict, required) - A list of invoiced items, each containing product details.

        - :Product_Name: (dict, required) - The product information, including the product ID.
        - (Additional fields): Other optional fields for the invoiced item, such as Quantity, Tax, Net_Total, etc.
            
    - ... (other parameters): Additional parameters that can be included in the params.

    Returns:
      dict: A dictionary containing information about the created invoice.

    """
    try:
        if "Subject" in params and params["Subject"] and "Invoiced_Items" in params and params["Invoiced_Items"]:
            url = f"https://www.zohoapis.com/crm/v5/Invoices"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            paylod = {"data": [data]}
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers, json=paylod)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            if response_json["data"] and "code" in response_json["data"][0] and response_json["data"][0]["code"] != "SUCCESS":
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)


def zohoCRM_update_invoice(access_token, params):
    """
    Update an existing invoice.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters:

    - :invoice_id: (str, required) - The ID of the invoice to be updated.
    - (Additional parameters): Other parameters to be updated, such as Subject, Account_Name, etc.
        
    Returns:
      dict: A dictionary containing information about the updated invoice.

    """
    try:
        if "invoice_id" in params and params["invoice_id"]:
            id = params["invoice_id"]
            url = f"https://www.zohoapis.com/crm/v5/Invoices/{id}"
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            paylod = {"data": [data]}
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.put(url, headers=headers, json=paylod)
            response_json = response.json()
            if "code" in response_json and response_json["code"] != 0:
                raise Exception(response_json)
            if response_json["data"] and "code" in response_json["data"][0] and response_json["data"][0]["code"] != "SUCCESS":
                raise Exception(response_json)
            return response_json

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Base URL")
        else:
            raise Exception(e)