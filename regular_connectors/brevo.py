import base64
from sib_api_v3_sdk.rest import ApiException
from sib_api_v3_sdk import Configuration,ApiClient,ContactsApi,CreateContact,TransactionalEmailsApi,SendSmtpEmail,SendSmtpEmailSender,SendSmtpEmailAttachment
import json
def create_sendinblue_api_instance(creds):
    try:
        configuration = Configuration()
        configuration.api_key['api-key'] = creds['apiKey']
        return configuration
    except ApiException as e:
        raise Exception(f"Exception when creating brevo API instance:{e}")
    
def brevo_get_contacts(cred,params):
    """
    Get a list of contacts.

    :param str api_key: Brevo API key. (required)
    :param dict params:
        - limit (int): Limit the number of contacts to retrieve. (optional)

    :return: Information about the contacts obtained from the Brevo API.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        instance = create_sendinblue_api_instance(creds)
        api_instance = ContactsApi(ApiClient(instance))
        api_response = api_instance.get_contacts(**params)
        return api_response.to_dict()

    except ApiException as e:
        raise Exception(e)

def brevo_get_contact(cred,params):
    """
    Get information about a specific contact.

    :param str api_key: Brevo API key. (required)
    :param dict params:
        - identifier (int): Identifier of the contact to retrieve. (required)

    :return: Information about the contact obtained from the Brevo API.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'identifier' in params:
            instance = create_sendinblue_api_instance(creds)
            api_instance = ContactsApi(ApiClient(instance))
            api_response = api_instance.get_contact_info(**params)
            api_response_json = api_response.to_dict()
            return api_response_json
        else:
            raise Exception("Missing input data")
    except ApiException as e:
        raise Exception(e)
    
def brevo_create_contact(cred,params):
    """
    Create a new contact.

    :param str api_key: Brevo API key. (required)
    :param dict params:
        - email (str): Email address of the contact. (required)
        - attributes (dict): Additional attributes of the contact. (optional)

    :return: Information about the created contact obtained from the Brevo API.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'email' in params:
            instance = create_sendinblue_api_instance(creds)
            api_instance = ContactsApi(ApiClient(instance))
            contact = CreateContact(**params)
            api_response = api_instance.create_contact(create_contact=contact)
            api_response_json = api_response.to_dict()
            return api_response_json
        else:
            raise Exception("Missing input data")
    except ApiException as e:
        raise Exception(e)

def brevo_delete_contact(cred,params):
    """
    Delete a contact.

    :param str api_key: Brevo API key. (required)
    :param dict params:
        - identifier (int): Identifier of the contact to delete. (required)

    :return: Confirmation message indicating the deletion was successful.
    :rtype: str
    """
    try:
        creds=json.loads(cred)
        if 'identifier' in params:
            instance = create_sendinblue_api_instance(creds)
            api_instance = ContactsApi(ApiClient(instance))
            api_response = api_instance.delete_contact(**params)
            return "Deleted Successfully"
        else:
            raise Exception("Missing input data")
    except ApiException as e:
        raise Exception(e)

def brevo_send_transactional_email(cred,params):
    """
    Send a transactional email using Brevo.
    :param str api_key: Brevo API key. (required)
    :param dict params:
        - sender (dict): Information about the email sender. (required)
        - to (list): List of email recipients. (required)
        - subject (str): Subject of the email. (required)
        - text_content (str): Plain text content of the email. Either `text_content` or `html_content` is required. (optional)
        - html_content (str): HTML content of the email. Either `text_content` or `html_content` is required. (optional)
        - attachments (list): List of attachments to include in the email. (optional)
        - cc (list): List of email recipients to CC. (optional)
        - bcc (list): List of email recipients to BCC. (optional)
        - tags (list): List of tags to associate with the email. (optional)

    :return: Information about the sent email obtained from the Brevo API.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'sender' in params and 'to' in params and 'subject' in params and ('html_content' in params or 'text_content' in params):
            sender_data = params.pop('sender')
            instance = create_sendinblue_api_instance(creds)
            api_instance = TransactionalEmailsApi(ApiClient(instance))            
            if 'attachments' in params:
                attachments = params.pop('attachments')
                send_smtp_email = SendSmtpEmail(sender=SendSmtpEmailSender(**sender_data), **params)
                attachment_objs = []
                for attachment in attachments:
                    if 'url' in attachment:
                        if 'name' in attachment:
                            attachment_objs.append(SendSmtpEmailAttachment(url=attachment['url'], name=attachment['name']))
                        else:
                            attachment_objs.append(SendSmtpEmailAttachment(url=attachment['url']))
                    elif 'content' in attachment and 'name' in attachment:
                        if isinstance(attachment['content'], bytes):
                            content_base64 = base64.b64encode(attachment['content']).decode('utf-8')
                            attachment_objs.append(SendSmtpEmailAttachment(content=content_base64, name=attachment['name']))
                        else:
                            raise Exception("Attachment content should be in bytes format.")
                    else:
                        raise Exception("Missing required attributes for attachment.")
                
                send_smtp_email.attachment = attachment_objs
            else:
                send_smtp_email = SendSmtpEmail(sender=SendSmtpEmailSender(**sender_data), **params)
            api_response = api_instance.send_transac_email(send_smtp_email)
            api_response_json = api_response.to_dict()
            return api_response_json
        else:
            raise Exception("Missing input data")
    except ApiException as e:
        raise Exception(e)



