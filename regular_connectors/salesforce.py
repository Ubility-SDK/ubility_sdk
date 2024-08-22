import requests
import base64
import json

######################     UI      ######################

# def salesforce_generate_code(creds,token):
#     """
#     Generate the Salesforce OAuth 2.0 authorization URL for obtaining an access token.

#     :domain: The Salesforce domain.
#     :client_id: The client ID associated with the connected app.

#     Returns:
#       str: The Salesforce OAuth 2.0 authorization URL with the necessary parameters for code retrieval.

#     """
#     try: 
# cred=json.loads(creds)        
# domain=cred['domainName']
#         client_id=['clientID']
#         url = f"https://{domain}.my.salesforce.com/services/oauth2/authorize?client_id={client_id}&code_challenge=V7R2SXbfwXn4A1v1TV81GFenhIbLv6VrRLuHfx04jgQ&redirect_uri=https://ziwo-test.ubilityai.com/admin/credentials&response_type=code&code_challenge_method=S256&grant_type=authorization_code$scope=full refresh_token offline_access profile"
#         return url

#     except Exception as error:
#         raise Exception(error)


# def salesforce_generate_refresh_token(domain,client_id, client_secret, code):
#     """
#     Obtain a Salesforce refresh token using the authorization code.

#     :domain: The Salesforce domain.
#     :client_id: The client ID associated with the connected app.
#     :client_secret: The client Secret associated with the connected app.
#     :code: The authorization code obtained during the initial OAuth 2.0 authorization.

#     Returns:
#       str: The Salesforce refresh token.

#     """
#     try:
#         url = f"https://{domain}.my.salesforce.com/services/oauth2/token?grant_type=authorization_code&code={code}&client_id={client_id}&client_secret={client_secret}&redirect_uri=https://ziwo-test.ubilityai.com/admin/credentials&code_verifier=A00F0D6C54EBCCBC3F5CA84771F43B2C79F503E8D560E7DC9003CE96CFE704D1"
#         response = requests.post(url)
#         response_json = response.json()
#         if "refresh_token" in response_json:
#             return response_json["refresh_token"]
#         else:
#             raise Exception({"refresh_token": "Invalid refresh_token"})

#     except Exception as error:
#         raise Exception(error)

######################    Generate Access Token      ######################

def salesforce_refresh_access_token(creds):
    """
    Refresh the Salesforce access token using the provided refresh token.

    :client_id: The client ID associated with the connected app.
    :client_secret: The client Secret associated with the connected app.
    :refresh_token: The refresh token obtained during the initial OAuth 2.0 authorization.

    Returns:
      str: The refreshed Salesforce access token.

    """
    try:
        cred=json.loads(creds)
        client_id=cred['clientID']
        client_secret=cred['clientSecret']
        refresh_token=cred['refreshToken']
        url = f"https://login.salesforce.com/services/oauth2/token?grant_type=refresh_token&client_id={client_id}&client_secret={client_secret}&refresh_token={refresh_token}"
        response = requests.post(url)
        response_json = response.json()
        if "access_token" in response_json:
            return response_json["access_token"]
        else:
            return {"access_token": "Invalid access_token"}

    except Exception as error:
        raise Exception(error)
    
    
###########################################################################

# User Actions


def salesforce_get_user(creds,token, params):
    """
    Retrieve information about a Salesforce user.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :id: (str, required) - The ID of the Salesforce user to be retrieved.

    Returns:
      dict: A dictionary containing information about the Salesforce user.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/User/"
        if "id" in params:
            access_token = token
            user_id = params["id"]
            url += f"{user_id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            result = response.json()
            if type(result) == list:
                for item in result[0]:
                    if item == "errorCode":
                        raise Exception(result)
                return result
            else:
                for item in result:
                    if item == "errorCode":
                        raise Exception(result)
                return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_list_users(creds,token, params):
    """
    Retrieve a list of Salesforce users based on the provided parameters.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :fields: (str, optional) - Comma-separated fields to be included in the SELECT query.
    - :conditions: (list of strings, optional) - list of conditions to filter the query results.

    Returns:
      dict: A dictionary containing information about the Salesforce users that match the query.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/query?q="
        access_token = token
        query = "SELECT Id, name, Email FROM User"
        conditions = ""
        for key, value in params.items():
            if key == "fields":
                query = f"SELECT {value} FROM User"

            if key == "conditions":
                conditions = " AND ".join(value)
                conditions = " WHERE " + conditions

        url += query + conditions
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        result = response.json()
        if type(result) == list:
            for item in result[0]:
                if item == "errorCode":
                    raise Exception(result)
            return result
        else:
            for item in result:
                if item == "errorCode":
                    raise Exception(result)
            return result

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


###########################################################################

# Task Actions


def salesforce_get_task(creds,token, params):
    """
    Retrieve information about a Salesforce task.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :id: (str, required) - The ID of the Salesforce task to be retrieved.

    Returns:
      dict: A dictionary containing information about the Salesforce task.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Task/"
        if "id" in params:
            access_token = token
            task_id = params["id"]
            url += f"{task_id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            result = response.json()
            if type(result) == list:
                for item in result[0]:
                    if item == "errorCode":
                        raise Exception(result)
                return result
            else:
                for item in result:
                    if item == "errorCode":
                        raise Exception(result)
                return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_get_task_summary(creds,token):
    """
    Retrieve a summary of Salesforce Task.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.

    Returns:
      dict: A dictionary containing summary information about Salesforce Task.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Task"
        access_token = token
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        result = response.json()
        if type(result) == list:
            for item in result[0]:
                if item == "errorCode":
                    raise Exception(result)
            return result
        else:
            for item in result:
                if item == "errorCode":
                    raise Exception(result)
            return result

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_list_tasks(creds,token, params):
    """
    Retrieve a list of Salesforce tasks based on the provided parameters.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :fields: (str, optional) - Comma-separated fields to be included in the SELECT query.
    - :conditions: (list of strings, optional) - list of conditions to filter the query results.

    Returns:
      dict: A dictionary containing information about the Salesforce tasks that match the query.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/query?q="

        access_token = token
        query = "SELECT Id, Subject, Status, Priority FROM Task"
        conditions = ""
        for key, value in params.items():
            if key == "fields":
                query = f"SELECT {value} FROM Task"

            if key == "conditions":
                conditions = " AND ".join(value)
                conditions = " WHERE " + conditions

        url += query + conditions

        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        result = response.json()
        if type(result) == list:
            for item in result[0]:
                if item == "errorCode":
                    raise Exception(result)
            return result
        else:
            for item in result:
                if item == "errorCode":
                    raise Exception(result)
            return result

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_create_task(creds,token, params):
    """
    Create a new task in Salesforce.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :status: (str, required) - Task status.

            (Options: Completed, Deferred, In Progress, Not Started, Waiting on someone else, or any other status)

    - :activityDate: (str, optional) - The date of the activity.
    
            (Format: YYYY-MM-DD)

    - :priority: (str, optional) - Task priority.

            (Options: High, Low, Normal)

    - :ownerId: (str, optional) - The ID of the user who owns the task.
    - :description: (str, optional) - Task description.
    - :callDurationInSeconds: (int, optional) - The duration of a call in seconds.
    - :callType: (str, optional) - The type of call.

            (Options: Inbound, Internal, Outbound)

    - :callDisposition: (str, optional) - The outcome of a call.
    - :callObject: (str, optional) - The object of a call.
    - :reminderDateTime: (str, optional) - The date and time when a reminder is set for the task.
    
            (Format: YYYY-MM-DDTHH:mm:ss.SSSZ)

    - :isReminderSet: (bool, optional) - Indicates whether a reminder is set for the task.
    - :recurrenceInterval: (int, optional) - The interval between recurring tasks.
    - :recurrenceRegeneratedType: (str, optional) - The type of recurrence regeneration.

            (Options: RecurrenceRegenerateAfterDueDate, RecurrenceRegenerateAfterToday, RecurrenceRegenerated)

    - :subject: (str, optional) - The type of task.

            (Options: Call, Email, Send Letter, Send Quote, or any other status)

    - :taskSubtype: (str, optional) - The subtype of the task.

            (Options: Cadence, Call, Email, LinkedIn, List Email, Task)
            (Note: If 'Cadence' is selected, the subject cannot be added)

    - :whoId: (str, optional) - The ID of the contact or lead who is related to the task.
    - :whatId: (str, optional) - The ID of the related record.
    - :recurrenceDayOfWeekMask: (int, optional) - The bitmask of days of the week when a recurring task repeats.

            (Options: 1 (Sunday), 2 (Monday), 4 (Tuesday), 8 (Wednesday), 16 (Thursday), 32 (Friday), 64 (Saturday))
            (e.g: To set the task to recur on Monday(2) and Wednesday(8), recurrenceDayOfWeekMask=10 --> '2+8')
    
    
    - :recurrenceDayOfMonth: (int, optional) - The day of the month when a recurring task repeats.
    - :recurrenceInstance: (str, optional) - The instance in the month when a recurring task repeats.

            (Options: 1st, 2nd, 3rd, 4th, last)

    - :recurrenceMonthOfYear: (str, optional) - The month of the year when a recurring task repeats.

            (Options: January, February, ..., December)

    - :recurrenceStartDateOnly: (str, optional) - The start date of recurrence.

            (Format: YYYY-MM-DD)

    - :recurrenceEndDateOnly: (str, optional) - The end date of recurrence.

            (Format: YYYY-MM-DD)

    - :recurrenceTimeZoneSidKey: (str, optional) - The time zone for recurring tasks.
    - :recurrenceType: (str, optional) - The type of recurrence pattern.

            (Options: RecursDaily, RecursEveryWeekday, RecursMonthly, RecursMonthlyNth, RecursWeekly, RecursYearly, RecursYearlyNth)

    Returns:
      dict: The JSON response containing information about the created Task.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Task"
        if "status" in params:
            access_token = token
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value

            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            if type(result) == list:
                for item in result[0]:
                    if item == "errorCode":
                        raise Exception(result)
                return result
            else:
                for item in result:
                    if item == "errorCode":
                        raise Exception(result)
                return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_update_task(creds,token, params):
    """
    Update a task in Salesforce.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :id: (str, required) - The ID of the Task to be updated.
    - Additional optional parameters based on task type (same parameters in create task).
        
    Returns:
      dict: The JSON response containing information about the updated Task.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Task/"
        if "id" in params:
            access_token = token
            task_id = params["id"]
            url += f"{task_id}"
            data = {}
            for key, value in params.items():
                if key == "id":
                    continue
                if value:
                    data[key] = value

            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.patch(url, headers=headers, json=data)
            if response.status_code == 204:
                return {"Result": f"Updated Task ID: {task_id}"}
            else:
                if response.content:
                    result = response.json()
                    if type(result) == list:
                        for item in result[0]:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
                    else:
                        for item in result:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)
    

def salesforce_delete_task(creds,token, params):
    """
    Delete a Salesforce Task.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :id: (str, required) - The ID of the Task to be deleted.

    Returns:
      dict: A dictionary with a result message if the deletion is successful.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Task/"
        if "id" in params:
            access_token = token
            task_id = params["id"]
            url += f"{task_id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.delete(url, headers=headers)
            if response.status_code == 204:
                return {"Result": f"Deleted Task ID: {task_id}"}
            else:
                if response.content:
                    result = response.json()
                    if type(result) == list:
                        for item in result[0]:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
                    else:
                        for item in result:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


###########################################################################

# Opportunity Actions


def salesforce_get_opportunity(creds,token, params):
    """
    Retrieve information about a Salesforce opportunity.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :id: (str, required) - The ID of the Salesforce opportunity to be retrieved.

    Returns:
      dict: A dictionary containing information about the Salesforce opportunity.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Opportunity/"
        if "id" in params:
            access_token = token
            opportunity_id = params["id"]
            url += f"{opportunity_id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            result = response.json()
            if type(result) == list:
                for item in result[0]:
                    if item == "errorCode":
                        raise Exception(result)
                return result
            else:
                for item in result:
                    if item == "errorCode":
                        raise Exception(result)
                return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_get_opportunity_summary(creds,token):
    """
    Retrieve a summary of Salesforce opportunity.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.

    Returns:
      dict: A dictionary containing summary information about Salesforce opportunity.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Opportunity"
        access_token = token
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        result = response.json()
        if type(result) == list:
            for item in result[0]:
                if item == "errorCode":
                    raise Exception(result)
            return result
        else:
            for item in result:
                if item == "errorCode":
                    raise Exception(result)
            return result

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_list_opportunities(creds,token, params):
    """
    Retrieve a list of Salesforce opportunities based on the provided parameters.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :fields: (str, optional) - Comma-separated fields to be included in the SELECT query.
    - :conditions: (list of strings, optional) - list of conditions to filter the query results.

    Returns:
      dict: A dictionary containing information about the Salesforce opportunities that match the query.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/query?q="
        access_token = token
        query = "SELECT Id, AccountId, Amount, Probability, Type FROM Opportunity"
        conditions = ""
        for key, value in params.items():
            if key == "fields":
                query = f"SELECT {value} FROM Opportunity"

            if key == "conditions":
                conditions = " AND ".join(value)
                conditions = " WHERE " + conditions

        url += query + conditions

        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        result = response.json()
        if type(result) == list:
            for item in result[0]:
                if item == "errorCode":
                    raise Exception(result)
            return result
        else:
            for item in result:
                if item == "errorCode":
                    raise Exception(result)
            return result

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_create_opportunity(creds,token, params):
    """
    Create a new opportunity in Salesforce.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :name: (str, required) - The name of the Opportunity.
    - :stageName: (str, required) - The current stage of the Opportunity.
    
            (Options: Closed Lost, Closed Won, Meet & Present,
            
            Negotiate, Propose, Qualify)
    
    - :closeDate: (str, required) - The closing date for the Opportunity. 

        (Format: YYYY-MM-DD)

    - :accountId: (str, optional) - The ID of the associated Account.
    - :description: (str, optional) - Additional information about the Opportunity.
    - :amount: (float, optional) - The amount associated with the Opportunity.
    - :probability: (float, optional) - The probability of closing the Opportunity.
        
            (expressed as a percentage)
    
    
    - :type: (str, optional) - The type of Opportunity.

            (Options: Business, New Business)
        
    - :nextStep: (str, optional) - The next step planned for the Opportunity.
    - :leadSource: (str, optional) - The source that generated the lead for this Opportunity.

        (Options: Advertisement, Employee Referral, External Referral, Partner, Public Relations, Seminar - Internal, Seminar - Partner, Trade Show, Web, Word of mouth, or any other lead Source)

    - :forecastCategoryName: (str, optional) - The forecast category associated with the Opportunity.
    - :campaignId: (str, optional) - The ID of the associated Campaign.
    - :pricebook2Id: (str, optional) - The ID of the associated Price Book. 
    - :ownerId: (str, optional) - The ID of the user who owns for the Opportunity. 
    - :deliveryInstallationStatus__c: (str, optional) - Custom field for thedelivery installation
    
            status of the Opportunity.

    - :trackingNumber__c: (str, optional) - Custom field for tracking information associated with
    
            the Opportunity.

    - :orderNumber__c: (str, optional) - Custom field for the order number associated with
        
            the Opportunity.

    - :currentGenerators__c: (str, optional) - Custom field for current generators
    
            related to the Opportunity.

    - :mainCompetitors__c: (str, optional) - Custom field for main competitors associated
    
            with the Opportunity.

    Returns:
      dict: The JSON response containing information about the created opportunity.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Opportunity"
        if "name" in params and "stageName" in params and "closeDate" in params:
            access_token = token
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value

            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            if type(result) == list:
                for item in result[0]:
                    if item == "errorCode":
                        raise Exception(result)
                return result
            else:
                for item in result:
                    if item == "errorCode":
                        raise Exception(result)
                return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_update_opportunity(creds,token, params):
    """
    Update a Opportunity in Salesforce.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :id: (str, required) - The ID of the Opportunity to be updated.
        - Additional optional parameters based on Opportunity type (same parameters in create Opportunity).
        
    Returns:
      dict: The JSON response containing information about the updated Opportunity.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Opportunity/"
        if "id" in params:
            access_token = token
            opportunity_id = params["id"]
            url += f"{opportunity_id}"
            data = {}
            for key, value in params.items():
                if key == "id":
                    continue
                if value:
                    data[key] = value

            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.patch(url, headers=headers, json=data)
            if response.status_code == 204:
                return {"Result": f"Updated Opportunity ID: {opportunity_id}"}
            else:
                if response.content:
                    result = response.json()
                    if type(result) == list:
                        for item in result[0]:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
                    else:
                        for item in result:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_delete_opportunity(creds,token, params):
    """
    Delete a Salesforce opportunity.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :id: (str, required) - The ID of the opportunity to be deleted.

    Returns:
      dict: A dictionary with a result message if the deletion is successful.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Opportunity/"
        if "id" in params:
            access_token = token
            opportunity_id = params["id"]
            url += f"{opportunity_id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.delete(url, headers=headers)
            if response.status_code == 204:
                return {"Result": f"Deleted Opportunity ID: {opportunity_id}"}
            else:
                if response.content:
                    result = response.json()
                    if type(result) == list:
                        for item in result[0]:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
                    else:
                        for item in result:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


###########################################################################

# Lead Actions


def salesforce_get_lead(creds,token, params):
    """
    Retrieve information about a Salesforce lead.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :id: (str, required) - The ID of the Salesforce lead to be retrieved.

    Returns:
      dict: A dictionary containing information about the Salesforce lead.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Lead/"
        if "id" in params:
            access_token = token
            lead_id = params["id"]
            url += f"{lead_id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            result = response.json()
            if type(result) == list:
                for item in result[0]:
                    if item == "errorCode":
                        raise Exception(result)
                return result
            else:
                for item in result:
                    if item == "errorCode":
                        raise Exception(result)
                return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_get_lead_summary(creds,token):
    """
    Retrieve a summary of Salesforce lead.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.

    Returns:
      dict: A dictionary containing summary information about Salesforce lead.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Lead"
        access_token = token
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        result = response.json()
        if type(result) == list:
            for item in result[0]:
                if item == "errorCode":
                    raise Exception(result)
            return result
        else:
            for item in result:
                if item == "errorCode":
                    raise Exception(result)
            return result

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_list_leads(creds,token, params):
    """
    Retrieve a list of Salesforce leads based on the provided parameters.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :fields: (str, optional) - Comma-separated fields to be included in the SELECT query.
    - :conditions: (list of strings, optional) - list of conditions to filter the query results.

    Returns:
      dict: A dictionary containing information about the Salesforce leads that match the query.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/query?q="
        access_token = token
        query = "SELECT Id, Company, FirstName, LastName, Street, PostalCode, City, Email, Status FROM Lead"
        conditions = ""
        for key, value in params.items():
            if key == "fields":
                query = f"SELECT {value} FROM lead"

            if key == "conditions":
                conditions = " AND ".join(value)
                conditions = " WHERE " + conditions

        url += query + conditions

        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        result = response.json()
        if type(result) == list:
            for item in result[0]:
                if item == "errorCode":
                    raise Exception(result)
            return result
        else:
            for item in result:
                if item == "errorCode":
                    raise Exception(result)
            return result

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_create_lead(creds,token, params):
    """
    Create a new Lead in Salesforce.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :lastName: (str, required) - The last name of the lead.
    - :company: (str, required) - The name of the company associated with the lead.
    - :firstName: (str, optional) - The first name of the lead.
    - :salutation: (str, optional) - The salutation for the lead.
    - :title: (str, optional) - The job title of the lead.
    - :masterRecordId: (str, optional) - The ID of the master record if this record
    
            is a duplicate and is a child in a duplicate record set. 
            
            For new records, this can be set to null.

    - :website: (str, optional) - The website URL associated with the lead.
    - :leadSource: (str, optional) - The source from which the lead was obtained.

        (Options: Advertisement, Employee Referral, External Referral, Partner, Public Relations, Seminar - Internal, Seminar - Partner, Trade Show, Web, Word of mouth, or any other lead Source)
    
    - :status: (str, optional) - The status of the lead.

            (Options: Contacted, New, Nurturing, Qualified, Unqualified)

    - :industry: (str, optional) - The industry associated with the lead.
    - :rating: (str, optional) - The rating assigned to the lead.
    - :annualRevenue: (float, optional) - The annual revenue of the lead's company.
    - :numberOfEmployees: (str, optional) - The number of employees in the lead's company.
    - :ownerId: (str, optional) - The ID of the user who owns the lead.
    - :isUnreadByOwner: (bool, optional) - Indicates whether the lead is marked as unread by the owner.
    - :jigsaw: (str, optional) - The ID of a Data.com lead record.
    - :siccode__c: (str, optional) - The Standard Industrial Classification (SIC) code.
    - :productInterest__c: (str, optional) - The product of interest for the lead.
    - :primary__c: (bool, optional) - Indicates whether the lead is primary.
    - :currentGenerators__c: (str, optional) - The current generators for the lead.
    - :numberofLocations__c: (str, optional) - The number of locations for the lead.

    Returns:
      dict: The JSON response containing information about the created Lead.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Lead"
        if "company" in params and "lastName" in params:
            access_token = token
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value

            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            if type(result) == list:
                for item in result[0]:
                    if item == "errorCode":
                        raise Exception(result)
                return result
            else:
                for item in result:
                    if item == "errorCode":
                        raise Exception(result)
                return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_update_lead(creds,token, params):
    """
    Update a Lead in Salesforce.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :id: (str, required) - The ID of the Lead to be updated.
        - Additional optional parameters based on Lead type (same parameters in create Lead).
        
    Returns:
      dict: The JSON response containing information about the updated Lead.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Lead/"
        if "id" in params:
            access_token = token
            lead_id = params["id"]
            url += f"{lead_id}"
            data = {}
            for key, value in params.items():
                if key == "id":
                    continue
                if value:
                    data[key] = value

            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.patch(url, headers=headers, json=data)
            if response.status_code == 204:
                return {"Result": f"Updated Lead ID: {lead_id}"}
            else:
                if response.content:
                    result = response.json()
                    if type(result) == list:
                        for item in result[0]:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
                    else:
                        for item in result:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_delete_lead(creds,token, params):
    """
    Delete a Salesforce lead.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :id: (str, required) - The ID of the lead to be deleted.

    Returns:
      dict: A dictionary with a result message if the deletion is successful.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Lead/"
        if "id" in params:
            access_token = token
            lead_id = params["id"]
            url += f"{lead_id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.delete(url, headers=headers)
            if response.status_code == 204:
                return {"Result": f"Deleted Lead ID: {lead_id}"}
            else:
                if response.content:
                    result = response.json()
                    if type(result) == list:
                        for item in result[0]:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
                    else:
                        for item in result:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_add_lead_to_campaign(creds,token, params):
    """
    Add a lead to a Salesforce campaign.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :leadId: (str, required) - The ID of the lead to be added to the campaign.
    - :campaignId: (str, required) - The ID of the campaign to which the lead will be added.
    - :status: (str, optional) - The status of the campaign member.

    Returns:
      dict: A dictionary with a success result.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/CampaignMember"
        if "leadId" in params and "campaignId" in params:
            access_token = token
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value

            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            if type(result) == list:
                for item in result[0]:
                    if item == "errorCode":
                        raise Exception(result)
                return result
            else:
                for item in result:
                    if item == "errorCode":
                        raise Exception(result)
                return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


###########################################################################

# Contact Actions


def salesforce_get_contact(creds,token, params):
    """
    Retrieve information about a Salesforce contact.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :id: (str, required) - The ID of the Salesforce contact to be retrieved.

    Returns:
      dict: A dictionary containing information about the Salesforce contact.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Contact/"
        if "id" in params:
            access_token = token
            contact_id = params["id"]
            url += f"{contact_id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            result = response.json()
            if type(result) == list:
                for item in result[0]:
                    if item == "errorCode":
                        raise Exception(result)
                return result
            else:
                for item in result:
                    if item == "errorCode":
                        raise Exception(result)
                return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_get_contact_summary(creds,token):
    """
    Retrieve a summary of Salesforce contact.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.

    Returns:
      dict: A dictionary containing summary information about Salesforce contact.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Contact"
        access_token = token
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        result = response.json()
        if type(result) == list:
            for item in result[0]:
                if item == "errorCode":
                    raise Exception(result)
            return result
        else:
            for item in result:
                if item == "errorCode":
                    raise Exception(result)
            return result

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_list_contacts(creds,token, params):
    """
    Retrieve a list of Salesforce contacts based on the provided parameters.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :fields: (str, optional) - Comma-separated fields to be included in the SELECT query.
    - :conditions: (list of strings, optional) - list of conditions to filter the query results.

    Returns:
      dict: A dictionary containing information about the Salesforce contacts that match the query.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/query?q="
        access_token = token
        query = "SELECT Id, FirstName, LastName, Email FROM Contact"
        conditions = ""
        for key, value in params.items():
            if key == "fields":
                query = f"SELECT {value} FROM Contact"

            if key == "conditions":
                conditions = " AND ".join(value)
                conditions = " WHERE " + conditions

        url += query + conditions

        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        result = response.json()
        if type(result) == list:
            for item in result[0]:
                if item == "errorCode":
                    raise Exception(result)
            return result
        else:
            for item in result:
                if item == "errorCode":
                    raise Exception(result)
            return result

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_create_contact(creds,token, params):
    """
    Create a new Contact in Salesforce.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :lastName: (str, required) - The last name of the contact.
    - :firstName: (str, optional) - The first name of the contact.
    - :salutation: (str, optional) - The salutation for the contact.
    - :title: (str, optional) - The job title of the contact.
    - :masterRecordId: (str, optional) - The ID of the master record if this record
    
            is a duplicate and is a child in a duplicate record set. 
            
            For new records, this can be set to null.

    - :accountId: (str, optional) - The ID of the associated account.
    - :assistantName: (str, optional) - The name of the contact's assistant.
    - :assistantPhone: (str, optional) - The phone number of the contact's assistant.
    - :department: (str, optional) - The department to which the contact belongs.
    - :leadSource: (str, optional) - The source from which the lead was obtained.

        (Options: Advertisement, Employee Referral, External Referral, Partner, Public Relations, Seminar - Internal, Seminar - Partner, Trade Show, Web, Word of mouth, or any other lead Source)

    - :birthdate: (str, optional) - The birthdate of the contact.
    - :emailBouncedReason: (str, optional) - The reason for a bounced email.
    - :emailBouncedDate: (str, optional) - The date when an email bounced.
    - :jigsaw: (str, optional) - The ID of a Data.com contact record.
    - :level__c: (str, optional) - The level of the contact.
    - :languages__c: (str, optional) - The languages spoken by the contact.

    Returns:
      dict: The JSON response containing information about the created Contact.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Contact"
        if "lastName" in params:
            access_token = token
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value

            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            if type(result) == list:
                for item in result[0]:
                    if item == "errorCode":
                        raise Exception(result)
                return result
            else:
                for item in result:
                    if item == "errorCode":
                        raise Exception(result)
                return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_update_contact(creds,token, params):
    """
    Update a Contact in Salesforce.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :id: (str, required) - The ID of the Contact to be updated.
        - Additional optional parameters based on Contact type (same parameters in create Contact).
        
    Returns:
      dict: The JSON response containing information about the updated Contact.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Contact/"
        if "id" in params:
            access_token = token
            contact_id = params["id"]
            url += f"{contact_id}"
            data = {}
            for key, value in params.items():
                if key == "id":
                    continue
                if value:
                    data[key] = value

            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.patch(url, headers=headers, json=data)
            if response.status_code == 204:
                return {"Result": f"Updated Contact ID: {contact_id}"}
            else:
                if response.content:
                    result = response.json()
                    if type(result) == list:
                        for item in result[0]:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
                    else:
                        for item in result:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_delete_contact(creds,token, params):
    """
    Delete a Salesforce contact.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :id: (str, required) - The ID of the contact to be deleted.

    Returns:
      dict: A dictionary with a result message if the deletion is successful.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Contact/"
        if "id" in params:
            access_token = token
            contact_id = params["id"]
            url += f"{contact_id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.delete(url, headers=headers)
            if response.status_code == 204:
                return {"Result": f"Deleted Contact ID: {contact_id}"}
            else:
                if response.content:
                    result = response.json()
                    if type(result) == list:
                        for item in result[0]:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
                    else:
                        for item in result:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_add_contact_to_campaign(creds,token, params):
    """
    Add a contact to a Salesforce campaign.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :contactId: (str, required) - The ID of the contact to be added to the campaign.
    - :campaignId: (str, required) - The ID of the campaign to which the contact will be added.
    - :status: (str, optional) - The status of the campaign member.

    Returns:
      dict: A dictionary with a success result.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/CampaignMember"
        if "contactId" in params and "campaignId" in params:
            access_token = token
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value

            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            if type(result) == list:
                for item in result[0]:
                    if item == "errorCode":
                        raise Exception(result)
                return result
            else:
                for item in result:
                    if item == "errorCode":
                        raise Exception(result)
                return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


###########################################################################

# Case Actions


def salesforce_get_case(creds,token, params):
    """
    Retrieve information about a Salesforce case.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :id: (str, required) - The ID of the Salesforce case to be retrieved.

    Returns:
      dict: A dictionary containing information about the Salesforce case.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Case/"
        if "id" in params:
            access_token = token
            case_id = params["id"]
            url += f"{case_id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            result = response.json()
            if type(result) == list:
                for item in result[0]:
                    if item == "errorCode":
                        raise Exception(result)
                return result
            else:
                for item in result:
                    if item == "errorCode":
                        raise Exception(result)
                return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_get_case_summary(creds,token):
    """
    Retrieve a summary of Salesforce case.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.

    Returns:
      dict: A dictionary containing summary information about Salesforce case.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Case"
        access_token = token
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        result = response.json()
        if type(result) == list:
            for item in result[0]:
                if item == "errorCode":
                    raise Exception(result)
            return result
        else:
            for item in result:
                if item == "errorCode":
                    raise Exception(result)
            return result

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_list_cases(creds,token, params):
    """
    Retrieve a list of Salesforce cases based on the provided parameters.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :fields: (str, optional) - Comma-separated fields to be included in the SELECT query.
    - :conditions: (list of strings, optional) - list of conditions to filter the query results.

    Returns:
      dict: A dictionary containing information about the Salesforce cases that match the query.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/query?q="
        access_token = token
        query = (
            "SELECT Id, AccountId, ContactId, Priority, Status, Subject, Type FROM Case"
        )
        conditions = ""
        for key, value in params.items():
            if key == "fields":
                query = f"SELECT {value} FROM Case"

            if key == "conditions":
                conditions = " AND ".join(value)
                conditions = " WHERE " + conditions

        url += query + conditions

        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        result = response.json()
        if type(result) == list:
            for item in result[0]:
                if item == "errorCode":
                    raise Exception(result)
            return result
        else:
            for item in result:
                if item == "errorCode":
                    raise Exception(result)
            return result

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_create_case(creds,token, params):
    """
    Create a new Case in Salesforce.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :type: (str, required) - The type of the case.

            (Options: Feature Request, Problem, Question, or any other type)

    - :contactId: (str, optional) - The ID of the contact associated with the case.
    - :accountId: (str, optional) - The ID of the account associated with the case.
    - :parentId: (str, optional) - The ID of the parent case. 
    
            For new cases, this can be set to null.
    
    - :status: (str, optional) - The status of the case.

            (Options: Closed, Escalated, Waiting on Customer, New, Working)
    
    - :reason: (str, optional) - The reason for the case.

            (Options: Complex functionality, Existing problem, Instructions not clear,
            
            New problem, User didn't attend training)
    
    - :origin: (str, optional) - The origin of the case.

            (Options: Email, Phone, Web)

    - :priority: (str, optional) - Case priority.

            (Options: High, Low, Normal)

    - :isEscalated: (bool, optional) - Indicates whether the case has been escalated.
    - :ownerId: (str, optional) - The ID of the user who owns the case.
    - :engineeringReqNumber__c: (str, optional) - An engineering request number.
    - :slaviolation__c: (str, optional) - Indicates whether there is a SLA (Service Level Agreement) violation.

            (Options include Yes or No)

    - :product__c: (str, optional) - The product associated with the case.
    - :potentialLiability__c: (str, optional) - Indicates whether there is potential liability.

            (Options include Yes or No)

    Returns:
      dict: The JSON response containing information about the created Case.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Case"
        if "type" in params:
            access_token = token
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value

            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            if type(result) == list:
                for item in result[0]:
                    if item == "errorCode":
                        raise Exception(result)
                return result
            else:
                for item in result:
                    if item == "errorCode":
                        raise Exception(result)
                return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_update_case(creds,token, params):
    """
    Update a Case in Salesforce.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :id: (str, required) - The ID of the Case to be updated.
        - Additional optional parameters based on Case type (same parameters in create Case).
        
    Returns:
      dict: The JSON response containing information about the updated Case.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Case/"
        if "id" in params:
            access_token = token
            case_id = params["id"]
            url += f"{case_id}"
            data = {}
            for key, value in params.items():
                if key == "id":
                    continue
                if value:
                    data[key] = value

            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.patch(url, headers=headers, json=data)
            if response.status_code == 204:
                return {"Result": f"Updated Case ID: {case_id}"}
            else:
                if response.content:
                    result = response.json()
                    if type(result) == list:
                        for item in result[0]:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
                    else:
                        for item in result:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_delete_case(creds,token, params):
    """
    Delete a Salesforce case.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :id: (str, required) - The ID of the case to be deleted.

    Returns:
      dict: A dictionary with a result message if the deletion is successful.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Case/"
        if "id" in params:
            access_token = token
            case_id = params["id"]
            url += f"{case_id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.delete(url, headers=headers)
            if response.status_code == 204:
                return {"Result": f"Deleted Case ID: {case_id}"}
            else:
                if response.content:
                    result = response.json()
                    if type(result) == list:
                        for item in result[0]:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
                    else:
                        for item in result:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_add_comment_to_case(creds,token, params):
    """
    Add a comment to a Salesforce case.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :parentId: (str, required) - The ID of the case to which the comment will be added.
    - :commentBody: (str, optional) - The text content of the comment.
    - :isPublished: (bool, optional) - Publish the comment to be visible to customers. Default is True.

    Returns:
      dict: A dictionary with a success result.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/CaseComment"
        if "parentId" in params:
            access_token = token
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value

            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            if type(result) == list:
                for item in result[0]:
                    if item == "errorCode":
                        raise Exception(result)
                return result
            else:
                for item in result:
                    if item == "errorCode":
                        raise Exception(result)
                return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


###########################################################################

# Account Actions


def salesforce_get_account(creds,token, params):
    """
    Retrieve information about a Salesforce account.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :id: (str, required) - The ID of the Salesforce account to be retrieved.

    Returns:
      dict: A dictionary containing information about the Salesforce account.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Account/"
        if "id" in params:
            access_token = token
            account_id = params["id"]
            url += f"{account_id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            result = response.json()
            if type(result) == list:
                for item in result[0]:
                    if item == "errorCode":
                        raise Exception(result)
                return result
            else:
                for item in result:
                    if item == "errorCode":
                        raise Exception(result)
                return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_get_account_summary(creds,token):
    """
    Retrieve a summary of Salesforce account.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.

    Returns:
      dict: A dictionary containing summary information about Salesforce account.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Account"
        access_token = token
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        result = response.json()
        if type(result) == list:
            for item in result[0]:
                if item == "errorCode":
                    raise Exception(result)
            return result
        else:
            for item in result:
                if item == "errorCode":
                    raise Exception(result)
            return result

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_list_accounts(creds,token, params):
    """
    Retrieve a list of Salesforce accounts based on the provided parameters.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :fields: (str, optional) - Comma-separated fields to be included in the SELECT query.
    - :conditions: (list of strings, optional) - list of conditions to filter the query results.

    Returns:
      dict: A dictionary containing information about the Salesforce accounts that match the query.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/query?q="
        access_token = token
        query = "SELECT Id, Name, Type FROM Account"
        conditions = ""
        for key, value in params.items():
            if key == "fields":
                query = f"SELECT {value} FROM Account"

            if key == "conditions":
                conditions = " AND ".join(value)
                conditions = " WHERE " + conditions

        url += query + conditions

        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        result = response.json()
        if type(result) == list:
            for item in result[0]:
                if item == "errorCode":
                    raise Exception(result)
            return result
        else:
            for item in result:
                if item == "errorCode":
                    raise Exception(result)
            return result

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_create_account(creds,token, params):
    """
    Create a new Account in Salesforce.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :name: (str, required) - The name of the account.
    - :type: (str, optional) - The type of the account.

            (Options: Call, Email, LinkedIn, List Email, Task, Cadence)
            
    - :parentId: (str, optional) - The ID of the parent account. 
    
            It's typically used for creating a hierarchy of accounts.

    - :accountNumber: (str, optional) - A unique account number.
    - :website: (str, optional) - The website URL of the account.
    - :industry: (str, optional) - The industry to which the account belongs.
    - :accountSource: (str, optional) - The source from which the account was acquired.

        (Options: Advertisement, Employee Referral, External Referral, Partner, Public Relations, Seminar - Internal, Seminar - Partner, Trade Show, Web, Word of mouth, or any other account Source)

    - :sicDesc: (str, optional) - Standard Industrial Classification (SIC) description.
    - :customerPriority__c: (str, optional) - Custom field for customer priority.
    - :sla__c: (str, optional) - The Service Level Agreement (SLA) information.
    - :active__c: (str, optional) - Indicates whether the account is active or not.
    - :numberofLocations__c: (str, optional) - The number of locations associated
            with the account.
    - :upsellOpportunity__c: (str, optional) - Indicates upsell opportunity. 
    - :slaSerialNumber__c: (str, optional) - Custom field for SLA serial number.
    - :slaExpirationDate__c: (str, optional) - Custom field for SLA expiration date.

    Returns:
      dict: The JSON response containing information about the created Account.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Account"
        if "name" in params:
            access_token = token
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value

            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            if type(result) == list:
                for item in result[0]:
                    if item == "errorCode":
                        raise Exception(result)
                return result
            else:
                for item in result:
                    if item == "errorCode":
                        raise Exception(result)
                return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_update_account(creds,token, params):
    """
    Update a Account in Salesforce.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :id: (str, required) - The ID of the Account to be updated.
        - Additional optional parameters based on Account type (same parameters in create Account).
        
    Returns:
      dict: The JSON response containing information about the updated Account.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Account/"
        if "id" in params:
            access_token = token
            account_id = params["id"]
            url += f"{account_id}"
            data = {}
            for key, value in params.items():
                if key == "id":
                    continue
                if value:
                    data[key] = value

            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.patch(url, headers=headers, json=data)
            if response.status_code == 204:
                return {"Result": f"Updated Account ID: {account_id}"}
            else:
                if response.content:
                    result = response.json()
                    if type(result) == list:
                        for item in result[0]:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
                    else:
                        for item in result:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_delete_account(creds,token, params):
    """
    Delete a Salesforce account.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :id: (str, required) - The ID of the account to be deleted.

    Returns:
      dict: A dictionary with a result message if the deletion is successful.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Account/"
        if "id" in params:
            access_token = token
            account_id = params["id"]
            url += f"{account_id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.delete(url, headers=headers)
            if response.status_code == 204:
                return {"Result": f"Deleted Account ID: {account_id}"}
            else:
                if response.content:
                    result = response.json()
                    if type(result) == list:
                        for item in result[0]:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
                    else:
                        for item in result:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


###########################################################################

# Custom Object Actions


def salesforce_get_custom_object(creds,token, params):
    """
    Retrieve information about a Salesforce custom object record.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :customObjectName: (str, required) - The API name of the custom object.
    - :id: (str, required) - The ID of the Salesforce custom object to be retrieved.

    Returns:
      dict: A dictionary containing information about the Salesforce custom object record.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = (
            f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/"
        )
        if "customObjectName" in params and "id" in params:
            access_token = token
            custom_object_name = params["customObjectName"]
            record_id = params["id"]
            url += f"{custom_object_name}/{record_id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            result = response.json()
            if type(result) == list:
                for item in result[0]:
                    if item == "errorCode":
                        raise Exception(result)
                return result
            else:
                for item in result:
                    if item == "errorCode":
                        raise Exception(result)
                return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_list_custom_objects(creds,token, params):
    """
    Retrieve a list of Salesforce custom objects based on the provided parameters.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :customObjectName: (str, required) - The API name of the custom object.
    - :fields: (str, optional) - Comma-separated fields to be included in the SELECT query.
    - :conditions: (list of strings, optional) - list of conditions to filter the query results.

    Returns:
      dict: A dictionary containing information about the Salesforce custom objects that match the query.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/query?q="
        if "customObjectName" in params:
            access_token = token
            custom_object_name = params["customObjectName"]
            query = "Select id FROM " + custom_object_name
            conditions = ""

            for key, value in params.items():
                if key == "customObjectName":
                    continue
                if key == "fields":
                    query = f"SELECT {value} FROM " + custom_object_name

                if key == "conditions":
                    conditions = " AND ".join(value)
                    conditions = " WHERE " + conditions

            url += query + conditions

            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            result = response.json()
            if type(result) == list:
                for item in result[0]:
                    if item == "errorCode":
                        raise Exception(result)
                return result
            else:
                for item in result:
                    if item == "errorCode":
                        raise Exception(result)
                return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_create_custom_object(creds,token, params):
    """
    Create a new Custom Object Record in Salesforce.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :customObjectName: (str, required) - The API name of the custom object.

    - Custom Fields (str,optional) - Custom fields and their values for the new Custom Object Record.
            For example,
            
            {"customObjectName": "" , "field1": "value1", "field2": "value2"}

    Returns:
      dict: The JSON response containing information about the created Custom Object Record.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = (
            f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/"
        )
        if "customObjectName" in params:
            access_token = token
            custom_object_name = params["customObjectName"]
            url += f"{custom_object_name}"

            data = {}
            for key, value in params.items():
                if key == "customObjectName":
                    continue
                if value:
                    data[key] = value

            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            if type(result) == list:
                for item in result[0]:
                    if item == "errorCode":
                        raise Exception(result)
                return result
            else:
                for item in result:
                    if item == "errorCode":
                        raise Exception(result)
                return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_update_custom_object(creds,token, params):
    """
    Update a Custom Object Record in Salesforce.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :id: (str, required) - The ID of the Custom Object to be updated.
        - Additional optional parameters based on Custom Object type (same parameters in create Custom Object).
        
    Returns:
      dict: The JSON response containing information about the updated Custom Object Record.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = (
            f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/"
        )
        if "customObjectName" in params and "id" in params:
            access_token = token
            custom_object_name = params["customObjectName"]
            record_id = params["id"]
            url += f"{custom_object_name}/{record_id}"
            data = {}
            keys_to_skip = ["id", "customObjectName"]
            for key, value in params.items():
                if key in keys_to_skip:
                    continue
                if value:
                    data[key] = value

            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.patch(url, headers=headers, json=data)
            if response.status_code == 204:
                return {"Result": f"Updated Custom Object ID: {record_id} From {custom_object_name}"}
            else:
                if response.content:
                    result = response.json()
                    if type(result) == list:
                        for item in result[0]:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
                    else:
                        for item in result:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_delete_custom_object(creds,token, params):
    """
    Delete a Salesforce custom object record.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :customObjectName: (str, required) - The API name of the custom object.
    - :id: (str, required) - The ID of the custom object to be deleted.

    Returns:
      dict: A dictionary with a result message if the deletion is successful.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = (
            f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/"
        )
        if "customObjectName" in params and "id" in params:
            access_token = token
            custom_object_name = params["customObjectName"]
            record_id = params["id"]
            url += f"{custom_object_name}/{record_id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.delete(url, headers=headers)
            if response.status_code == 204:
                return {"Result": f"Deleted Custom Object ID: {record_id} From {custom_object_name}"}
            else:
                if response.content:
                    result = response.json()
                    if type(result) == list:
                        for item in result[0]:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
                    else:
                        for item in result:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


###########################################################################

# Search Action


def salesforce_search_records(creds,token, params):
    """
    Search records in Salesforce.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :query: (str, required) - The query string for record searching.

    Returns:
      dict: A dictionary containing information about the searched records.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/query?q="
        if "query" in params:
            access_token = token
            query = params["query"]
            url += query
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            result = response.json()
            if type(result) == list:
                for item in result[0]:
                    if item == "errorCode":
                        raise Exception(result)
                return result
            else:
                for item in result:
                    if item == "errorCode":
                        raise Exception(result)
                return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


###########################################################################

# Attachment Actions


def salesforce_get_attachment(creds,token, params):
    """
    Retrieve information about a Salesforce attachment.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :id: (str, required) - The ID of the Salesforce attachment to be retrieved.

    Returns:
      dict: A dictionary containing information about the Salesforce attachment.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Attachment/"
        if "id" in params:
            access_token = token
            attachment_id = params["id"]
            url += f"{attachment_id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            result = response.json()
            if type(result) == list:
                for item in result[0]:
                    if item == "errorCode":
                        raise Exception(result)
                return result
            else:
                for item in result:
                    if item == "errorCode":
                        raise Exception(result)
                return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_get_attachment_summary(creds,token):
    """
    Retrieve a summary of Salesforce attachment.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.

    Returns:
      dict: A dictionary containing summary information about Salesforce attachment.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Attachment"

        access_token = token
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        result = response.json()
        if type(result) == list:
            for item in result[0]:
                if item == "errorCode":
                    raise Exception(result)
            return result
        else:
            for item in result:
                if item == "errorCode":
                    raise Exception(result)
            return result

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_list_attachments(creds,token, params):
    """
    Retrieve a list of Salesforce attachments based on the provided parameters.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :fields: (str, optional) - Comma-separated fields to be included in the SELECT query.
    - :conditions: (list of strings, optional) - list of conditions to filter the query results.

    Returns:
      dict: A dictionary containing information about the Salesforce attachments that match the query.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/query?q="

        access_token = token
        query = "SELECT Id, Name FROM Attachment"
        conditions = ""
        for key, value in params.items():
            if key == "fields":
                query = f"SELECT {value} FROM Attachment"

            if key == "conditions":
                conditions = " AND ".join(value)
                conditions = " WHERE " + conditions

        url += query + conditions

        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        result = response.json()
        if type(result) == list:
            for item in result[0]:
                if item == "errorCode":
                    raise Exception(result)
            return result
        else:
            for item in result:
                if item == "errorCode":
                    raise Exception(result)
            return result

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_create_attachment(creds,token, params):
    """
    Create a new Attachment in Salesforce.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - One of the following is required:
        - :binary: (str) - The binary data of the file to be attached.
        - :url: (str) - The online URL from which the file content will be fetched.

    - :name: (str, required) - The name of the file, including the file extension.
    - :parentId: (str, required) - The ID of the record to which the attachment will be linked.

            (This could be the ID of an object like an Account, Contact, Opportunity, etc)

    - :ownerId: (str, optional) - The ID of the user who owns the attachment.
    - :isPrivate: (str, optional) - The ID of the user who owns the attachment.

    Returns:
      dict: The JSON response containing information about the created Attachment.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Attachment"
        if (
            "name" in params
            and "parentId" in params
            and ("binary" in params or "url" in params)
        ):
            access_token = token

            binary_data = None
            if params.get("binary"):
                binary_data = params["binary"]

            file_path = None
            if params.get("url"):
                file_path = params["url"]

            keys_to_skip = ["binary", "url"]
            data = {}
            for key, value in params.items():
                if key in keys_to_skip:
                    continue
                if value:
                    data[key] = value

            if file_path is not None:
                myFile = requests.get(file_path)
                if myFile.status_code == 200:
                    binary_data = myFile.content
                else:
                    raise Exception(
                        f"Failed to fetch the file. Status code: {myFile.status_code}"
                    )

            base64_data = base64.b64encode(binary_data.encode()).decode("utf-8")
            data["body"] = base64_data

            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            if type(result) == list:
                for item in result[0]:
                    if item == "errorCode":
                        raise Exception(result)
                return result
            else:
                for item in result:
                    if item == "errorCode":
                        raise Exception(result)
                return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_update_attachment(creds,token, params):
    """
    Update a Attachment in Salesforce.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :id: (str, required) - The ID of the Attachment to be updated.
        - Additional optional parameters based on Attachment type (same parameters in create Attachment).
        
    Returns:
      dict: The JSON response containing information about the updated Attachment.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Attachment/"
        if "id" in params:
            access_token = token
            attachment_id = params["id"]
            url += f"{attachment_id}"

            data = {}
            for key, value in params.items():
                if key == "id":
                    continue
                if value:
                    data[key] = value

            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.patch(url, headers=headers, json=data)
            if response.status_code == 204:
                return {"Result": f"Updated Attachment ID: {attachment_id}"}
            else:
                if response.content:
                    result = response.json()
                    if type(result) == list:
                        for item in result[0]:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
                    else:
                        for item in result:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


def salesforce_delete_attachment(creds,token, params):
    """
    Delete a Salesforce attachment.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :id: (str, required) - The ID of the attachment to be deleted.

    Returns:
      dict: A dictionary with a result message if the deletion is successful.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Attachment/"
        if "id" in params:
            access_token = token
            attachment_id = params["id"]
            url += f"{attachment_id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.delete(url, headers=headers)
            if response.status_code == 204:
                return {"Result": f"Deleted Attachment ID: {attachment_id}"}
            else:
                if response.content:
                    result = response.json()
                    if type(result) == list:
                        for item in result[0]:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
                    else:
                        for item in result:
                            if item == "errorCode":
                                raise Exception(result)
                        return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


###########################################################################

# Flow Actions


def salesforce_list_flows(creds,token, params):
    """
    Retrieve a list of Salesforce flows.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Empty dictionary.

    Returns:
      dict: A dictionary containing information about the Salesforce flows.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/actions/custom/flow"
        access_token = token
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        result = response.json()
        if type(result) == list:
            for item in result[0]:
                if item == "errorCode":
                    raise Exception(result)
            return result
        else:
            for item in result:
                if item == "errorCode":
                    raise Exception(result)
            return result

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


###########################################################################

# Add Notes to Opportunity OR Lead OR Contact OR Account


def salesforce_add_note_to_record(creds,token, params):
    """
    Add a note to a Salesforce record.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - :parentId: (str, required) - The ID of the record to which the note will be added.
    - :title: (str, required) - The title of the note. 
    - :body: (str, optional) - The content or body of the note.
    - :ownerId: (str, optional) - The ID of the owner of the note.
    - :isPrivate: (bool, optional) - Set the note as private.

    Returns:
      dict: A dictionary with a success result.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/Note"
        if "parentId" in params and "title" in params:
            access_token = token
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value

            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            if type(result) == list:
                for item in result[0]:
                    if item == "errorCode":
                        raise Exception(result)
                return result
            else:
                for item in result:
                    if item == "errorCode":
                        raise Exception(result)
                return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)


###########################################################################

# Document Action


def salesforce_upload_document(creds,token, params):
    """
    Upload a document to Salesforce.

    :domain: The Salesforce domain.
    :token: The Salesforce access token for authentication.
    :params: Dictionary containing parameters.

    - One of the following is required:
        - :binary: (str) - The binary data of the document.
        - :url: (str) - The online URL from which to fetch the document.
    - :pathOnClient: (str, required) - The file name with extension.
    - :title: (str, required) - The title of the document.
    - :description: (str, optional) - The description of the document.
    - :ownerId: (str, optional) - The ID of the document owner.

    Returns:
      dict: A dictionary with a success result.

    """
    try:
        cred=json.loads(creds)
        domain=cred['domainName']
        url = f"https://{domain}.my.salesforce.com/services/data/v58.0/sobjects/ContentVersion"
        if (
            "title" in params
            and "pathOnClient" in params
            and ("binary" in params or "url" in params)
        ):
            access_token = token

            binary_data = None
            if params.get("binary"):
                binary_data = params["binary"]

            file_path = None
            if params.get("url"):
                file_path = params["url"]

            keys_to_skip = ["binary", "url"]
            data = {}
            for key, value in params.items():
                if key in keys_to_skip:
                    continue
                if value:
                    data[key] = value

            if file_path is not None:
                myFile = requests.get(file_path)
                if myFile.status_code == 200:
                    binary_data = myFile.content
                else:
                    raise Exception(
                        f"Failed to fetch the file. Status code: {myFile.status_code}"
                    )

            base64_data = base64.b64encode(binary_data.encode()).decode("utf-8")
            data["versionData"] = base64_data

            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            if type(result) == list:
                for item in result[0]:
                    if item == "errorCode":
                        raise Exception(result)
                return result
            else:
                for item in result:
                    if item == "errorCode":
                        raise Exception(result)
                return result
        else:
            raise Exception("Missing input data")

    except Exception as error:
        if "Expecting value" in str(error):
            raise Exception("Invalid Domain")
        else:
            raise Exception(error)
