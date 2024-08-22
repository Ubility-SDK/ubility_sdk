import xmlrpc.client
import json

def odoo_create_contact(cred,params):
    """
    Create a contact in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :name: (str,required) - The name of the contact.
        - :email: (str,optional) - The email address of the contact.
        - :phone: (str,optional) - The phone number of the contact.
        - :mobile: (str,optional) - The mobile number of the contact.
        - :website: (str,optional) - The website of the contact.
        - :comment: (str,optional) - Additional comments or notes.
        - :function: (str,optional) - The function or role of the contact.
        - :vat: (str,optional) - The vat number of the contact.
        - :city: (str,optional) - The city of the contact.
        - :street: (str,optional) - The street address of the contact.
        - :street2: (str,optional) - Additional street information.
        - :zip: (str,optional) - The postal code of the contact.
        - :country_id: (int,optional) - The ID of the country for the contact
        - :state_id: (int,optional) - The ID of the state or region for the contact.

    Returns:
        dict: A dictionary containing the created contact's ID.
    """
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "name" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "res.partner"
                data = {}
                for key, value in params.items():
                    if value:
                        data[key] = value
                id = models.execute_kw(db, uid, apiPassword, model, "create", [data])
                return {"id": id}
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_get_contact_by_id(cred,params):
    """
    Get contact details from Odoo by contact ID.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :contact_id: (int,required) - The ID of the contact.
        - :fields: (list,optional) - List of fields to include in the response.
            Available fields: name, email, phone, mobile, website, comment, function, vat, city, country_id, state_id, street, street2, zip.

    Returns:
        dict: Contact details.
    """
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "contact_id" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            id = params.get("contact_id")
            fields = params.get("fields", [])
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "res.partner"
                data = models.execute_kw(
                    db, uid, apiPassword, model, "read", [int(id)], {"fields": fields}
                )
                if data:
                    return {"Contact": data}
                else:
                    raise Exception("Not found")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_get_many_contact(cred,params):
    """
    Get multiple contacts from Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :limit: (int,optional) - The maximum number of contacts to retrieve.
        - :fields: (list,optional) - List of fields to include in the response.
            Available fields: name, email, phone, mobile, website, comment, function, vat,city, country_id, state_id, street, street2, zip.

    Returns:
        dict: A dictionary containing the retrieved contacts.
    """
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds :
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            limit = params.get("limit")
            fields = params.get("fields", [])
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "res.partner"
                ids = models.execute_kw(db, uid, apiPassword, model, "search", [[]])
                data = models.execute_kw(
                    db, uid, apiPassword, model, "read", [ids], {"fields": fields}
                )
                return {"Contacts": data[:limit]}
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_delete_contact(cred,params):
    """
    Delete a contact in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :contact_id: (int,required) - The ID of the contact.

    Returns:
        dict: A confirmation message indicating successful deletion.
    """
    
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "contact_id" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            id = params.get("contact_id")
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "res.partner"
                if models.execute_kw(
                    db, uid, apiPassword, model, "search", [[("id", "=", int(id))]]
                ):
                    models.execute_kw(db, uid, apiPassword, model, "unlink", [[id]])
                    return {"message": "Deleted successfully"}
                else:
                    raise Exception("ID not found or could not be deleted.")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_update_contact(cred,params):
    """
    Update a contact in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :contact_id: (int,required) - The ID of the contact.
        - :name: (str,optional) - The name of the contact.
        - :email: (str,optional) - The email address of the contact.
        - :phone: (str,optional) - The phone number of the contact.
        - :mobile: (str,optional) - The mobile number of the contact.
        - :website: (str,optional) - The website of the contact.
        - :comment: (str,optional) - Additional comments or notes.
        - :function: (str,optional) - The function or role of the contact.
        - :vat: (str,optional) - The vat number of the contact.
        - :city: (str,optional) - The city of the contact.
        - :street: (str,optional) - The street address of the contact.
        - :street2: (str,optional) - Additional street information.
        - :zip: (str,optional) - The postal code of the contact.
        - :country_id: (int,optional) - The ID of the country for the contact
        - :state_id: (int,optional) - The ID of the state or region for the contact.

    Returns:
        dict: A confirmation message indicating successful of the update.
    """
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "contact_id" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            id = params["contact_id"]
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "res.partner"
                data = {}
                for key, value in params.items():
                    skip_keys = ["contact_id"]
                    if key in skip_keys:
                        continue
                    if value:
                        data[key] = value
                if data:
                    if models.execute_kw(
                        db, uid, apiPassword, model, "search", [[("id", "=", int(id))]]
                    ):
                        models.execute_kw(
                            db, uid, apiPassword, model, "write", [[int(id)], data]
                        )
                        return {"message": "Updated successfully"}
                    else:
                        raise Exception("Not found")
                else:
                    raise Exception("Please specify at least one field to update")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_create_user(cred,params):
    """
    Create a user in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :name: (str,required) - The name of the user.
        - :login: (str,required) - The email address of the user.
            
    Returns:
        dict: A dictionary containing the created user's ID.
    """
    
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "name" in params and "login" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "res.users"
                data = {}
                for key, value in params.items():
                    if value:
                        data[key] = value
                id = models.execute_kw(db, uid, apiPassword, model, "create", [data])
                return {"id": id}
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_get_user_by_id(cred,params):
    """
    Get user details from Odoo by user ID.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :user_id: (int,required) - The ID of the user.
        - :fields: (list,optional) - List of fields to include in the response.
            Available fields: name, email, opportunity_count .

    Returns:
        dict: User details.
    """
    
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "user_id" in params :
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            id = params.get("user_id")
            fields = params.get("fields", [])
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "res.users"
                data = models.execute_kw(
                    db, uid, apiPassword, model, "read", [int(id)], {"fields": fields}
                )
                if data:
                    return {"User": data}
                else:
                    raise Exception("Not found")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_get_many_users(cred,params):
    """
    Get multiple users from Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :limit: (int,optional) - The maximum number of users to retrieve.
        - :fields: (list,optional) - List of fields to include in the response.
            Available fields: name, email, opportunity_count .

    Returns:
        dict: A dictionary containing the retrieved users.
    """
    
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds :
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            limit = params.get("limit")
            fields = params.get("fields", [])
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "res.users"
                ids = models.execute_kw(db, uid, apiPassword, model, "search", [[]])
                data = models.execute_kw(
                    db, uid, apiPassword, model, "read", [ids], {"fields": fields}
                )
                return {"Users": data[:limit]}
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_delete_user(cred,params):
    """
    Delete a user in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :user_id: (int,required) - The ID of the user.

    Returns:
        dict: A confirmation message indicating successful deletion.
    """

    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "user_id" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            id = params.get("user_id")
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "res.users"
                if models.execute_kw(
                    db, uid, apiPassword, model, "search", [[("id", "=", int(id))]]
                ):
                    models.execute_kw(db, uid, apiPassword, model, "unlink", [[id]])
                    return {"message": "Deleted successfully"}
                else:
                    raise Exception("ID not found or could not be deleted.")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_update_user(cred,params):
    """
    Update a user in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :user_id: (int,required) - The ID of the user.
        - :name: (str,optional) - The name of the user.
        - :login: (str,optional) - The email address of the user.

    Returns:
        dict: A confirmation message indicating successful of the update.
    """
    
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "user_id" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            id = params["user_id"]
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "res.users"
                data = {}
                for key, value in params.items():
                    skip_keys = ["user_id"]
                    if key in skip_keys:
                        continue
                    if value:
                        data[key] = value
                if data:
                    if models.execute_kw(
                        db, uid, apiPassword, model, "search", [[("id", "=", int(id))]]
                    ):
                        models.execute_kw(
                            db, uid, apiPassword, model, "write", [[int(id)], data]
                        )
                        return {"message": "Updated successfully"}
                    else:
                        raise Exception("Not found")
                else:
                    raise Exception("Please specify at least one field to update")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_create_opportunity(cred,params):
    """
    Create a new opportunity in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

     - :name: (str,required) - The name of the opportunity.
     - :partner_id: (int,optional) - ID of the partner associated with the opportunity.
     - :user_id: (int,optional) - ID of the user responsible for the opportunity.
     - :email_form: (str,optional) - Email address associated with the opportunity.
     - :expected_revenue: (float,optional) - Expected revenue for the opportunity.
     - :recurring_revenue_monthly: (float,optional) - Recurring revenue 
     
        per month for the opportunity.
     - :description: (str,optional) - Description or notes for the opportunity.
     - :phone: (str,optional) - Phone number associated with the opportunity.
     - :probability: (float,optional) - Probability of closing the opportunity (in percentage).
     - :date_deadline: (date,optional) - Deadline or closing date for the opportunity (in "YYYY-MM-DD" format).
     - :tag_ids: (list,optional) - List of tag IDs associated with the opportunity.
     - :priority: (int,optional) - Priority of the opportunity (1, 2, or 3).
            
    Returns:
        dict: A dictionary containing the ID of the created opportunity.
    """
    
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "name" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "crm.lead"
                data = {}
                for key, value in params.items():
                    if value:
                        data[key] = value
                id = models.execute_kw(db, uid, apiPassword, model, "create", [data])
                return {"id": id}
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_get_opportunity_by_id(cred,params):
    """
    Get opportunity details from Odoo by opportunity ID.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :opportunity_id: (int,required) - The ID of the opportunity.
        - :fields: (list,optional) - List of fields to include in the response.
            Available fields: name, email_normalized, expected_revenue , description , phone , priority , probability .

    Returns:
        dict: Opportunity details.
    """
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "opportunity_id" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            id = params.get("opportunity_id")
            fields = params.get("fields", [])
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "crm.lead"
                data = models.execute_kw(
                    db, uid, apiPassword, model, "read", [int(id)], {"fields": fields}
                )
                if data:
                    return {"Opportunity": data}
                else:
                    raise Exception("Not found")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_get_many_opportunity(cred,params):
    """
    Get multiple opportunities from Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :limit: (int,optional) - The maximum number of opportunities to retrieve.
        - :fields: (list,optional) - List of fields to include in the response.
            Available fields: name, email_normalized, expected_revenue , description , phone , priority , probability .

    Returns:
        dict: A dictionary containing the retrieved opportunities.
    """
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds :
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            limit = params.get("limit")
            fields = params.get("fields", [])
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "crm.lead"
                ids = models.execute_kw(db, uid, apiPassword, model, "search", [[]])
                data = models.execute_kw(
                    db, uid, apiPassword, model, "read", [ids], {"fields": fields}
                )
                return {"Opportunities": data[:limit]}
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_delete_opportunity(cred,params):
    """
    Delete a opportunity in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :opportunity_id: (int,required) - The ID of the opportunity.

    Returns:
        dict: A confirmation message indicating successful deletion.
    """
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "opportunity_id" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            id = params.get("opportunity_id")
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "crm.lead"
                if models.execute_kw(
                    db, uid, apiPassword, model, "search", [[("id", "=", int(id))]]
                ):
                    models.execute_kw(db, uid, apiPassword, model, "unlink", [[id]])
                    return {"message": "Deleted successfully"}
                else:
                    raise Exception("ID not found or could not be deleted.")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_update_opportunity(cred,params):
    """
    Update a opportunity in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

     - :opportunity_id: (int,required) - The ID of the opportunity.
     - :name: (str,optional) - The name of the opportunity.
     - :expected_revenue: (float,optional) - Expected revenue for the opportunity.
     - :description: (str,optional) - Description or notes for the opportunity.
     - :phone: (str,optional) - Phone number associated with the opportunity.
     - :probability: (float,optional) - Probability of closing the opportunity (in percentage).
     - :priority: (int,optional) - Priority of the opportunity (1, 2, or 3).
     - :date_deadline: (date,optional) - Deadline or closing date for the opportunity (in "YYYY-MM-DD" format).

    Returns:
        dict: A confirmation message indicating successful of the update.
    """
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "opportunity_id" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            id = params["opportunity_id"]
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "crm.lead"
                data = {}
                for key, value in params.items():
                    skip_keys = ["opportunity_id"]
                    if key in skip_keys:
                        continue
                    if value:
                        data[key] = value
                if data:
                    if models.execute_kw(
                        db, uid, apiPassword, model, "search", [[("id", "=", int(id))]]
                    ):
                        models.execute_kw(
                            db, uid, apiPassword, model, "write", [[int(id)], data]
                        )
                        return {"message": "Updated successfully"}
                    else:
                        raise Exception("Not found")
                else:
                    raise Exception("Please specify at least one field to update")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_create_sales_team(cred,params):
    """
    Create a new sales team in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :name: (str,required) - The name of the sales team.
        - :alias_name: (str,optional) - Alias name for the sales team.
        - :user_id: (int,optional) - The ID of the team leader.
        - :invoiced_target: (float,optional) - Invoicing target per month for the sales team.
        - :alias_contact: (str,optional) - Alias contact setting ("everyone", "partners", or "followers").
            
    Returns:
        dict: A dictionary containing the ID of the created sales team.
    """
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "name" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "crm.team"
                data = {}
                for key, value in params.items():
                    if value:
                        data[key] = value
                id = models.execute_kw(db, uid, apiPassword, model, "create", [data])
                return {"id": id}
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_get_sales_team_by_id(cred,params):
    """
    Get sales team details from Odoo by sales team ID.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :sales_team_id: (int,required) - The ID of the sales team.
        - :fields: (list,optional) - List of fields to include in the response.
            Available fields: name, alias_name, alias_email , user_id , opportunities_count , invoiced_target .

    Returns:
        dict: Sales team details.
    """
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "sales_team_id" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            id = params.get("sales_team_id")
            fields = params.get("fields", [])
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "crm.team"
                data = models.execute_kw(
                    db, uid, apiPassword, model, "read", [int(id)], {"fields": fields}
                )
                if data:
                    return {"SalesTeam": data}
                else:
                    raise Exception("Not found")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_get_many_sales_team(cred,params):
    """
    Get multiple sales team from Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :limit: (int,optional) - The maximum number of sales team to retrieve.
        - :fields: (list,optional) - List of fields to include in the response.
            Available fields: name, alias_name, alias_email , user_id , opportunities_count , invoiced_target .

    Returns:
        dict: A dictionary containing the retrieved sales team.
    """

    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds :
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            limit = params.get("limit")
            fields = params.get("fields", [])
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "crm.team"
                ids = models.execute_kw(db, uid, apiPassword, model, "search", [[]])
                data = models.execute_kw(
                    db, uid, apiPassword, model, "read", [ids], {"fields": fields}
                )
                return {"SalesTeams": data[:limit]}
            else:
                raise Exception(
                    {"error": "Authentication failed. Please check your credentials."}
                )
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_delete_sales_team(cred,params):
    """
    Delete a sales team in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :sales_team_id: (int,required) - The ID of the sales team.

    Returns:
        dict: A confirmation message indicating successful deletion.
    """
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "sales_team_id" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            id = params.get("sales_team_id")
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "crm.team"
                if models.execute_kw(
                    db, uid, apiPassword, model, "search", [[("id", "=", int(id))]]
                ):
                    models.execute_kw(db, uid, apiPassword, model, "unlink", [[id]])
                    return {"message": "Deleted successfully"}
                else:
                    raise Exception("ID not found or could not be deleted.")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_update_sales_team(cred,params):
    """
    Update a sales team in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :sales_team_id: (int,required) - The ID of the sales team.
        - :name: (str,optional) - The name of the sales team.
        - :alias_name: (str,optional) - Alias name for the sales team.
        - :invoiced_target: (float,optional) - Invoicing target per month for the sales team.
        - :alias_contact: (str,optional) - Alias contact setting ("everyone", "partners", or "followers").

    Returns:
        dict: A confirmation message indicating successful of the update.
    """
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "sales_team_id" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            id = params["sales_team_id"]
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "crm.team"
                data = {}
                for key, value in params.items():
                    skip_keys = ["sales_team_id"]
                    if key in skip_keys:
                        continue
                    if value:
                        data[key] = value
                if data:
                    if models.execute_kw(
                        db, uid, apiPassword, model, "search", [[("id", "=", int(id))]]
                    ):
                        models.execute_kw(
                            db, uid, apiPassword, model, "write", [[int(id)], data]
                        )
                        return {"message": "Updated successfully"}
                    else:
                        raise Exception("Not found")
                else:
                    raise Exception("Please specify at least one field to update")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_create_sales_team_member(cred,params):
    """
    Create a new sales team member in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :crm_team_id: (str,required) - The ID of the sales team.
        - :user_id: (str,required) - The ID of the sales person.
            
    Returns:
        dict: A dictionary containing the ID of the created sales team member.
    """
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "crm_team_id" in params and "user_id" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "crm.team.member"
                data = {}
                for key, value in params.items():
                    if value:
                        data[key] = value
                id = models.execute_kw(db, uid, apiPassword, model, "create", [data])
                return {"id": id}
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_get_sales_team_member_by_id(cred,params):
    """
    Get sales team member details from Odoo by sales team ID.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :crm_team_id: (int,required) - The ID of the sales team member.
        - :fields: (list,optional) - List of fields to include in the response.
            Available fields: name, crm_team_id, email , user_id , lead_month_count .

    Returns:
        dict: Sales team member details.
    """
    
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "crm_team_id" in params :
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            id = params.get("crm_team_id")
            fields = params.get("fields", [])
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "crm.team.member"
                data = models.execute_kw(
                    db, uid, apiPassword, model, "read", [int(id)], {"fields": fields}
                )
                if data:
                    return {"SalesTeamMember": data}
                else:
                    raise Exception("Not found")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_get_many_sales_team_member(cred,params):
    """
    Get multiple sales team member from Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :limit: (int,optional) - The maximum number of sales team member to retrieve.
        - :fields: (list,optional) - List of fields to include in the response.
            Available fields: name, crm_team_id, email , user_id , lead_month_count .

    Returns:
        dict: A dictionary containing the retrieved sales team member.
    """
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds :
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            limit = params.get("limit")
            fields = params.get("fields", [])
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "crm.team.member"
                ids = models.execute_kw(db, uid, apiPassword, model, "search", [[]])
                data = models.execute_kw(
                    db, uid, apiPassword, model, "read", [ids], {"fields": fields}
                )
                return {"SalesTeamMembers": data[:limit]}
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_delete_sales_team_member(cred,params):
    """
    Delete a sales team member in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :crm_team_id: (int,required) - The ID of the sales team member.

    Returns:
        dict: A confirmation message indicating successful deletion.
    """
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "crm_team_id" in params :
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            id = params.get("crm_team_id")
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "crm.team.member"
                if models.execute_kw(
                    db, uid, apiPassword, model, "search", [[("id", "=", int(id))]]
                ):
                    models.execute_kw(db, uid, apiPassword, model, "unlink", [[id]])
                    return {"message": "Deleted successfully"}
                else:
                    raise Exception("ID not found or could not be deleted.")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_get_many_sale_orders(cred,params):
    """
    Get multiple sales orders from Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :limit: (int,optional) - The maximum number of sales orders to retrieve.
        - :fields: (list,optional) - List of fields to include in the response.
            Available fields: name, partner_id, user_id , team_id , order_line , note .
          
    Returns:
        dict: A dictionary containing the retrieved sales orders.
    """
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds :
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            limit = params.get("limit")
            fields = params.get("fields", [])
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "sale.order"
                ids = models.execute_kw(db, uid, apiPassword, model, "search", [[]])
                data = models.execute_kw(
                    db, uid, apiPassword, model, "read", [ids], {"fields": fields}
                )
                return {"SalesOrders": data[:limit]}
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_create_sale_order(cred,params):
    """
    Create a new sales order in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :partner_id: (str,required) - The ID of the customer (partner) for the sale order.
        - :user_id: (str,required) - The ID of the salesperson responsible for the sale order.
        - :note: (str,optional) - Additional notes or comments for the sale order.
        - :order_lines_data: (list,optional) - List of dictionaries representing the order lines.
            Each dictionary should contain "product_id" and "product_uom_qty" keys. (required)

    Returns:
        dict: A dictionary containing the ID of the created sales order.
    """
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "partner_id" in params and "user_id" in params and "order_lines_data" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            order_lines_data = params.get("order_lines_data")
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "sale.order"
                order_lines = [
                    (
                        0,
                        0,
                        {
                            "product_id": line["product_id"],
                            "product_uom_qty": line["product_uom_qty"],
                        },
                    )
                    for line in order_lines_data
                ]
                data = {
                    "partner_shipping_id": params["partner_id"],
                    "partner_invoice_id": params["partner_id"],
                    "order_line": order_lines,
                }
                for key, value in params.items():
                    skip_keys = ["order_lines_data"]
                    if key in skip_keys:
                        continue
                    if value:
                        data[key] = value
                id = models.execute_kw(db, uid, apiPassword, model, "create", [data])
                return {"id": id}
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_update_sale_order(cred,params):
    """
    Update a sales order in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :order_id: (int,required) - The ID of the sales order.
        - :note: (str,optional) - Additional notes or comments for the sale order.
        - :order_lines_data: (list,optional) - List of dictionaries representing the order lines.
            Each dictionary should contain "product_id" and "product_uom_qty" keys. (required)

    Returns:
        dict: A confirmation message indicating successful of the update.
    """
    
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "order_id" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            id = params["order_id"]
            order_lines_data = params.get("order_lines_data", [])
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            data = {}
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "sale.order"
                if order_lines_data:
                    order_lines = [
                        (
                            0,
                            0,
                            {
                                "product_id": line["product_id"],
                                "product_uom_qty": line["product_uom_qty"],
                            },
                        )
                        for line in order_lines_data
                    ]
                    data = {"order_line": order_lines}
                for key, value in params.items():
                    skip_keys = ["order_id", "order_lines_data"]
                    if key in skip_keys:
                        continue
                    if value:
                        data[key] = value
                if data:
                    if models.execute_kw(
                        db, uid, apiPassword, model, "search", [[("id", "=", int(id))]]
                    ):
                        models.execute_kw(
                            db, uid, apiPassword, model, "write", [[int(id)], data]
                        )
                        return {"message": "Updated successfully"}
                    else:
                        raise Exception("Not found")
                else:
                    raise Exception("Please specify at least one field to update")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_delete_sale_order(cred,params):
    """
    Delete a sales order in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :order_id: (int,required) - The ID of the sales order.

    Returns:
        dict: A confirmation message indicating successful deletion.
    """
    
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "order_id" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            id = params.get("order_id")
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "sale.order"
                if models.execute_kw(
                    db, uid, apiPassword, model, "search", [[("id", "=", int(id))]]
                ):
                    models.execute_kw(db, uid, apiPassword, model, "unlink", [[id]])
                    return {"message": "Deleted successfully"}
                else:
                    raise Exception("ID not found or could not be deleted.")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_get_sale_order_by_id(cred,params):
    """
    Get sales order details from Odoo by sales order ID.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :order_id: (int,required) - The ID of the sales order.
        - :fields: (list,optional) - List of fields to include in the response.
            Available fields: name, partner_id, user_id , team_id , order_line , note .

    Returns:
        dict: Sales order details.
    """
    
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "order_id" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            id = params.get("order_id")
            fields = params.get("fields", [])
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "sale.order"
                data = models.execute_kw(
                    db, uid, apiPassword, model, "read", [int(id)], {"fields": fields}
                )
                if data:
                    return {"SalesOrder": data}
                else:
                    raise Exception("Not found")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_get_many_company(cred,params):
    """
    Get multiple companies from Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :limit: (int,optional) - The maximum number of companies to retrieve.
        - :fields: (list,optional) - List of fields to include in the response.
            Available fields: name, email, phone, mobile, website, vat, city, country_id, state_id, street, street2, zip.

    Returns:
        dict: A dictionary containing the retrieved companies.
    """
    
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds :
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            limit = params.get("limit")
            fields = params.get("fields", [])
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "res.company"
                ids = models.execute_kw(db, uid, apiPassword, model, "search", [[]])
                data = models.execute_kw(
                    db, uid, apiPassword, model, "read", [ids], {"fields": fields}
                )
                return {"Companies": data[:limit]}
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_create_company(cred,params):
    """
    Create a company in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :name: (str,required) - The name of the company.
        - :email: (str,optional) - The email address of the company.
        - :phone: (str,optional) - The phone number of the company.
        - :mobile: (str,optional) - The mobile number of the company.
        - :website: (str,optional) - The website of the company.
        - :vat: (str,optional) - The vat number of the company.
        - :city: (str,optional) - The city of the company.
        - :street: (str,optional) - The street address of the company.
        - :street2: (str,optional) - Additional street information.
        - :zip: (str,optional) - The postal code of the company.
        - :country_id: (int,optional) - The ID of the country for the company
        - :state_id: (int,optional) - The ID of the state or region for the company.

    Returns:
        dict: A dictionary containing the created company's ID.
    """
    
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "name" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "res.company"
                data = {}
                for key, value in params.items():
                    if value:
                        data[key] = value
                id = models.execute_kw(db, uid, apiPassword, model, "create", [data])
                return {"id": id}
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_get_company_by_id(cred,params):
    """
    Get company details from Odoo by company ID.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :company_id: (int,required) - The ID of the company.
        - :fields: (list,optional) - List of fields to include in the response.
            Available fields: name, email, phone, mobile, website, vat, city, country_id, state_id, street, street2, zip.

    Returns:
        dict: Company details.
    """
    
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "company_id" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            id = params.get("company_id")
            fields = params.get("fields", [])
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "res.company"
                data = models.execute_kw(
                    db, uid, apiPassword, model, "read", [int(id)], {"fields": fields}
                )
                if data:
                    return {"Company": data}
                else:
                    raise Exception("Not found")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_update_company(cred,params):
    """
    Update a company in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :company_id: (int,required) - The ID of the company.
        - :name: (str,optional) - The name of the company.
        - :email: (str,optional) - The email address of the company.
        - :phone: (str,optional) - The phone number of the company.
        - :mobile: (str,optional) - The mobile number of the company.
        - :website: (str,optional) - The website of the company.
        - :vat: (str,optional) - The vat number of the company.
        - :city: (str,optional) - The city of the company.
        - :street: (str,optional) - The street address of the company.
        - :street2: (str,optional) - Additional street information.
        - :zip: (str,optional) - The postal code of the company.
        - :country_id: (int,optional) - The ID of the country for the company
        - :state_id: (int,optional) - The ID of the state or region for the company.

    Returns:
        dict: A confirmation message indicating successful of the update.
    """
    
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "company_id" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            id = params["company_id"]
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "res.company"
                data = {}
                for key, value in params.items():
                    skip_keys = ["company_id"]
                    if key in skip_keys:
                        continue
                    if value:
                        data[key] = value
                if data:
                    if models.execute_kw(
                        db, uid, apiPassword, model, "search", [[("id", "=", int(id))]]
                    ):
                        models.execute_kw(
                            db, uid, apiPassword, model, "write", [[int(id)], data]
                        )
                        return {"message": "Updated successfully"}
                    else:
                        raise Exception("Not found")
                else:
                    raise Exception("Please specify at least one field to update")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_get_many_product(cred,params):
    """
    Get multiple products from Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :limit: (int,optional) - The maximum number of products to retrieve.
        - :fields: (list,optional) - List of fields to include in the response.
            Available fields: name, standard_price, list_price, description .
          
    Returns:
        dict: A dictionary containing the retrieved products.
    """
    
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds :
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]        
            limit = params.get("limit")
            fields = params.get("fields", [])
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "product.template"
                ids = models.execute_kw(db, uid, apiPassword, model, "search", [[]])
                data = models.execute_kw(
                    db, uid, apiPassword, model, "read", [ids], {"fields": fields}
                )
                return {"Products": data[:limit]}
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_create_product(cred,params):
    """
    Create a new product in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :name: (str,required) - The name of the product.
        - :list_price: (float,optional) - The sale price of the product.
        - :standard_price: (float,optional) - The cost price of the product.
        - :description: (str,optional) - Internal notes for the product.


    Returns:
        dict: A dictionary containing the ID of the created product.
    """
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "name" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]  
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "product.template"
                data = {}
                for key, value in params.items():
                    if value:
                        data[key] = value
                id = models.execute_kw(db, uid, apiPassword, model, "create", [data])
                return {"id": id}
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_get_product_by_id(cred,params):
    """
    Get product details from Odoo by product ID.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :product_id: (int,required) - The ID of the product.
        - :fields: (list,optional) - List of fields to include in the response.
            Available fields: name, standard_price, list_price, description .

    Returns:
        dict: Product details.
    """
    
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "product_id" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]  
            id = params.get("product_id")
            fields = params.get("fields", [])
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "product.template"
                data = models.execute_kw(
                    db, uid, apiPassword, model, "read", [int(id)], {"fields": fields}
                )
                if data:
                    return {"Product": data}
                else:
                    raise Exception("Not found")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_delete_product(cred,params):
    """
    Delete a product in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :product_id: (int,required) - The ID of the product.

    Returns:
        dict: A confirmation message indicating successful deletion.
    """
    
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "product_id" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]  
            id = params.get("product_id")
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "product.template"
                if models.execute_kw(
                    db, uid, apiPassword, model, "search", [[("id", "=", int(id))]]
                ):
                    models.execute_kw(db, uid, apiPassword, model, "unlink", [[id]])
                    return {"message": "Deleted successfully"}
                else:
                    raise Exception("ID not found or could not be deleted.")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_update_product(cred,params):
    """
    Update a product in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :product_id: (int,required) - The ID of the product.
        - :name: (str,optional) - The name of the product.
        - :list_price: (float,optional) - The sale price of the product.
        - :standard_price: (float,optional) - The cost price of the product.
        - :description: (str,optional) - Internal notes for the product.

    Returns:
        dict: A confirmation message indicating successful of the update.
    """
    
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "product_id" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]  
            id = params["product_id"]
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "product.template"
                data = {}
                for key, value in params.items():
                    skip_keys = ["product_id"]
                    if key in skip_keys:
                        continue
                    if value:
                        data[key] = value
                if data:
                    if models.execute_kw(
                        db, uid, apiPassword, model, "search", [[("id", "=", int(id))]]
                    ):
                        models.execute_kw(
                            db, uid, apiPassword, model, "write", [[int(id)], data]
                        )
                        return {"message": "Updated successfully"}
                    else:
                        raise Exception("Not found")
                else:
                    raise Exception("Please specify at least one field to update")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_get_many_product_category(cred,params):
    """
    Get multiple product category from Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :limit: (int,optional) - The maximum number of product category to retrieve.
        - :fields: (list,optional) - List of fields to include in the response.
            Available fields: name .
          
    Returns:
        dict: A dictionary containing the retrieved product category.
    """
    
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds :
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]  
            limit = params.get("limit")
            fields = params.get("fields", [])
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "product.category"
                ids = models.execute_kw(db, uid, apiPassword, model, "search", [[]])
                data = models.execute_kw(
                    db, uid, apiPassword, model, "read", [ids], {"fields": fields}
                )
                return {"Categories": data[:limit]}
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_create_product_category(cred,params):
    """
    Create a new product category in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :name: (str,required) - The name of the product category.

    Returns:
        dict: A dictionary containing the ID of the created product category.
    """
    
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "name" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]  
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "product.category"
                data = {}
                for key, value in params.items():
                    if value:
                        data[key] = value
                id = models.execute_kw(db, uid, apiPassword, model, "create", [data])
                return {"id": id}
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_get_product_category_by_id(cred,params):
    """
    Get category details from Odoo by category ID.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :category_id: (int,required) - The ID of the category.
        - :fields: (list,optional) - List of fields to include in the response.
            Available fields: name .

    Returns:
        dict: Category details.
    """
    
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "category_id" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]  
            id = params.get("category_id")
            fields = params.get("fields", [])
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "product.category"
                data = models.execute_kw(
                    db, uid, apiPassword, model, "read", [int(id)], {"fields": fields}
                )
                if data:
                    return {"Category": data}
                else:
                    raise Exception("Not found")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_update_product_category(cred,params):
    """
    Update a product category in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :category_id: (int,required) - The ID of the category.
        - :name: (str,optional) - The name of the product category.

    Returns:
        dict: A confirmation message indicating successful of the update.
    """
    
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "category_id" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            id = params["category_id"]
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "product.category"
                data = {}
                for key, value in params.items():
                    skip_keys = ["category_id"]
                    if key in skip_keys:
                        continue
                    if value:
                        data[key] = value
                if data:
                    if models.execute_kw(
                        db, uid, apiPassword, model, "search", [[("id", "=", int(id))]]
                    ):
                        models.execute_kw(
                            db, uid, apiPassword, model, "write", [[int(id)], data]
                        )
                        return {"message": "Updated successfully"}
                    else:
                        raise Exception("Not found")
                else:
                    raise Exception("Please specify at least one field to update")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_delete_product_category(cred,params):
    """
    Delete a product category in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :category_id: (int,required) - The ID of the category.

    Returns:
        dict: A confirmation message indicating successful deletion.
    """
    
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "category_id" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            id = params.get("category_id")
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                model = "product.category"
                if models.execute_kw(
                    db, uid, apiPassword, model, "search", [[("id", "=", int(id))]]
                ):
                    models.execute_kw(db, uid, apiPassword, model, "unlink", [[id]])
                    return {"message": "Deleted successfully"}
                else:
                    raise Exception("ID not found or could not be deleted.")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_get_many_CustomResource(cred,params):
    """
    Get multiple custom resources from Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :model: (str,required): The Odoo model for the custom resource.
        - :limit: (int,optional) - The maximum number of records to retrieve.
        - :fields: (list,optional) - List of fields to include in the response.
          
    Returns:
        dict: A dictionary containing the retrieved custom resources.
    """
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            model = params.get("model")
            limit = params.get("limit")
            fields = params.get("fields", [])
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                ids = models.execute_kw(db, uid, apiPassword, model, "search", [[]])
                data = models.execute_kw(
                    db, uid, apiPassword, model, "read", [ids], {"fields": fields}
                )
                return data[:limit]
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_create_CustomResource(cred,params):
    """
    Create a new custom resource in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :model: (str,required) - The Odoo model for the custom resource.
        - Custom Fields (str,optional) - Custom fields and their values for the new resource.
            For example,
            
            {"model": "" , "custom_field1": "value1", "custom_field2": "value2"}

    Returns:
        dict: A dictionary containing the ID of the created custom resource.
      
    """
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "model" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            model = params.get("model")
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                data = {}
                for key, value in params.items():
                    skip_keys = ["model"]
                    if key in skip_keys:
                        continue
                    if value:
                        data[key] = value
                id = models.execute_kw(db, uid, apiPassword, model, "create", [data])
                return {"id": id}
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_get_CustomResource_by_id(cred,params):
    """
    Get Custom Resource details from Odoo by Custom Resource ID.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.
    
        - :model: (str,required) - The Odoo model for the custom resource.
        - :customResource_id: (int,required) - The ID of the Custom Resource.
        - :fields: (list,optional) - List of fields to include in the response.

    Returns:
        dict: Custom Resource details.
    """
    
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "customResource_id" in params and "model" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            id = params.get("customResource_id")
            fields = params.get("fields", [])
            model = params.get("model")
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                data = models.execute_kw(
                    db, uid, apiPassword, model, "read", [int(id)], {"fields": fields}
                )
                if data:
                    return data
                else:
                    raise Exception("Not found")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_update_CustomResource(cred,params):
    """
    Update a Custom Resource in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :model: (str,required) - The Odoo model for the custom resource.
        - :customResource_id: (int,required) - The ID of the Custom Resource.
        - Custom Fields (str,optional): Custom fields and their values for the new resource.
            For example,
            
            {"model": "", "custom_field1": "value1", "custom_field2": "value2"}
        
    Returns:
        dict: A confirmation message indicating successful of the update.
    """
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "customResource_id" in params and "model" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            id = params["customResource_id"]
            model = params.get("model")
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                data = {}
                for key, value in params.items():
                    skip_keys = ["customResource_id", "model"]
                    if key in skip_keys:
                        continue
                    if value:
                        data[key] = value
                if data:
                    if models.execute_kw(
                        db, uid, apiPassword, model, "search", [[("id", "=", int(id))]]
                    ):
                        models.execute_kw(
                            db, uid, apiPassword, model, "write", [[int(id)], data]
                        )
                        return {"message": "Updated successfully"}
                    else:
                        raise Exception("Not found")
                else:
                    raise Exception("Please specify at least one field to update")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)


def odoo_delete_CustomResource(cred,params):
    """
    Delete a Custom Resource in Odoo.

    :param str url: The URL of the Odoo instance.
    :param str db: The name of the Odoo database.
    :param str username: The username for authentication.
    :param str apiPassword: The API password for authentication.
    :param dict params: Dictionary containing parameters.

        - :model: (str,required) - The Odoo model for the custom resource.
        - :customResource_id: (int,required) - The ID of the Custom Resource.

    Returns:
        dict: A confirmation message indicating successful deletion.
    """
    try:
        creds=json.loads(cred)
        if "url" in creds and "db" in creds and "username" in creds and "apiPassword" in creds and "customResource_id" in params and "model" in params:
            url = creds["url"]
            db = creds["db"]
            username = creds["username"]
            apiPassword = creds["apiPassword"]
            id = params.get("customResource_id")
            model = params.get("model")
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, apiPassword, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
                if models.execute_kw(
                    db, uid, apiPassword, model, "search", [[("id", "=", int(id))]]
                ):
                    models.execute_kw(db, uid, apiPassword, model, "unlink", [[id]])
                    return {"message": "Deleted successfully"}
                else:
                    raise Exception("ID not found or could not be deleted.")
            else:
                raise Exception("Authentication failed. Please check your credentials.")
        else:
            raise Exception("Missing Input Data")
    except Exception as error:
        raise Exception(error)
