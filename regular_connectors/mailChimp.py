import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import json

def create_client_instance(API_KEY, SERVER_PREFIX):
    """
    Returns a client instance of MailChimp API using the provided Api key and server prefix

    :param str API_KEY: Used for authentication purposes.
    :param str SERVER_PREFIX: Used for authentication purposes.

    :return: client instance of MailChimp API
    :rtype: MailchimpMarketing Client object
    """
    try:
        if API_KEY and SERVER_PREFIX:
            mailchimp = MailchimpMarketing.Client()
            mailchimp.set_config({"api_key": API_KEY, "server": SERVER_PREFIX})
            return mailchimp
        else:
            raise Exception("Please provide API Key and Server Prefix")
    except Exception as e:
        raise Exception(f"Error creating client instance: {e}")


def reply_upon_success(response):
    """
    changes the response into a dictionary if it consists of a status code only

    :param object response: response object received from the mailchimp api

    :return: response object from MailChimp API in case of failure, otherwise a dictionary indicating the success of the operation
    :rtype: dict
    """

    valid_status_code = [200, 201, 202, 204, 206, 207, 208]
    if response.status_code in valid_status_code:
        return {
            "result": "Operation Performed successfuly",
            "Status Code": response.status_code,
        }
    else:
        return response


def mailchimp_check_connection(cred):
    """
    A health check for the API that won't return any account-specific information.

    :param str API_KEY: Used for authentication purposes.
    :param str SERVER_PREFIX: Used for authentication purposes.

    :return: result of the health check
    :rtype: dict
    """
    try:
        creds = json.loads(cred)
        API_KEY = creds["apiKey"]
        SERVER_PREFIX = creds["serverPrefix"]
        mailchimp = create_client_instance(API_KEY, SERVER_PREFIX)
        try:
            response = mailchimp.ping.get()
        except ApiClientError as error:
            raise Exception(f"Mailchimp API error: {error.text}")
        else:
            return response
    except Exception as e:
        raise Exception(f"error checking connection: {e}")


#################################### Code goes Here #############################################

#################################### Members ####################################################

def mailchimp_create_member(cred,params):
    """
    Add a new member to the list.

    :API_KEY: String used for authentication purposes.
    :SERVER_PREFIX: String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :list_id: (str,required) - The unique ID for the list. 
    - :skip_merge_validation: (bool,optional) - If skip_merge_validation is true, member data will be accepted without merge field values, even if the merge field is usually required. This defaults to false.
    - :body: Required dictionary containing the body parameters.

        - :email_address: (str,required) - Email address for a subscriber.
        - :status: (str,required) - Subscriber's current status. (subscribed, unsubscribed, cleaned, pending, transactional) .
        - :email_type: (str,optional) - Type of email this member asked to get (html, text). 
        - :merge_fields: (dict,optional) - A dictionary of merge fields where the keys are the merge tags. See the `Merge Fields documentation <https://mailchimp.com/developer/marketing/docs/merge-fields/#structure>`_ for more about the structure. 
        - :interests: (dict,optional) - The key of this dictionary's properties is the ID of the interest in question. and the value is a boolean true.
        - :language: (str,optional) - If set/detected, the `subscriber's language <https://mailchimp.com/help/view-and-edit-contact-languages/>`_. 
        - :vip: (bool,optional) - `VIP status <https://mailchimp.com/help/designate-and-send-to-vip-contacts/>`_ for subscriber.
        - :location: (dict,optional) - Subscriber location information. 

            - :latitude: (float,optional) - The location latitude. 
            - :longitude: (float,optional) - The location longitude. 

        - :marketing_permissions: (list of dict,optional) - List containing the marketing permissions for the subscriber.

            - :marketing_permission_id: (str,optional)
            - :enabled: (bool,optional) - If the subscriber has opted-in to the marketing permission. 

        - :ip_signup: (str,optional) - IP address the subscriber signed up from. 
        - :timestamp_signup: (str,optional) - The date and time the subscriber signed up for the list in ISO 8601 format. 
        - :ip_opt: (str,optional) - The IP address the subscriber used to confirm their opt-in status. 
        - :timestamp_opt: (str,optional) - The date and time the subscriber confirmed their opt-in status in ISO 8601 format. 
        - :tags: (list of str,optional) - The tags that are associated with a member. 

    :return: response object from MailChimp API containing the information of the newly added member
    :rtype: dict
    """
    try:
        creds = json.loads(cred)
        API_KEY = creds["apiKey"]
        SERVER_PREFIX = creds["serverPrefix"]
        body = params.get("body", {})
        if "list_id" in params and "email_address" in body and "status" in body and "apiKey" in creds and "serverPrefix" in creds:
            data = {key: value for (key, value) in params.items() if value}
            mailchimp = create_client_instance(API_KEY, SERVER_PREFIX)
            try:
                response = mailchimp.lists.add_list_member(**data)
            except ApiClientError as error:
                raise Exception(f"Mailchimp API error: {error.text}")
            else:
                return response
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(f"Error creating member: {e}")

def mailchimp_get_member(cred,params):
    """
    Get information about a specific list member, including a currently subscribed, unsubscribed, or bounced member.

    :API_KEY: String used for authentication purposes.
    :SERVER_PREFIX: String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :list_id: (str,required) - The unique ID for the list. 
    - :subscriber_hash: (str,required) - The MD5 hash of the lowercase version of the list member's email address. This endpoint also accepts a list member's email address or contact_id. 
    - :fields: (list of str,optional) - A comma-separated list of fields to return. Reference parameters of sub-objects with dot notation. 
    - :exclude_fields: (list of str,optional) - A comma-separated list of fields to exclude. Reference parameters of sub-objects with dot notation. 

    :return: response object from MailChimp API containing information about selected member
    :rtype: dict
    """
    try:
        creds = json.loads(cred)
        API_KEY = creds["apiKey"]
        SERVER_PREFIX = creds["serverPrefix"]
        if "list_id" in params and "subscriber_hash" in params and "apiKey" in creds and "serverPrefix" in creds:
            data = {key: value for (key, value) in params.items() if value}
            mailchimp = create_client_instance(API_KEY, SERVER_PREFIX)
            try:
                response = mailchimp.lists.get_list_member(**data)
            except ApiClientError as error:
                raise Exception(f"Mailchimp API error: {error.text}")
            else:
                return response
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(f"Error getting member: {e}")

def mailchimp_get_list_members(cred,params):
    """
    Get information about members in a specific Mailchimp list.

    :API_KEY: String used for authentication purposes.
    :SERVER_PREFIX: String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :list_id: (str,required) - The unique ID for the list. 
    - :fields: (list of str,optional) - A comma-separated list of fields to return. Reference parameters of sub-objects with dot notation. 
    - :exclude_fields: (list of str,optional) - A comma-separated list of fields to exclude. Reference parameters of sub-objects with dot notation. 
    - :count: (int,optional) - The number of records to return. Default value is 10. Maximum value is 1000.
    - :offset: (int,optional) - Used for `pagination <https://mailchimp.com/developer/marketing/docs/methods-parameters/#pagination>`_, this is the number of records from a collection to skip. Default value is 0.
    - :email_type: (str,optional) - The email type.
    - :status: (str,optional) - The subscriber's status.(subscribed, unsubscribed, cleaned, pending, transactional, archived)
    - :since_timestamp_opt: (str,optional) - Restrict results to subscribers who opted-in after the set timeframe. Uses ISO 8601 time format: 2015-10-21T15:41:36+00:00. 
    - :before_timestamp_opt: (str,optional) - Restrict results to subscribers who opted-in before the set timeframe. Uses ISO 8601 time format: 2015-10-21T15:41:36+00:00. 
    - :since_last_changed: (str,optional) - Restrict results to subscribers whose information changed after the set timeframe. Uses ISO 8601 time format: 2015-10-21T15:41:36+00:00. 
    - :before_last_changed: (str,optional) - Restrict results to subscribers whose information changed before the set timeframe. Uses ISO 8601 time format: 2015-10-21T15:41:36+00:00. 
    - :unique_email_id: (str,optional) - A unique identifier for the email address across all Mailchimp lists. 
    - :vip_only: (bool,optional) - A filter to return only the list's VIP members. Passing true will restrict results to VIP list members, passing false will return all list members. 
    - :interest_category_id: (str,optional) - The unique id for the interest category. 
    - :interest_ids: (list of str,optional) - Used to filter list members by interests. Must be accompanied by interest_category_id and interest_match. The value must be a comma separated list of interest ids present for any supplied interest categories.
    - :interest_match: (str,optional) - Used to filter list members by interests. Must be accompanied by interest_category_id and interest_ids. "any" will match a member with any of the interest supplied, "all" will only match members with every interest supplied, and "none" will match members without any of the interest supplied. Possible values: (any, all, none).
    - :sort_field: (str,optional) - Returns files sorted by the specified field. Possible values: (timestamp_opt, timestamp_signup, last_changed).
    - :sort_dir: (str,optional) - Determines the order direction for sorted results. Possible values: (ASC, DESC)
    - :since_last_campaign: (bool,optional) - Filter subscribers by those subscribed/unsubscribed/pending/cleaned since last email campaign send. Member status is required to use this filter.
    - :unsubscribed_since: (str,optional) - Filter subscribers by those unsubscribed since a specific date. Using any status other than unsubscribed with this filter will result in an error.

    :return: response object from MailChimp API in the form of a list of dictionaries with each dictionary representing a member of the list
    :rtype: List[dict]
    """
    try:
        creds = json.loads(cred)
        API_KEY = creds["apiKey"]
        SERVER_PREFIX = creds["serverPrefix"]
        if "list_id" in params and "apiKey" in creds and "serverPrefix" in creds:
            data = {key: value for (key, value) in params.items() if value}
            mailchimp = create_client_instance(API_KEY, SERVER_PREFIX)
            try:
                response = mailchimp.lists.get_list_members_info(**data)
            except ApiClientError as error:
                raise Exception(f"Mailchimp API error: {error.text}")
            else:
                return response
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(f"Error getting list members: {e}")

def mailchimp_update_member(cred,params):
    """
    Update information for a specific list member.

    :API_KEY: String used for authentication purposes.
    :SERVER_PREFIX: String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :list_id: (str,required) - The unique ID for the list.
    - :subscriber_hash: (str,required) - The MD5 hash of the lowercase version of the list member's email address. This endpoint also accepts a list member's email address or contact_id. 
    - :skip_merge_validation: (bool,optional) - If skip_merge_validation is true, member data will be accepted without merge field values, even if the merge field is usually required. This defaults to false.
    - :body: Required dictionary containing the body parameters.

        - :email_address: (str,optional) - Email address for a subscriber.
        - :status: (str,optional) - Subscriber's current status. (subscribed, unsubscribed, cleaned, pending) .
        - :email_type: (str,optional) - Type of email this member asked to get (html, text). 
        - :merge_fields: (dict,optional) - A dictionary of merge fields where the keys are the merge tags. See the `Merge Fields documentation <https://mailchimp.com/developer/marketing/docs/merge-fields/#structure>`_ for more about the structure. 
        - :interests: (dict,optional) - The key of this dictionary's properties is the ID of the interest in question. and the value is a boolean value.
        - :language: (str,optional) - If set/detected, the `subscriber's language <https://mailchimp.com/help/view-and-edit-contact-languages/>`_. 
        - :vip: (bool,optional) - `VIP status <https://mailchimp.com/help/designate-and-send-to-vip-contacts/>`_ for subscriber.
        - :location: (dict,optional) - Subscriber location information. 

            - :latitude: (float,optional) - The location latitude. 
            - :longitude: (float,optional) - The location longitude. 

        - :marketing_permissions: (list of dict,optional) - List containing the marketing permissions for the subscriber.

            - :marketing_permission_id: (str,optional)
            - :enabled: (bool,optional) - If the subscriber has opted-in to the marketing permission. 

        - :ip_signup: (str,optional) - IP address the subscriber signed up from. 
        - :timestamp_signup: (str,optional) - The date and time the subscriber signed up for the list in ISO 8601 format. 
        - :ip_opt: (str,optional) - The IP address the subscriber used to confirm their opt-in status. 
        - :timestamp_opt: (str,optional) - The date and time the subscriber confirmed their opt-in status in ISO 8601 format. 
        - :tags: (list of str,optional) - The tags that are associated with a member. 

    :return: response object from MailChimp API containing the information of the newly updated member
    :rtype: dict
    """
    try:
        creds = json.loads(cred)
        API_KEY = creds["apiKey"]
        SERVER_PREFIX = creds["serverPrefix"]
        if "list_id" in params and "subscriber_hash" in params and "body" in params and "apiKey" in creds and "serverPrefix" in creds:
            data = {key: value for (key, value) in params.items() if value}
            mailchimp = create_client_instance(API_KEY, SERVER_PREFIX)
            try:
                response = mailchimp.lists.update_list_member(**data)
            except ApiClientError as error:
                raise Exception(f"Mailchimp API error: {error.text}")
            else:
                return response
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(f"Error updating member: {e}")

def mailchimp_delete_member(cred,params):
    """
    Delete all personally identifiable information related to a list member, and remove them from a list. This will make it impossible to re-import the list member.

    :API_KEY: String used for authentication purposes.
    :SERVER_PREFIX: String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :list_id: (str,required) - The unique ID for the list. 
    - :subscriber_hash: (str,required) - The MD5 hash of the lowercase version of the list member's email address. This endpoint also accepts a list member's email address or contact_id. 

    :return: response object from MailChimp API in case of failure, otherwise a dictionary indicating the success of the operation
    :rtype: dict
    """
    try:
        creds = json.loads(cred)
        API_KEY = creds["apiKey"]
        SERVER_PREFIX = creds["serverPrefix"]
        list_id = params.get("list_id", None)
        subscriber_hash = params.get("subscriber_hash", None)
        # note for list id and subscriber
        if "apiKey" in creds and "serverPrefix" in creds and list_id and subscriber_hash:
            data = {"list_id": list_id, "subscriber_hash": subscriber_hash}
            mailchimp = create_client_instance(API_KEY, SERVER_PREFIX)
            try:
                response = mailchimp.lists.delete_list_member_permanent(**data)
            except ApiClientError as error:
                raise Exception(f"Mailchimp API error: {error.text}")
            else:
                return reply_upon_success(response)
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(f"Error deleting member: {e}")

def mailchimp_archive_member(cred,params):
    """
    Archive a list member. To permanently delete, use the delete-permanent action.

    :API_KEY: String used for authentication purposes.
    :SERVER_PREFIX: String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :list_id: (str,required) - The unique ID for the list. 
    - :subscriber_hash: (str,required) - The MD5 hash of the lowercase version of the list member's email address. This endpoint also accepts a list member's email address or contact_id. 

    :return: response object from MailChimp API in case of failure, otherwise a dictionary indicating the success of the operation
    :rtype: dict
    """
    try:
        creds = json.loads(cred)
        API_KEY = creds["apiKey"]
        SERVER_PREFIX = creds["serverPrefix"]
        list_id = params.get("list_id", None)
        subscriber_hash = params.get("subscriber_hash", None)
        # note for list id and subscriber
        if "apiKey" in creds and "serverPrefix" in creds and list_id and subscriber_hash:
            data = {"list_id": list_id, "subscriber_hash": subscriber_hash}
            mailchimp = create_client_instance(API_KEY, SERVER_PREFIX)
            try:
                response = mailchimp.lists.delete_list_member(**data)
            except ApiClientError as error:
                raise Exception(f"Mailchimp API error: {error.text}")
            else:
                return reply_upon_success(response)
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(f"Error Archiving member: {e}")

def mailchimp_add_note_to_member(cred,params):
    """
    Add a new note for a specific subscriber.

    :API_KEY: String used for authentication purposes.
    :SERVER_PREFIX: String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :list_id: (str,required) - The unique ID for the list.
    - :subscriber_hash: (str,required) - The MD5 hash of the lowercase version of the list member's email address. This endpoint also accepts a list member's email address or contact_id. 
    - :body: Required dictionary containing the body parameters.

        - :note: (str,optional) - The content of the note. Note length is limited to 1,000 characters. 

    :return: response object from MailChimp API contining added note information
    :rtype: dict
    """
    try:
        creds = json.loads(cred)
        API_KEY = creds["apiKey"]
        SERVER_PREFIX = creds["serverPrefix"]
        if "list_id" in params and "subscriber_hash" in params and "body" in params and "apiKey" in creds and "serverPrefix" in creds:
            data = {key: value for (key, value) in params.items() if value}
            mailchimp = create_client_instance(API_KEY, SERVER_PREFIX)
            try:
                response = mailchimp.lists.create_list_member_note(**data)
            except ApiClientError as error:
                raise Exception(f"Mailchimp API error: {error.text}")
            else:
                return response
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(f"Error adding note to member: {e}")


############################################ Events #################################################

def mailchimp_add_member_event(cred,params):
    """
    Add a new note for a specific subscriber.

    :API_KEY: String used for authentication purposes.
    :SERVER_PREFIX: String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :list_id: (str,required) - The unique ID for the list.
    - :subscriber_hash: (str,required) - The MD5 hash of the lowercase version of the list member's email address. This endpoint also accepts a list member's email address or contact_id. 
    - :body: Required dictionary containing the body parameters.

        - :name: (str,required) - The name for this type of event ('purchased', 'visited', etc). Must be 2-30 characters in length
        - :properties: (list of str,optional) - An optional list of properties 
        - :is_syncing: (bool,optional) - Events created with the is_syncing value set to true will not trigger automations. 
        - :occurred_at: (str,optional) - The date and time the event occurred in ISO 8601 format. 

    :return: response object from MailChimp API in case of failure, otherwise a dictionary indicating the success of the operation
    :rtype: dict
    """
    try:
        creds = json.loads(cred)
        API_KEY = creds["apiKey"]
        SERVER_PREFIX = creds["serverPrefix"]
        body = params.get("body", {})
        if "list_id" in params and "subscriber_hash" in params and "name" in body and "apiKey" in creds and "serverPrefix" in creds:
            data = {key: value for (key, value) in params.items() if value}
            mailchimp = create_client_instance(API_KEY, SERVER_PREFIX)
            try:
                response = mailchimp.lists.create_list_member_event(**data)
            except ApiClientError as error:
                raise Exception(f"Mailchimp API error: {error.text}")
            else:
                return reply_upon_success(response)
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(f"Error adding member's event: {e}")

def mailchimp_list_member_events(cred,params):
    """
    Get events for a contact.

    :API_KEY: String used for authentication purposes.
    :SERVER_PREFIX: String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :list_id: (str,required) - The unique ID for the list.
    - :subscriber_hash: (str,required) - The MD5 hash of the lowercase version of the list member's email address. This endpoint also accepts a list member's email address or contact_id.
    - :count: (int,optional) - The number of records to return. Default value is 10. Maximum value is 1000
    - :offset: (int,optional) - Used for `pagination <https://mailchimp.com/developer/marketing/docs/methods-parameters/#pagination>`_, this is the number of records from a collection to skip. Default value is 0.
    - :fields: (list of str,optional) - A comma-separated list of fields to return. Reference parameters of sub-objects with dot notation. 
    - :exclude_fields: (list of str,optional) - A comma-separated list of fields to exclude. Reference parameters of sub-objects with dot notation. 

    :return: response object from MailChimp API containing a list of the events with each event in the form of a dictionary as well as other relevant information
    :rtype: dict
    """
    try:
        creds = json.loads(cred)
        API_KEY = creds["apiKey"]
        SERVER_PREFIX = creds["serverPrefix"]
        if "list_id" in params and "subscriber_hash" in params and "apiKey" in creds and "serverPrefix" in creds:
            data = {key: value for (key, value) in params.items() if value}
            mailchimp = create_client_instance(API_KEY, SERVER_PREFIX)
            try:
                response = mailchimp.lists.get_list_member_events(**data)
            except ApiClientError as error:
                raise Exception(f"Mailchimp API error: {error.text}")
            else:
                return response
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(f"Error listing member's events: {e}")


########################################## Tags ##################################################


def mailchimp_update_member_tags(cred,params):
    """
    Add or remove tags from a list member. If a tag that does not exist is passed in and set as 'active', a new tag will be created.

    :API_KEY: String used for authentication purposes.
    :SERVER_PREFIX: String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :list_id: (str,required) - The unique ID for the list.
    - :subscriber_hash: (str,required) - The MD5 hash of the lowercase version of the list member's email address. This endpoint also accepts a list member's email address or contact_id. 
    - :body: Required dictionary containing the body parameters.

        - :tags: (list of dict,required) - A list of tags assigned to the list member, with each tag being represented with a dictionary containing the following parameters:

            - :name: (str,optional) - The name of the tag.
            - :status: (str,optional) - The status for the tag on the member, pass in active to add a tag or inactive to remove it. Possible values: (inactive, active).

        - :is_syncing: (bool,optional) - When is_syncing is true, automations based on the tags in the request will not fire 

    :return: response object from MailChimp API in case of failure, otherwise a dictionary indicating the success of the operation
    :rtype: dict
    """
    try:
        creds = json.loads(cred)
        API_KEY = creds["apiKey"]
        SERVER_PREFIX = creds["serverPrefix"]
        if (
            "list_id" in params
            and "subscriber_hash" in params
            and "tags" in params.get("body", {})
        ) and "apiKey" in creds and "serverPrefix" in creds:
            data = {key: value for (key, value) in params.items() if value}
            mailchimp = create_client_instance(API_KEY, SERVER_PREFIX)
            try:
                response = mailchimp.lists.update_list_member_tags(**data)
            except ApiClientError as error:
                raise Exception(f"Mailchimp API error: {error.text}")
            else:
                return reply_upon_success(response)
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(f"Error updating member tags: {e}")

def mailchimp_list_member_tags(cred,params):
    """
    Get the tags on a list member.

    :API_KEY: String used for authentication purposes.
    :SERVER_PREFIX: String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :list_id: (str,required) - The unique ID for the list.
    - :subscriber_hash: (str,required) - The MD5 hash of the lowercase version of the list member's email address. This endpoint also accepts a list member's email address or contact_id.
    - :count: (int,optional) - The number of records to return. Default value is 10. Maximum value is 1000
    - :offset: (int,optional) - Used for `pagination <https://mailchimp.com/developer/marketing/docs/methods-parameters/#pagination>`_, this is the number of records from a collection to skip. Default value is 0.
    - :fields: (list of str,optional) - A comma-separated list of fields to return. Reference parameters of sub-objects with dot notation. 
    - :exclude_fields: (list of str,optional) - A comma-separated list of fields to exclude. Reference parameters of sub-objects with dot notation. 

    :return: response object from MailChimp API containing a list of the tags with each tag in the form of a dictionary as well as other relevant information
    :rtype: dict
    """
    try:
        creds = json.loads(cred)
        API_KEY = creds["apiKey"]
        SERVER_PREFIX = creds["serverPrefix"]
        if "list_id" in params and "subscriber_hash" in params and "apiKey" in creds and "serverPrefix" in creds:
            data = {key: value for (key, value) in params.items() if value}
            mailchimp = create_client_instance(API_KEY, SERVER_PREFIX)
            try:
                response = mailchimp.lists.get_list_member_tags(**data)
            except ApiClientError as error:
                raise Exception(f"Mailchimp API error: {error.text}")
            else:
                return response
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(f"Error getting member tags: {e}")

def mailchimp_find_tags(cred,params):
    """
    Search for tags on a list by name. If no name is provided, will return all tags on the list.

    :API_KEY: String used for authentication purposes.
    :SERVER_PREFIX: String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :list_id: (str,required) - The unique ID for the list. 
    - :name: (str,optional) - The search query used to filter tags. The search query will be compared to each tag as a prefix, so all tags that have a name starting with this field will be returned.

    :return: response object from MailChimp API containing a list of the tags with each tag in the form of a dictionary as well as other relevant information
    :rtype: dict
    """
    try:
        creds = json.loads(cred)
        API_KEY = creds["apiKey"]
        SERVER_PREFIX = creds["serverPrefix"]
        if "list_id" in params and "apiKey" in creds and "serverPrefix" in creds:
            data = {key: value for (key, value) in params.items() if value}
            mailchimp = create_client_instance(API_KEY, SERVER_PREFIX)
            try:
                response = mailchimp.lists.tag_search(**data)
            except ApiClientError as error:
                raise Exception(f"Mailchimp API error: {error.text}")
            else:
                return response
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(f"Error finding tags: {e}")


######################################## Lists #####################################################

def mailchimp_get_many_lists(cred,params):
    """
    Get information about all lists in the account.

    :API_KEY: String used for authentication purposes.
    :SERVER_PREFIX: String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :fields: (list of str,optional) - A comma-separated list of fields to return. Reference parameters of sub-objects with dot notation. 
    - :exclude_fields: (list of str,optional) - A comma-separated list of fields to exclude. Reference parameters of sub-objects with dot notation. 
    - :count: (int,optional) - The number of records to return. Default value is 10. Maximum value is 1000.
    - :offset: (int,optional) - Used for `pagination <https://mailchimp.com/developer/marketing/docs/methods-parameters/#pagination>`_, this is the number of records from a collection to skip. Default value is 0.
    - :before_date_created: (str,optional) - Restrict response to lists created before the set date. Uses ISO 8601 time format: 2015-10-21T15:41:36+00:00.
    - :since_date_created: (str,optional) - Restrict results to lists created after the set date. Uses ISO 8601 time format: 2015-10-21T15:41:36+00:00.
    - :before_campaign_last_sent: (str,optional) - 

        Restrict results to lists created before the last campaign send date. Uses ISO 8601 time format: 2015-10-21T15:41:36+00:00.
    - :since_campaign_last_sent: (str,optional) - 

        Restrict results to lists created after the last campaign send date. 

        Uses ISO 8601 time format: 2015-10-21T15:41:36+00:00.
    - :email: (str,optional) - Restrict results to lists that include a specific subscriber's email address.
    - :sort_field: (str,optional) - Returns files sorted by the specified field. Possible value: (date_created)
    - :sort_dir: (str,optional) - Determines the order direction for sorted results. Possible values: (ASC, DESC)
    - :has_ecommerce_store: (bool,optional) - Restrict results to lists that contain an active, connected, undeleted ecommerce store.
    - :include_total_contacts: (str,optional) - Return the total_contacts field in the stats response, which contains an approximate count of all contacts in any state.

    :return: response object from MailChimp API in the form of a dictionary containing a list of dictionaries with each dictionary representing a list and other relevant information
    :rtype: dict
    """
    try:
        creds = json.loads(cred)
        API_KEY = creds["apiKey"]
        SERVER_PREFIX = creds["serverPrefix"]
        try:
            if "apiKey" in creds and "serverPrefix" in creds:
                data = {key: value for (key, value) in params.items() if value}
                mailchimp = create_client_instance(API_KEY, SERVER_PREFIX)
                response = mailchimp.lists.get_all_lists(**data)
            else:
                raise Exception("Missing input data")
        except ApiClientError as error:
            raise Exception(f"Mailchimp API error: {error.text}")
        else:
            return response
    except Exception as e:
        raise Exception(f"Error getting lists: {e}")


########################################### Campaigns ##############################################

def mailchimp_get_campaign(cred,params):
    """
    Get information about a specific campaign.

    :API_KEY: String used for authentication purposes.
    :SERVER_PREFIX: String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :campaign_id: (str,required) - The unique id for the campaign.
    - :fields: (list of str,optional) - A comma-separated list of fields to return. Reference parameters of sub-objects with dot notation. 
    - :exclude_fields: (list of str,optional) - A comma-separated list of fields to exclude. Reference parameters of sub-objects with dot notation. 

    :return: response object from MailChimp API containing information about selected campaign
    :rtype: dict
    """
    try:
        creds = json.loads(cred)
        API_KEY = creds["apiKey"]
        SERVER_PREFIX = creds["serverPrefix"]
        if "campaign_id" in params and "apiKey" in creds and "serverPrefix" in creds:
            data = {key: value for (key, value) in params.items() if value}
            mailchimp = create_client_instance(API_KEY, SERVER_PREFIX)
            try:
                response = mailchimp.campaigns.get(**data)
            except ApiClientError as error:
                raise Exception(f"Mailchimp API error: {error.text}")
            else:
                return response
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(f"Error getting campain: {e}")

def mailchimp_get_many_campaigns(cred,params):
    """
    Get all campaigns in an account.

    :API_KEY: String used for authentication purposes.
    :SERVER_PREFIX: String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :fields: (list of str,optional) - A comma-separated list of fields to return. Reference parameters of sub-objects with dot notation. 
    - :exclude_fields: (list of str,optional) - A comma-separated list of fields to exclude. Reference parameters of sub-objects with dot notation. 
    - :count: (int,optional) - The number of records to return. Default value is 10. Maximum value is 1000.
    - :offset: (int,optional) - Used for `pagination <https://mailchimp.com/developer/marketing/docs/methods-parameters/#pagination>`_, this is the number of records from a collection to skip. Default value is 0.
    - :type: (str,optional) - The campaign type. Possible values: (regular, plaintext, absplit, rss, variate)
    - :status: (str,optional) - The status of the campaign.(save, sent, sending, schedule, paused)
    - :before_send_time: (str,optional) - Restrict the response to campaigns sent before the set time. Uses ISO 8601 time format: 2015-10-21T15:41:36+00:00.
    - :since_send_time: (str,optional) - Restrict the response to campaigns sent after the set time. Uses ISO 8601 time format: 2015-10-21T15:41:36+00:00.
    - :before_create_time: (str,optional) - Restrict the response to campaigns created before the set time. Uses ISO 8601 time format: 2015-10-21T15:41:36+00:00.
    - :since_create_time: (str,optional) - Restrict the response to campaigns created after the set time. Uses ISO 8601 time format: 2015-10-21T15:41:36+00:00.
    - :list_id: (str,optional) - The unique id for the list.
    - :folder_id: (bool,optional) - The unique folder id.
    - :member_id: (str,optional) - Retrieve campaigns sent to a particular list member. Member ID is The MD5 hash of the lowercase version of the list member’s email address.
    - :sort_field: (str,optional) - Returns files sorted by the specified field. Possible values: (create_time, send_time)
    - :sort_dir: (str,optional) - Determines the order direction for sorted results. Possible values: (ASC, DESC)

    :return: response object from MailChimp API in the form of a dictionary containing a list of dictionaries with each dictionary representing a campaign and other relevant information
    :rtype: dict
    """
    try:
        creds = json.loads(cred)
        API_KEY = creds["apiKey"]
        SERVER_PREFIX = creds["serverPrefix"]
        try:
            if "apiKey" in creds and "serverPrefix" in creds:
                data = {key: value for (key, value) in params.items() if value}
                mailchimp = create_client_instance(API_KEY, SERVER_PREFIX)
                response = mailchimp.campaigns.list(**data)
            else:
                raise Exception("Missing input data")
        except ApiClientError as error:
            raise Exception(f"Mailchimp API error: {error.text}")
        else:
            return response
    except Exception as e:
        raise Exception(f"Error getting campains: {e}")

def mailchimp_send_campaign(cred,params):
    """
    Send a Mailchimp campaign. For RSS Campaigns, the campaign will send according to its schedule. All other campaigns will send immediately.

    :API_KEY: String used for authentication purposes.
    :SERVER_PREFIX: String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :campaign_id: (str,required) - The unique id for the campaign.

    :return: response object from MailChimp API in case of failure, otherwise a dictionary indicating the success of the operation
    :rtype: dict
    """
    try:
        creds = json.loads(cred)
        API_KEY = creds["apiKey"]
        SERVER_PREFIX = creds["serverPrefix"]
        campaign_id = params.get("campaign_id", None)
        if "apiKey" in creds and "serverPrefix" in creds and campaign_id:
            data = {"campaign_id": campaign_id}
            mailchimp = create_client_instance(API_KEY, SERVER_PREFIX)
            try:
                response = mailchimp.campaigns.send(**data)
            except ApiClientError as error:
                raise Exception(f"Mailchimp API error: {error.text}")
            else:
                return reply_upon_success(response)
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(f"Error sending campain: {e}")

def mailchimp_resend_campaign(cred,params):
    """
    Creates a Resend to Non-Openers version of this campaign. We will also check if this campaign meets the criteria for Resend to Non-Openers campaigns.

    :API_KEY: String used for authentication purposes.
    :SERVER_PREFIX: String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :campaign_id: (str,required) - The unique id for the campaign.

    :return: response object from MailChimp API containing A summary of an individual campaign's settings and content.
    :rtype: dict
    """
    try:
        creds = json.loads(cred)
        API_KEY = creds["apiKey"]
        SERVER_PREFIX = creds["serverPrefix"]
        campaign_id = params.get("campaign_id", None)
        if "apiKey" in creds and "serverPrefix" in creds and campaign_id:
            data = {"campaign_id": campaign_id}
            mailchimp = create_client_instance(API_KEY, SERVER_PREFIX)
            try:
                response = mailchimp.campaigns.create_resend(**data)
            except ApiClientError as error:
                raise Exception(f"Mailchimp API error: {error.text}")
            else:
                return response
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(f"Error resending campain: {e}")

def mailchimp_replicate_campaign(cred,params):
    """
    Replicate a campaign in saved or send status.

    :API_KEY: String used for authentication purposes.
    :SERVER_PREFIX: String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :campaign_id: (str,required) - The unique id for the campaign.

    :return: response object from MailChimp API containing A summary of an individual campaign's settings and content.
    :rtype: dict
    """
    try:
        creds = json.loads(cred)
        API_KEY = creds["apiKey"]
        SERVER_PREFIX = creds["serverPrefix"]
        campaign_id = params.get("campaign_id", None)
        if "apiKey" in creds and "serverPrefix" in creds and campaign_id:
            data = {"campaign_id": campaign_id}
            mailchimp = create_client_instance(API_KEY, SERVER_PREFIX)
            try:
                response = mailchimp.campaigns.replicate(**data)
            except ApiClientError as error:
                raise Exception(f"Mailchimp API error: {error.text}")
            else:
                return response
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(f"Error replicating campain: {e}")

def mailchimp_delete_campaign(cred,params):
    """
    Remove a campaign from your Mailchimp account.

    :API_KEY: String used for authentication purposes.
    :SERVER_PREFIX: String used for authentication purposes.
    :params: Dictionary containing parameters.

    - :campaign_id: (str,required) - The unique id for the campaign.

    :return: response object from MailChimp API in case of failure, otherwise a dictionary indicating the success of the operation
    :rtype: dict
    """
    try:
        creds = json.loads(cred)
        API_KEY = creds["apiKey"]
        SERVER_PREFIX = creds["serverPrefix"]
        campaign_id = params.get("campaign_id", None)
        if "apiKey" in creds and "serverPrefix" in creds and campaign_id:
            data = {"campaign_id": campaign_id}
            mailchimp = create_client_instance(API_KEY, SERVER_PREFIX)
            try:
                response = mailchimp.campaigns.remove(**data)
            except ApiClientError as error:
                raise Exception(f"Mailchimp API error: {error.text}")
            else:
                return reply_upon_success(response)
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(f"Error deleting campain: {e}")
