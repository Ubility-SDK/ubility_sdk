import requests
import json, logging
###########################################################################

# Ticket Actions


def freshdesk_get_ticket(cred, ticket_id):
    """
    Retrieve information about a specific ticket.

    :domain: The Freshdesk domain for the account.
    :ticket_id: The ID of the ticket to be retrieved.
    :params: A dictionary containing parameters:

        - :user: (str, required) - The username for authentication.
        - :pwd: (str, required) - same value of username.

    Returns:
      dict: A dictionary containing information about the specified ticket.

    """
    try:
        creds=json.loads(cred)
        domain=creds['domain']
        url = f"https://{domain}.freshdesk.com/api/v2/tickets/{ticket_id}"
        if ".freshdesk.com" in domain:
                raise Exception(f"Invalid URL detected. Please verify your domain name. Domain: {domain}, URL: {url}")
        if "apiKey" in creds:
            user = creds["apiKey"]
            pwd = creds["apiKey"]
            response = requests.get(url, auth=(user, pwd))
            result = response.json()
            for item in result:
                if item == "errors" or item == "code":
                    raise Exception(result)
            return result
        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Domain OR Id Not Found")
        else:
            raise Exception(e)

def freshdesk_get_all_tickets(cred, params):
    """
    Get a list of tickets from Freshdesk based on specified parameters.
    
    :domain: The Freshdesk domain for the account.
    :params: A dictionary containing parameters:

        - :user: (str, required) - The username for authentication.
        - :pwd: (str, required) - same value of username.
        - :company_id: (str, optional) - The ID of the company associated with the tickets.
        - :requester_id: (str, optional) - The ID of the requester associated with the tickets.
        - :email: (str, optional) - The email address associated with the tickets.
        - :include: (str, optional) - Specify additional details to include (stats, requester, description, company).
        - :updated_since: (str, optional) - Retrieve tickets updated since the specified date.
        
                (format: "YYYY-MM-DDTHH:MM:SS.000Z")

        - :order_type: (str, optional) - Specify the order type for sorting (asc, desc).
        - :order_by: (str, optional) - Specify the field for sorting tickets 
        
                (Options: created_at, due_by, updated_at, priority, status, fr_due_by, nr_due_by, closed_at)

    Returns:
      dict: A dictionary containing a list of tickets based on the specified parameters.

    """
    try:
        creds=json.loads(cred)
        domain=creds['domain']
        url = f"https://{domain}.freshdesk.com/api/v2/tickets"
        if ".freshdesk.com" in domain:
                raise Exception(f"Invalid URL detected. Please verify your domain name. Domain: {domain}, URL: {url}")
        if "apiKey" in creds:
            user = creds["apiKey"]
            pwd = creds["apiKey"]
            query_string = ""
            for key, value in params.items():
                if value:
                    query_string += f"&{key}={value}"

            if query_string != "":
                url += f"?{query_string}"

            response = requests.get(url, auth=(user, pwd))
            result = response.json()
            for item in result:
                if item == "errors" or item == "code":
                    raise Exception(result)
            return result

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Domain")
        else:
            raise Exception(e)


def freshdesk_create_ticket(cred, params):
    """
    Create a new ticket in Freshdesk.

    :domain: The Freshdesk domain for the account.
    :params: A dictionary containing parameters:

        - :user: (str, required) - The username for authentication.
        - :pwd: (str, required) - same value of username.
        - :description: (str, required) - The description of the ticket.
        - :subject: (str, required) - The subject of the ticket.
        - :priority: (int, required) - The priority of the ticket.  

                Options: 1 [Low], 2 [Medium], 3 [High], 4 [Urgent]
        
        - :status: (int, required) - The status of the ticket.
                
                Options: 2 [Open], 3 [Pending], 4 [Resolved], 5 [Closed]
        
        - :source: (int, required) - The source of the ticket (1, 2, 3, 7, 9, 10).
                
                Options: 1 [Email], 2 [Portal], 3 [Phone], 7 [Chat], 9 [Feedback Widget], 10 [Outbound Email]

        - At least, one of these parameters is required:
            email, phone, requester_id, facebook_id, unique_external_id, twitter_id.

        - :type: (str, optional) - Type of the ticket.
         
                (Options: Refund, Question, Problem, Incident, Feature Request)

        - :tags: (list of str, optional) - List of tags associated with the ticket.
        - :cc_emails: (list of str) - List of email addresses to be CC'd on the ticket.
        - ... (other parameters): Additional parameters that can be included in the params.

    Returns:
      dict: A dictionary containing information about the created ticket.

    """
    try:
        creds=json.loads(cred)
        domain=creds['domain']
        url = f"https://{domain}.freshdesk.com/api/v2/tickets"
        if ".freshdesk.com" in domain:
                raise Exception(f"Invalid URL detected. Please verify your domain name. Domain: {domain}, URL: {url}")
        allRequired = [
            "priority",
            "status",
            "source",
            "description",
            "subject",
        ]
        oneRequired = [
            "requester_id",
            "email",
            "facebook_id",
            "phone",
            "twitter_id",
            "unique_external_id",
        ]
        # Check if All items in 'allRequired' exist, and at least one item from 'oneRequired' exists in 'params'
        if all(item in params for item in allRequired) and any(
            item in params for item in oneRequired
        ):
            user = creds["apiKey"]
            pwd = creds["apiKey"]
            data = {"ticket": {}}
            for key, value in params.items():
                if value:
                    data["ticket"][key] = value
            response = requests.post(url, auth=(user, pwd), json=data)
            result = response.json()
            for item in result:
                if item == "errors" or item == "code":
                    raise Exception(result)
            return result
        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Domain")
        else:
            raise Exception(e)


def freshdesk_delete_ticket(cred, ticket_id):
    """
    Delete a specific ticket.

    :domain: The Freshdesk domain for the account.
    :ticket_id: The ID of the ticket to be deleted.
    :params: A dictionary containing parameters:

        - :user: (str, required) - The username for authentication.
        - :pwd: (str, required) - same value of username.

    Returns:
      dict: A dictionary containing information about the status of the deletion.

    """
    try:
        creds=json.loads(cred)
        domain=creds['domain']
        url = f"https://{domain}.freshdesk.com/api/v2/tickets/{ticket_id}"
        if ".freshdesk.com" in domain:
                raise Exception(f"Invalid URL detected. Please verify your domain name. Domain: {domain}, URL: {url}")
        if "apiKey" in creds:
            user = creds["apiKey"]
            pwd = creds["apiKey"]
            response = requests.delete(url, auth=(user, pwd))
            successStatus= [200,201,202,204,206,207,208]
            if response.status_code in successStatus:
                return {"Result": f"Deleted ticket ID: {ticket_id}"}
            else:
                raise Exception(
                    f"Failed to delete the ticket. Status code: {response.status_code}"
                )

        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Domain OR Id Not Found")
        else:
            raise Exception(e)


def freshdesk_update_ticket(cred, ticket_id, params):
    """
    Update an existing ticket.

    :domain: The Freshdesk domain for the account.
    :ticket_id: The ID of the ticket to be updated.
    :params: A dictionary containing parameters:

        - :user: (str, required) - The username for authentication.
        - :pwd: (str, required) - same value of username.
        - (Additional parameters): Other parameters to be updated, such as status, source, priority, etc.
        
    Returns:
      dict: A dictionary containing information about the updated ticket.

    """
    try:
        creds=json.loads(cred)
        domain=creds['domain']
        url = f"https://{domain}.freshdesk.com/api/v2/tickets/{ticket_id}"
        if ".freshdesk.com" in domain:
                raise Exception(f"Invalid URL detected. Please verify your domain name. Domain: {domain}, URL: {url}")
        if "apiKey" in creds:
            user = creds["apiKey"]
            pwd = creds["apiKey"]
            data = {"ticket": {}}
            for key, value in params.items():
                if value:
                    data["ticket"][key] = value
            response = requests.put(url, auth=(user, pwd), json=data)
            result = response.json()
            for item in result:
                if item == "errors" or item == "code" or item == "message":
                    raise Exception(result)
            return result
        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Domain OR Id Not Found")
        else:
            raise Exception(e)


###########################################################################

# Contact Actions


def freshdesk_get_contact(cred, contact_id):
    """
    Retrieve information about a specific contact.

    :domain: The Freshdesk domain for the account.
    :contact_id: The ID of the contact to be retrieved.
    :params: A dictionary containing parameters:

        - :user: (str, required) - The username for authentication.
        - :pwd: (str, required) - same value of username.

    Returns:
      dict: A dictionary containing information about the specified contact.

    """
    try:
        creds=json.loads(cred)
        domain=creds['domain']
        url = f"https://{domain}.freshdesk.com/api/v2/contacts/{contact_id}"
        if ".freshdesk.com" in domain:
                raise Exception(f"Invalid URL detected. Please verify your domain name. Domain: {domain}, URL: {url}")
        if "apiKey" in creds:
            user = creds["apiKey"]
            pwd = creds["apiKey"]
            response = requests.get(url, auth=(user, pwd))
            result = response.json()
            for item in result:
                if item == "errors" or item == "code":
                    raise Exception(result)
            return result
        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Domain OR Id Not Found")
        else:
            raise Exception(e)


def freshdesk_get_all_contacts(cred, params):
    """
    Get a list of contacts from Freshdesk based on specified parameters.
    
    :domain: The Freshdesk domain for the account.
    :params: A dictionary containing parameters:

        - :user: (str, required) - The username for authentication.
        - :pwd: (str, required) - same value of username.
        - :company_id: (str, optional) - The ID of the company associated with the contacts.
        - :email: (str, optional) - The email address associated with the contacts.
        - :mobile: (str, optional) - The mobile number associated with the contacts.
        - :phone: (str, optional) - The phone number associated with the contacts.
        - :updated_since: (str, optional) - Retrieve contacts updated since the specified date.
        
                (format: "YYYY-MM-DDTHH:MM:SS.000Z")
                
        - :state: (str, optional) - The state of the contacts (blocked, deleted, unverified, verified).

    Returns:
      dict: A dictionary containing a list of contacts based on the specified parameters.

    """
    try:
        creds=json.loads(cred)
        domain=creds['domain']
        url = f"https://{domain}.freshdesk.com/api/v2/contacts"
        if ".freshdesk.com" in domain:
                raise Exception(f"Invalid URL detected. Please verify your domain name. Domain: {domain}, URL: {url}")
        if "apiKey" in creds:
            user = creds["apiKey"]
            pwd = creds["apiKey"]
            query_string = ""
            for key, value in params:
                if value:
                    query_string += f"&{key}={value}"

            if query_string != "":
                url += f"?{query_string}"
            response = requests.get(url, auth=(user, pwd))
            result = response.json()
            for item in result:
                if item == "errors" or item == "code":
                    raise Exception(result)
            return result
        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Domain")
        else:
            raise Exception(e)


def freshdesk_create_contact(cred, params):
    """
    Create a new contact in Freshdesk.

    :domain: The Freshdesk domain for the account.
    :params: A dictionary containing parameters:

        - :user: (str, required) - The username for authentication.
        - :pwd: (str, required) - same value of username.
        - :email: (str, required) - The email address of the contact (unique identifier).
        - :custom_fields: (dict, optional) - Dictionary of custom fields.
        
                (e.g., {"key": "value"})

        - :other_emails: (list of str, optional) - List of other email addresses associated with the contact.
        - :other_companies: (list of dict, optional) - List of other companies associated with the contact.
            Each dict should have 'company_id' (int) and 'view_all_tickets' (bool).

    Returns:
      dict: A dictionary containing information about the created contact.

    """
    try:
        creds=json.loads(cred)
        domain=creds['domain']
        url = f"https://{domain}.freshdesk.com/api/v2/contacts"
        if ".freshdesk.com" in domain:
                raise Exception(f"Invalid URL detected. Please verify your domain name. Domain: {domain}, URL: {url}")
        if "apiKey" in creds and "email" in params:
            user = creds["apiKey"]
            pwd = creds["apiKey"]
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            response = requests.post(url, auth=(user, pwd), json=data)
            result = response.json()
            for item in result:
                if item == "errors" or item == "code":
                    raise Exception(result)
            return result
        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Domain")
        else:
            raise Exception(e)


def freshdesk_delete_contact(cred, contact_id):
    """
    Delete a specific contact.

    :domain: The Freshdesk domain for the account.
    :contact_id: The ID of the contact to be deleted.
    :params: A dictionary containing parameters:

        - :user: (str, required) - The username for authentication.
        - :pwd: (str, required) - same value of username.

    Returns:
      dict: A dictionary containing information about the status of the deletion.

    """
    try:
        creds=json.loads(cred)
        domain=creds['domain']
        url = f"https://{domain}.freshdesk.com/api/v2/contacts/{contact_id}"
        if ".freshdesk.com" in domain:
                raise Exception(f"Invalid URL detected. Please verify your domain name. Domain: {domain}, URL: {url}")
        if "apiKey" in creds:
            user = creds["apiKey"]
            pwd = creds["apiKey"]
            response = requests.delete(url, auth=(user, pwd))
            successStatus= [200,201,202,204,206,207,208]
            if response.status_code in successStatus:
                return {"Result": f"Deleted contact ID: {contact_id}"}
            else:
                raise Exception(
                    f"Failed to delete the contact. Status code: {response.status_code}"
                )

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Domain OR Id Not Found")
        else:
            raise Exception(e)


def freshdesk_update_contact(cred, contact_id, params):
    """
    Update an existing contact.

    :domain: The Freshdesk domain for the account.
    :contact_id: The ID of the contact to be updated.
    :params: A dictionary containing parameters:

        - :user: (str, required) - The username for authentication.
        - :pwd: (str, required) - same value of username.
        - (Additional parameters): Other parameters to be updated, such as email, other_emails, etc.
        
    Returns:
      dict: A dictionary containing information about the updated contact.

    """
    try:
        creds=json.loads(cred)
        domain=creds['domain']
        url = f"https://{domain}.freshdesk.com/api/v2/contacts/{contact_id}"
        if ".freshdesk.com" in domain:
                raise Exception(f"Invalid URL detected. Please verify your domain name. Domain: {domain}, URL: {url}")
        if "apiKey" in creds:
            user = creds["apiKey"]
            pwd = creds["apiKey"]
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            response = requests.put(url, auth=(user, pwd), json=data)
            result = response.json()
            for item in result:
                if item == "errors" or item == "code" or item == "message":
                    raise Exception(result)
            return result
        else:
            raise SyntaxError("Missing input data")

    except Exception as e:
        if "Expecting value" in str(e):
            raise Exception("Invalid Domain OR Id Not Found")
        else:
            raise Exception(e)