import requests
import json

def freshsales_get_many_account(cred,params):
    """
    Fetches multiple accounts from Freshsales based on the provided parameters.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :view_id: (string,required) - The view ID for fetching specific account information.

    Returns:
        dict: A dictionary containing the account information fetched from Freshsales.

    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "view_id" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            view_id = params["view_id"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/sales_accounts/view/{view_id}"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Failed to Retrieve many accounts. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_get_account(cred,params):
    """
    Fetches an account from Freshsales based on the provided account ID.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :account_id: (string,required) - The ID of the account to fetch.

    Returns:
        dict: A dictionary containing the account information fetched from Freshsales.

    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "account_id" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            account_id = params["account_id"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/sales_accounts/{account_id}"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Failed to Retrieve account. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_create_account(cred,params):
    """
    Creates an account in Freshsales.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

  - :name: (string,required) - Name of the account.
  - :address: (string,optional) - Address of the account.
  - :annual_revenue: (float,optional) - Annual revenue of the account.
  - :business_type_id: (string,optional) - ID of the business that the account belongs to.
  - :city: (string,optional) - City that the account belongs to.
  - :country: (string,optional) - Country that the account belongs to.
  - :facebook: (string,optional) - Facebook username of the account
  - :industry_type_id: (string,optional) - ID of the industry that the account belongs to
  - :linkedin: (string,optional) - LinkedIn account of the account
  - :number_of_employees: (int,optional) - Number of employees in the account
  - :owner_id: (string,optional) - ID of the user to whom the account has been assigned
  - :parent_sales_account_id: (string,optional) - Parent account id of the account
  - :phone: (string,optional) - Phone number of the account
  - :state: (string,optional) - State that the account belongs to
  - :territory_id: (string,optional) - ID of the territory that the account belongs to
  - :twitter: (string,optional) - Twitter username of the account
  - :website: (string,optional) - Website of the account
  - :zipcode: (string,optional) - Zipcode of the region that the account belongs to

    Returns:
        dict: A dictionary containing the newly created account information from Freshsales.

    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "name" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/sales_accounts"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            response = requests.post(url, headers=headers, json=data)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Failed to create account. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_update_account(cred,params):
    """
    Updates an account in Freshsales.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :account_id: (string,required) - The ID of the account.
    - :name: (string,optional) - Name of the account.
    - :address: (string,optional) - Address of the account.
    - :annual_revenue: (float,optional) - Annual revenue of the account.
    - :business_type_id: (string,optional) - ID of the business that the account belongs to.
    - :city: (string,optional) - City that the account belongs to.
    - :country: (string,optional) - Country that the account belongs to.
    - :facebook: (string,optional) - Facebook username of the account
    - :industry_type_id: (string,optional) - ID of the industry that the account belongs to
    - :linkedin: (string,optional) - LinkedIn account of the account
    - :number_of_employees: (int,optional) - Number of employees in the account
    - :owner_id: (string,optional) - ID of the user to whom the account has been assigned
    - :parent_sales_account_id: (string,optional) - Parent account id of the account
    - :phone: (string,optional) - Phone number of the account
    - :state: (string,optional) - State that the account belongs to
    - :territory_id: (string,optional) - ID of the territory that the account belongs to
    - :twitter: (string,optional) - Twitter username of the account
    - :website: (string,optional) - Website of the account
    - :zipcode: (string,optional) - Zipcode of the region that the account belongs to

    Returns:
        dict: A dictionary containing the updated account information from Freshsales.

    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "account_id" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            account_id = params["account_id"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/sales_accounts/{account_id}"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            response = requests.put(url, headers=headers, json=data)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Failed to update account. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def freshsales_delete_account(cred,params):
    """
    Deletes an account from Freshsales.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :account_id: (string,required) - The ID of the account

    Returns:
        dict: A dictionary containing a success message if the account is deleted successfully.

    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "account_id" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            account_id = params["account_id"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/sales_accounts/{account_id}"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            response = requests.delete(url, headers=headers)
            if response:
                return {"message": f"Account deleted successfully."}
            else:
                raise Exception(
                    f"Failed to delete account. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_get_many_appointment(cred,params):
    """
    Fetches multiple appointments from Freshsales based on the provided parameters.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :include: (string,optional) - Include additional data with appointments(create or targetable or appointment_attendees)
    - :filter: (string,optional) - Filter appointments by status (upcoming or past)


    Returns:
        dict: A dictionary containing the appointment information fetched from Freshsales.

    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/appointments"
            if "filter" in params and "include" in params:
                filter_value = params["filter"]
                include_value = params["include"]
                url += f"?filter={filter_value}&include={include_value}"
            elif "filter" in params:
                filter_value = params["filter"]
                url += f"?filter={filter_value}"
            elif "include" in params:
                include_value = params["include"]
                url += f"?include={include_value}"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Failed to fetch appointments. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def freshsales_get_appointment(cred,params):
    """
    Retrieve appointment details including attendees, users, and contacts.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :appointment_id: (string,required) - The ID of the appointment to fetch.

    Returns:
        dict: A dictionary containing the appointment details.

    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "appointment_id" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            appointment_id = params["appointment_id"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/appointments/{appointment_id}"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Failed to Retrieve appointment. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_create_appointment(cred,params):
    """
    Creates an appointment in Freshsales.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :title: (string,required) - Title of the appointment
    - :from_date: (datetime/date,required) - Timestamp that denotes the start of appointment/Start date if this is an all day appointment
    - :end_date: (datetime/date,required) - Timestamp that denotes the end of appointment/End date if this is an all day appointment
    - :appointment_attendees_attributes: (List,optional) - 

        Each attendee should be represented as a dictionary with
        
        keys "attendee_type"(user or contact) and "attendee_id".

    - :creater_id: (string,optional) - ID of the user who created the appointment
    - :is_allday: (boolean,optional) - Specifies if appoinment is an all day appointment or not, default value is false. It is a mandatory attribute for all day appointment.
    - :latitude: (string,optional) - Latitude of the location when you check in for an appointment
    - :location: (string,optional) - Location of the appointment.
    - :longitude: (string,optional) - Longitude of the location when you check in for an appointment
    - :outcome_id: (string,optional) - ID of outcome of Appointment sales activity type
    - :targetable_id: (string,optional) - ID of contact/account against whom appointment has been created.
    - :targetable_type: (string,optional) - String that denotes against which entity appointment has been created.

        Possible values are either "Contact" or "SalesAccount" or "Deal".

    - :time_zone: (string,optional) - Timezone that the appointment is scheduled in

    Returns:
        dict: A dictionary containing the newly created appointment information from Freshsales.

    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "title" in params and "from_date" in params and "end_date" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/appointments"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            response = requests.post(url, headers=headers, json=data)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Failed to create appointment. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_update_appointment(cred,params):
    """
    Updates an appointment in Freshsales.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :appointment_id: (string,required) - The ID of the appointment.
    - :title: (string,optional) - Title of the appointment
    - :from_date: (datetime/date,optional) - Timestamp that denotes the start of appointment/Start date if this is an all day appointment
    - :end_date: (datetime/date,optional) - Timestamp that denotes the end of appointment/End date if this is an all day appointment
    - :appointment_attendees_attributes: (List,optional) - All attendees associated to the appointment.

        "appointment_attendees_attributes":[{"attendee_type":"FdMultitenant::User","attendee_id":"222"},{"attendee_type":"Contact","attendee_id":"115773"}]
    - :creater_id: (string,optional) - ID of the user who created the appointment
    - :is_allday: (boolean,optional) - Specifies if appoinment is an all day appointment or not, default value is false. It is a mandatory attribute for all day appointment.
    - :latitude: (string,optional) - Latitude of the location when you check in for an appointment
    - :location: (string,optional) - Location of the appointment.
    - :longitude: (string,optional) - Longitude of the location when you check in for an appointment
    - :outcome_id: (string,optional) - ID of outcome of Appointment sales activity type
    - :targetable_id: (string,optional) - ID of contact/account against whom appointment has been created.
    - :targetable_type: (string,optional) - String that denotes against which entity appointment has been created.

        Possible values are either "Contact" or "SalesAccount" or "Deal".

    - :time_zone: (string,optional) - Timezone that the appointment is scheduled in

    Returns:
        dict: A dictionary containing the updated appointment information from Freshsales.

    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "appointment_id" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            appointment_id = params["appointment_id"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/appointments/{appointment_id}"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            response = requests.put(url, headers=headers, json=data)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Failed to update appointment. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_delete_appointment(cred,params):
    """
    Deletes an appointment from Freshsales.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :appointment_id: (string,required) - The ID of the appointment

    Returns:
        dict: A dictionary containing a success message if the appointment is deleted successfully.

    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "appointment_id" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            appointment_id = params["appointment_id"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/appointments/{appointment_id}"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            response = requests.delete(url, headers=headers)
            if response:
                return {"message": "Appointment deleted successfully."}
            else:
                raise Exception(
                    f"Failed to delete appointment. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_get_many_contact(cred,params):
    """
    Fetches multiple contacts from Freshsales based on the provided parameters.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :view_id: (string,required) - The view ID for fetching specific contact information.

    Returns:
        dict: A dictionary containing the contact information fetched from Freshsales.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "view_id" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            view_id = params["view_id"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/contacts/view/{view_id}"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Failed to fetch contacts. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_get_contact(cred,params):
    """
    Fetches an contact from Freshsales based on the provided contact ID.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :contact_id: (string,required) - The ID of the contact to fetch.

    Returns:
        dict: A dictionary containing the contact information fetched from Freshsales.

    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "contact_id" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            contact_id = params["contact_id"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/contacts/{contact_id}"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Failed to Retrieve contact. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_create_contact(cred,params):
    """
    Creates an contact in Freshsales.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :first_name: (string,required) - First name of the contact
    - :last_name: (string,required) - Last name of the contact
    - :email: (string,required) - Primary email address of the contact
    - :address: (string,optional) - Address of the contact
    - :campaign_id: (string,optional) - The campaign that led your contact to your web app.
    - :city: (string,optional) - City that the contact belongs to
    - :contact_status_id: (string,optional) - ID of the contact status that the contact belongs to
    - :country: (string,optional) - Country that the contact belongs to
    - :external_id: (string,optional) - External ID of the contact
    - :facebook: (string,optional) - Facebook username of the contact
    - :job_title: (string,optional) - Designation of the contact in the account he belongs to
    - :keyword: (string,optional) - The keywords that the contact used to reach your website/web app
    - :lead_source_id: (string,optional) - ID of the source where contact came from
    - :lifecycle_stage_id: (string,optional) - ID of the lifecycle stage that the contact belongs to
    - :linkedin: (string,optional) - LinkedIn account of the contact
    - :medium: (string,optional) - The medium that led your contact to your website/ web app
    - :mobile_number: (string,optional) - Mobile phone number of the contact
    - :owner_id: (string,optional) - ID of the user to whom the contact has been assigned
    - :sales_account_id: (string,optional) - ID of the primary account that the contact belongs to
    - :state: (string,optional) - State that the contact belongs to
    - :subscription_status: (Array of hashes,optional) - Status of subscription that the contact is in
    - :subscription_types: (Array of hashes,optional) - Type of subscription that the contact is in. We have 5 default options:
    
            i. Newsletter (id : 2)
            ii. Promotional (id : 3)
            iii. Product updates (id : 4)
            iv. Confrences & Events (id : 5)
            v. Non-marketing emails from our company (id : 1)
    - :territory_id: (string,optional) - ID of the territory that the contact belongs to
    - :time_zone: (string,optional) - Timezone that the contact belongs to
    - :twitter: (string,optional) - Twitter username of the contact
    - :work_number: (string,optional) - Work phone number of the contact
    - :zipcode: (string,optional) - Zipcode of the region that the contact belongs to

    Returns:
        dict: A dictionary containing the newly created contact information from Freshsales.

    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "first_name" in params and "last_name" in params and "email" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/contacts"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            response = requests.post(url, headers=headers, json=data)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Failed to create contact. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_update_contact(cred,params):
    """
    Updates an contact in Freshsales.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :contact_id: (string,required) - The ID of the contact.
    - :first_name: (string,optional) - First name of the contact
    - :last_name: (string,optional) - Last name of the contact
    - :email: (string,optional) - Primary email address of the contact
    - :address: (string,optional) - Address of the contact
    - :campaign_id: (string,optional) - The campaign that led your contact to your web app.
    - :city: (string,optional) - City that the contact belongs to
    - :contact_status_id: (string,optional) - ID of the contact status that the contact belongs to
    - :country: (string,optional) - Country that the contact belongs to
    - :external_id: (string,optional) - External ID of the contact
    - :facebook: (string,optional) - Facebook username of the contact
    - :job_title: (string,optional) - Designation of the contact in the account he belongs to
    - :keyword: (string,optional) - The keywords that the contact used to reach your website/web app
    - :lead_source_id: (string,optional) - ID of the source where contact came from
    - :lifecycle_stage_id: (string,optional) - ID of the lifecycle stage that the contact belongs to
    - :linkedin: (string,optional) - LinkedIn account of the contact
    - :medium: (string,optional) - The medium that led your contact to your website/ web app
    - :mobile_number: (string,optional) - Mobile phone number of the contact
    - :owner_id: (string,optional) - ID of the user to whom the contact has been assigned
    - :sales_account_id: (string,optional) - ID of the primary account that the contact belongs to
    - :state: (string,optional) - State that the contact belongs to
    - :subscription_status: (Array of hashes,optional) - Status of subscription that the contact is in
    - :subscription_types: (Array of hashes,optional) - Type of subscription that the contact is in. We have 5 default options:
            i. Newsletter (id : 2)
            ii. Promotional (id : 3)
            iii. Product updates (id : 4)
            iv. Confrences & Events (id : 5)
            v. Non-marketing emails from our company (id : 1)
    - :territory_id: (string,optional) - ID of the territory that the contact belongs to
    - :time_zone: (string,optional) - Timezone that the contact belongs to
    - :twitter: (string,optional) - Twitter username of the contact
    - :work_number: (string,optional) - Work phone number of the contact
    - :zipcode: (string,optional) - Zipcode of the region that the contact belongs to      

    Returns:
        dict: A dictionary containing the updated contact information from Freshsales.

    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "contact_id" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            contact_id = params["contact_id"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/contacts/{contact_id}"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            response = requests.put(url, headers=headers, json=data)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Failed to update contact. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_delete_contact(cred,params):
    """
    Deletes an contact from Freshsales.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :contact_id: (string,required) - The ID of the contact

    Returns:
        dict: A dictionary containing a success message if the contact is deleted successfully.

    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "contact_id" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            contact_id = params["contact_id"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/contacts/{contact_id}"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            response = requests.delete(url, headers=headers)
            if response:
                return {"message": "Contact deleted successfully."}
            else:
                raise Exception(
                    f"Failed to delete contact. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_get_many_deal(cred,params):
    """
    Fetches multiple deals from Freshsales based on the provided parameters.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :view_id: (string,required) - The view ID for fetching specific deal information.

    Returns:
        dict: A dictionary containing the deal information fetched from Freshsales.

    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "view_id" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            view_id = params["view_id"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/deals/view/{view_id}"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Failed to Retrieve many deals. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_get_deal(cred,params):
    """
    Fetches an deal from Freshsales based on the provided deal ID.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :deal_id: (string,required) - The ID of the deal to fetch.

    Returns:
        dict: A dictionary containing the deal information fetched from Freshsales.

    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "deal_id" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            deal_id = params["deal_id"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/deals/{deal_id}"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Failed to Retrieve deal. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_create_deal(cred,params):
    """
    Creates an deal in Freshsales.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :name: (string,required) - Name of the deal
    - :amount: (float,required) - Value of the deal
    - :base_currency_amount: (float,optional) - Value of the deal in base currency
    - :campaign_id: (string,optional) - ID of the campaign that landed this deal
    - :currency_id: (string,optional) - ID of the currency that the deal belongs to
    - :deal_payment_status_id: (string,optional) - ID of the mode of payment for the deal
    - :deal_pipeline_id: (string,optional) - ID of the deal pipeline that it belongs to
    - :deal_reason_id: (string,optional) - ID of the deal reason - Reason for losing the deal
    - :deal_stage_id: (string,optional) - ID of the deal stage that the deal belongs to
    - :deal_type_id: (string,optional) - ID of the deal type that the deal belongs to
    - :lead_source_id: (string,optional) - ID of the source where deal came from
    - :owner_id: (string,optional) - ID of the user to whom the deal has been assigned
    - :probability: (int,optional) - (>=0 and <=100)	The probability of winning the deal
    - :sales_account_id: (string,optional) - ID of the account that the deal belongs to
    - :territory_id: (string,optional) - ID of the territory that the deal belongs to

    Returns:
        dict: A dictionary containing the newly created deal information from Freshsales.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "name" in params and "amount" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/deals"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            response = requests.post(url, headers=headers, json=data)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Failed to create deal. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_update_deal(cred,params):
    """
    Updates an deal in Freshsales.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :deal_id: (string,required) - The ID of the deal.
    - :name: (string,optional) - Name of the deal
    - :amount: (float,optional) - Value of the deal
    - :base_currency_amount: (float,optional) - Value of the deal in base currency
    - :campaign_id: (string,optional) - ID of the campaign that landed this deal
    - :currency_id: (string,optional) - ID of the currency that the deal belongs to
    - :deal_payment_status_id: (string,optional) - ID of the mode of payment for the deal
    - :deal_pipeline_id: (string,optional) - ID of the deal pipeline that it belongs to
    - :deal_reason_id: (string,optional) - ID of the deal reason - Reason for losing the deal
    - :deal_stage_id: (string,optional) - ID of the deal stage that the deal belongs to
    - :deal_type_id: (string,optional) - ID of the deal type that the deal belongs to
    - :lead_source_id: (string,optional) - ID of the source where deal came from
    - :owner_id: (string,optional) - ID of the user to whom the deal has been assigned
    - :probability: (int,optional) - (>=0 and <=100)	The probability of winning the deal
    - :sales_account_id: (string,optional) - ID of the account that the deal belongs to
    - :territory_id: (string,optional) - ID of the territory that the deal belongs to

    Returns:
        dict: A dictionary containing the updated deal information from Freshsales.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "deal_id" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            deal_id = params["deal_id"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/deals/{deal_id}"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            response = requests.put(url, headers=headers, json=data)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Failed to update deal. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_delete_deal(cred,params):
    """
    Deletes an deal from Freshsales.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :deal_id: (string,required) - The ID of the deal

    Returns:
        dict: A dictionary containing a success message if the deal is deleted successfully.

    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "deal_id" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            deal_id = params["deal_id"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/deals/{deal_id}"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            response = requests.delete(url, headers=headers)
            if response:
                return {"message": "Deal deleted successfully."}
            else:
                raise Exception(
                    f"Failed to delete deal. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_create_note(cred,params):
    """
    Creates an note in Freshsales.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :description: (string,required) - Description of the note
    - :targetable_id: (string,required) - ID of contact/account against whom note has been created
    - :targetable_type: (string,required) - String that denotes against which entity note has been created.

        Possible values are either "Contact" or "SalesAccount" or "Deal".

    Returns:
        dict: A dictionary containing the newly created note information from Freshsales.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "description" in params and "targetable_id" in params and "targetable_type" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/notes"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            response = requests.post(url, headers=headers, json=data)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Failed to create note. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_update_note(cred,params):
    """
    Updates an note in Freshsales.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :note_id: (string,required) - The ID of the note.
    - :description: (string,optional) - Description of the note
    - :targetable_id: (string,optional) - ID of contact/account against whom note has been created
    - :targetable_type: (string,optional) - String that denotes against which entity note has been created.

        Possible values are either "Contact" or "SalesAccount" or "Deal".

    Returns:
        dict: A dictionary containing the updated note information from Freshsales.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "note_id" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            note_id = params["note_id"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/notes/{note_id}"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            response = requests.put(url, headers=headers, json=data)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Failed to update note. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_delete_note(cred,params):
    """
    Deletes an note from Freshsales.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :note_id: (string,required) - The ID of the note

    Returns:
        dict: A dictionary containing a success message if the note is deleted successfully.

    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "note_id" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            note_id = params["note_id"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/notes/{note_id}"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            response = requests.delete(url, headers=headers)
            if response:
                return {"message": "Note deleted successfully."}
            else:
                raise Exception(
                    f"Failed to delete note. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_get_many_sales_activity(cred):
    """
    Retrieves multiple sales activities from Freshsales based on the provided parameters.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.

    Returns:
        dict: A dictionary containing the sales activities fetched from Freshsales.

    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/sales_activities"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Failed to Retrieve many sales activities. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_get_sales_activity(cred,params):
    """
    Retrieves sales activity from Freshsales based on the provided sales activity ID.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :sales_activity_id: (string,required) - The ID of the deal to fetch.

    Returns:
        dict: A dictionary containing the sales activity information fetched from Freshsales.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "sales_activity_id" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            sales_activity_id = params["sales_activity_id"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/sales_activities/{sales_activity_id}"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Failed to Retrieve sales activity. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_search_by_query(cred,params):
    """
    Searches for entities in Freshsales based on the provided query.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :query: (string,required) - The search query
    - :entities: (string,required) - Comma-separated string of entities to search within (e.g., "contact,deal,sales_account,user").

    Returns:
        dict: A dictionary containing the search results fetched from Freshsales.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "query" in params and "entities" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            query = params["query"]
            entities = params["entities"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/search?q={query}&include={entities}"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Failed to fetch search results. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_lookup_by_field(cred,params):
    """
    Searches for the name or email address of records

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :search_field: (string,required) - The field to search by (e.g., "email","name","custom field").
    - :field_value: (string,required) - The value to search for in the specified field.
    - :entities: (string,required) - Comma-separated string of entities to search within (e.g., "contact,deal,sales_account").

    Returns:
        dict: A dictionary containing the search results fetched from Freshsales.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "search_field" in params and "field_value" in params and "entities" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            search_field = params["search_field"]
            field_value = params["field_value"]
            entities = params["entities"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/lookup?q={field_value}&f={search_field}&entities={entities}"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Failed to fetch search results. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_get_many_task(cred,params):
    """
    Fetches multiple tasks from Freshsales based on the provided parameters.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :include: (string,optional) - Include additional additional details in the response.(users or targetable or owner)
    - :filter: (string,optional) - Filter tasks by status (completed or overdue or open)

    Returns:
        dict: A dictionary containing the task information fetched from Freshsales.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/tasks"
            if "filter" in params and "include" in params:
                filter_value = params["filter"]
                include_value = params["include"]
                url += f"?filter={filter_value}&include={include_value}"
            elif "filter" in params:
                filter_value = params["filter"]
                url += f"?filter={filter_value}"
            elif "include" in params:
                include_value = params["include"]
                url += f"?include={include_value}"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Failed to fetch tasks. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_get_task(cred,params):
    """
    Fetches an task from Freshsales based on the provided task ID.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :task_id: (string,required) - The ID of the task to fetch.

    Returns:
        dict: A dictionary containing the task information fetched from Freshsales.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "task_id" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            task_id = params["task_id"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/tasks/{task_id}"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Failed to Retrieve task. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_create_task(cred,params):
    """
    Creates an task in Freshsales.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :title: (string,required) - Title of the task
    - :due_date: (datetime,required) - Timestamp that denotes when the task is due to be completed
    - :owner_id: (string,required) - ID of the user to whom the task has been assigned
    - :targetable_type: (string,required) - String that denotes against which entity task has been created.

        Possible values are either "Contact" or "SalesAccount" or "Deal"
    - :targetable_id: (string,required) - ID of contact/account against whom task has been created
    - :creater_id: (string,optional) - ID of the user who created the task
    - :outcome_id: (string,optional) - ID of outcome of Task sales activity type
    - :task_type_id: (string,optional) - ID of type of Task sales activity type

    Returns:
        dict: A dictionary containing the newly created task information from Freshsales.
    """
    try:
        creds = json.loads(cred)
        required_params = ['title', 'due_date','owner_id', 'targetable_type', 'targetable_id']
        if all(param in params for param in required_params) and "domain" in creds and "apiKey" in creds:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/tasks"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            response = requests.post(url, headers=headers, json=data)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Failed to create task. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_update_task(cred,params):
    """
    Updates an task in Freshsales.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :task_id: (string,required) - The ID of the task.
    - :title: (string,optional) - Title of the task
    - :due_date: (datetime,optional) - Timestamp that denotes when the task is due to be completed
    - :owner_id: (string,optional) - ID of the user to whom the task has been assigned
    - :targetable_type: (string,optional) - String that denotes against which entity task has been created.

        Possible values are either "Contact" or "SalesAccount" or "Deal"
    - :targetable_id: (string,optional) - ID of contact/account against whom task has been created
    - :creater_id: (string,optional) - ID of the user who created the task
    - :outcome_id: (string,optional) - ID of outcome of Task sales activity type
    - :task_type_id: (string,optional) - ID of type of Task sales activity type

    Returns:
        dict: A dictionary containing the updated task information from Freshsales.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "task_id" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            task_id = params["task_id"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/tasks/{task_id}"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            response = requests.put(url, headers=headers, json=data)
            if response:
                return response.json()
            else:
                raise Exception(
                    f"Failed to update task. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)

def freshsales_delete_task(cred,params):
    """
    Deletes an task from Freshsales.

    :param str domain: The Freshsales domain.
    :param str apiKey: The API key for authentication.
    :param dict params: Dictionary containing parameters.

    - :task_id: (string,required) - The ID of the task

    Returns:
        dict: A dictionary containing a success message if the task is deleted successfully.
    """
    try:
        creds = json.loads(cred)
        if "domain" in creds and "apiKey" in creds and "task_id" in params:
            domain = creds["domain"]
            apiKey = creds["apiKey"]
            task_id = params["task_id"]
            url = f"https://{domain}.myfreshworks.com/crm/sales/api/tasks/{task_id}"
            headers = {
                "Authorization": f"Token token={apiKey}",
                "Content-Type": "application/json"
            }
            response = requests.delete(url, headers=headers)
            if response:
                return {"message": "Task deleted successfully."}
            else:
                raise Exception(
                    f"Failed to delete task. Status code: {response.status_code}, Response: {response.text}")
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)
