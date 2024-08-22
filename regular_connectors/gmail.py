from googleapiclient.discovery import build
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import json,re
import logging


def create_service(access_token, API_SERVICE_NAME, API_VERSION):
    try:
        creds_data = json.loads(access_token)
        creds = Credentials.from_authorized_user_info(creds_data)
        if creds and creds.expired and creds.refresh_token:
            # in this case the token is expired and we need to get a new access token
            creds.refresh(Request())
        service = build(
            API_SERVICE_NAME, API_VERSION, credentials=creds, static_discovery=False
        )

        logging.warning(API_SERVICE_NAME, API_VERSION, 'service created successfully')
        return service
    except Exception as e:
        logging.warning(f'Failed to create service instance for {e}')
        raise Exception(f'Failed to create service instance {e}')


def create_token(cred):
    try:
        result={}
        result['token']=cred['accessToken']
        result['refresh_token']=cred['refreshToken']
        result['token_uri']="https://oauth2.googleapis.com/token"
        result['client_id']=cred['clientID']
        result['client_secret']=cred['clientSecret']
        result['scopes']=["https://mail.google.com/"]
        result['expiry']=cred['expirey']
        return json.dumps(result)
    except Exception as e:
        raise Exception(e)
##################################### here comes the code ##########################################


################################################# Messages #########################################


def gmail_addLabel(creds,API_SERVICE_NAME, API_VERSION, request):
    """
     Adds a label, which is A mechanism for organizing messages and threads, to a specific message.

    :param str access_token: (str,required) Used for authentication. 
    :param str API_SERVICE_NAME: (str,required) for the calendar, it's 'gmail'
    :param str API_VERSION: (str,required) the version used is v1  
    :param dict request: contains properties to be added to the updated paymentIntent
       
        - :message_id: (str,REQUIRED) the message id , to which the label will be added
        - :label_id: (str,REQUIRED) The Id of the label to be added 
        - :label_name: (str) The name of the label to be added
        
    :return: Details containing the Labels added to the message
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
        message_id = request.get("message_id", "")
        label_id = request.get("label_id", "")
        label_name = request.get("label_name", "")

        if not (label_id or label_name):
            raise Exception("Missing input data")

        # Get the label ID if label_name is provided
        if label_name:
            labels = service.users().labels().list(userId="me").execute()
            for label in labels["labels"]:
                if label["name"] == label_name:
                    label_id = label["id"]
                    break

        # Add the label to the message
        if label_id:
            return (
                service.users()
                .messages()
                .modify(userId="me", id=message_id, body={"addLabelIds": [label_id]})
                .execute()
            )

    except Exception as e:
        raise Exception(e)


def gmail_deleteMessage(creds,API_SERVICE_NAME, API_VERSION, request):
    """
     Immediately and permanently deletes the specified message. This operation cannot be undone.

    :param str access_token: (str,required) Used for authentication. 
    :param str API_SERVICE_NAME: (str,required) for the calendar, it's 'gmail'
    :param str API_VERSION: (str,required) the version used is v1
    :param dict request: contains the id of the message to be deleted and the user Id
       
        - :userId: (str,REQUIRED) The user's email address. The special value me can be used to 
                                  indicate the authenticated user.
        - :message_id: (str,REQUIRED) The ID of the message to delete.
      
        
    :return: Success or failure of the deletion process of the message
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
        message_id = request.get("message_id", "")
        if not message_id:
            raise Exception("Missing input data")
        service.users().messages().delete(
            userId="me", id=request["message_id"]
        ).execute()
        return {"Result": f"Deleted Message ID: {message_id}"}
    except Exception as e:
        raise Exception(e)


def gmail_getMessage(creds,API_SERVICE_NAME, API_VERSION, request):
    """
     Gets the specified message.

    :param str access_token: (str,required) Used for authentication. 
    :param str API_SERVICE_NAME: (str,required) for the calendar, it's 'gmail'
    :param str API_VERSION: (str,required) the version used is v1
    :param dict request: contains the id of the message to be returned,and the user Id
       
        - :userId: (str,REQUIRED) The user's email address. The special value me can be used to 
                                  indicate the authenticated user.
        - :message_id: (str,REQUIRED) The ID of the message to be retrieved.
      
        
    :return: If successful, the response body contains an instance of Message.
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
        scope = request.get("scope", "single")

        if scope == "single":
            message_id = request.get("message_id", "")
            if not message_id:
                raise Exception("Missing input data")
            message = (
                service.users().messages().get(userId="me", id=message_id).execute()
            )
            return message
        elif scope == "all":
            label_ids = request.get("labelIds", [])
            max_results = request.get("maxResults", 5)
            spamTrash = request.get("includeSpamTrash", False)
            messages = (
                service.users()
                .messages()
                .list(
                    userId="me",
                    labelIds=label_ids,
                    maxResults=max_results,
                    includeSpamTrash=spamTrash,
                )
                .execute()
            )
            return messages

        else:
            raise Exception("Invalid scope specified")

    except Exception as e:
        raise Exception(e)


def gmail_markAsRead(creds,API_SERVICE_NAME, API_VERSION, request):
    """
     Removes the 'UNREAD' label from a message 

    :param str access_token: (str,required) Used for authentication. 
    :param str API_SERVICE_NAME: (str,required) for the calendar, it's 'gmail'
    :param str API_VERSION: (str,required) the version used is v1
    :param dict request: contains paramaters to be added to the message
       
        - :userId: (str,REQUIRED) The user's email address. The special value me can be used to 
                                  indicate the authenticated user.
        - :message_id: (str,REQUIRED) The ID of the message whose label is to be changed.
        
    :return: Details containing the Labels attached to the message
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
        message_id = request.get("message_id", "")
        if not message_id:
            raise Exception("Missing input data")

        body = {"removeLabelIds": ["UNREAD"]}
        return (
            service.users()
            .messages()
            .modify(userId="me", id=message_id, body=body)
            .execute()
        )
    except Exception as e:
        raise Exception(e)


def gmail_markAsUnread(creds,API_SERVICE_NAME, API_VERSION, request):
    """
     Adds the 'UNREAD' label from a message 

    :param str access_token: (str,required) Used for authentication. 
    :param str API_SERVICE_NAME: (str,required) for the calendar, it's 'gmail'
    :param str API_VERSION: (str,required) the version used is v1
    :param dict request: contains paramaters to be added to the message
       
        - :userId: (str,REQUIRED) The user's email address. The special value me can be used to 
                                  indicate the authenticated user.
        - :message_id: (str,REQUIRED) The ID of the message whose label is to be changed.
        
    :return: Details containing the Labels attached to the message
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
        message_id = request.get("message_id", "")
        if not message_id:
            raise Exception("Missing input data")

        body = {"addLabelIds": ["UNREAD"]}
        return (
            service.users()
            .messages()
            .modify(userId="me", id=request["message_id"], body=body)
            .execute()
        )
    except Exception as e:
        raise Exception(e)


def gmail_removeLabel(creds,API_SERVICE_NAME, API_VERSION, request):
    """
     Removes a specific label from a message 

    :param str access_token: (str,required) Used for authentication. 
    :param str API_SERVICE_NAME: (str,required) for the calendar, it's 'gmail'
    :param str API_VERSION: (str,required) the version used is v1
    :param dict request: contains paramaters to be added to the message
       
        - :userId: (str,REQUIRED) The user's email address. The special value me can be used to 
                                  indicate the authenticated user.
        - :message_id: (str,REQUIRED) The ID of the message whose label is to be changed(or added).
        - :label_id:  (str,REQUIRED) The ID of the label to be removed from a message.
        
    :return: Details containing the Labels attached to the message
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
        message_id = request.get("message_id", "")
        label_id = request.get("label_id", "")
        label_name = request.get("label_name", "")

        if not (label_id or label_name):
            raise Exception("Missing input data")

        # Get the label ID if label_name is provided
        if label_name:
            labels = service.users().labels().list(userId="me").execute()
            for label in labels["labels"]:
                if label["name"] == label_name:
                    label_id = label["id"]
                    break

        # Remove the label from the message
        if label_id:
            return (
                service.users()
                .messages()
                .modify(userId="me", id=message_id, body={"removeLabelIds": [label_id]})
                .execute()
            )

    except Exception as e:
        raise Exception(e)


def gmail_replyToMessage(creds,API_SERVICE_NAME, API_VERSION, request):
    
    """
     Removes a specific label from a message 

    :param str access_token: (str,required) Used for authentication. 
    :param str API_SERVICE_NAME: (str,required) for the calendar, it's 'gmail'
    :param str API_VERSION: (str,required) the version used is v1
    :param dict request: contains paramaters to be added to the message
       
        - :in_reply_to: (str,REQUIRED) The ID of the message to reply to.
        - :message:  (str,REQUIRED) The message body
        - :type:  (str) The type of email
        - :attachments_list:  (dict) Attachments are of two types: URL,ByteString
                type,name,url.
        - :bcc_recipients: (arr) to send an email to multiple people without each recipient knowing the email details of the others.
        - :cc_recipients:  (arr) to send an email to multiple people with each recipient knowing the email details of the others.
        
    :return: Details about the reply message 
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        to = ""
        subject = ""
        # id of the message we're replying to
        in_reply_to = request.get("in_reply_to", None)
        email_type = request.get("type", "plain")
        cc = request.get("cc_recipients", None)
        bcc = request.get("bcc_recipients", None)
        message = request.get("message", None)  # this is the message body
        attachments = request.get("attachments_list", None)
        # Test required fields
        if "in_reply_to" not in request and "message" not in request:
            raise Exception("Missing input data")

        service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
        # find the destination for the reply using in_reply_to
        original_message = (
            service.users().messages().get(userId="me", id=in_reply_to).execute()
        )
        thread_id = original_message.get("threadId", None)
        for header in original_message["payload"]["headers"]:
            if header["name"] == "From":
                to += header["value"]
            if header["name"] == "subject":
                subject = header["value"]

        mimeMessage = MIMEMultipart()
        # Fill mimeMessage fields
        mimeMessage["In-Reply-To"] = in_reply_to
        mimeMessage["References"] = in_reply_to
        mimeMessage["subject"] = "Reply :" + str(subject)
        mimeMessage["to"] = to
        mimeMessage["cc"] = cc
        mimeMessage["bcc"] = bcc
        email_content = MIMEText(message, email_type)

        # Add body content
        mimeMessage.attach(email_content)

        if attachments:
            for attach in attachments:
                if attach["type"] == "URL":
                    response = requests.get(attach["url"])
                    if response.status_code == 200:
                        content = response.content
                        # Extract the file name from the URL or provide a default name
                        filename = attach["name"]
                        # Create an attachment
                        attachment = MIMEBase("application", "octet-stream")
                        attachment.set_payload(content)
                        encoders.encode_base64(attachment)
                        attachment.add_header(
                            "Content-Disposition", "attachment", filename=filename
                        )
                        mimeMessage.attach(attachment)
                else:  # type = ByteString
                    payload = MIMEBase("application", "octet-stream")
                    payload.set_payload(attach["content"])
                    encoders.encode_base64(payload)
                    payload.add_header(
                        "Content-Disposition", "attachment", filename=attach["name"]
                    )
                    mimeMessage.attach(payload)

        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
        return (
            service.users()
            .messages()
            .send(userId="me", body={"raw": raw_string, "threadId": thread_id})
            .execute()
        )
    except Exception as e:
        raise Exception(e)


def gmail_sendMessage(creds,API_SERVICE_NAME, API_VERSION, request):
     
    """
    Sends the specified message to the recipients in the To, Cc, and Bcc headers.

    :param str access_token: (str,required) Used for authentication. 
    :param str API_SERVICE_NAME: (str,required) for the calendar, it's 'gmail'
    :param str API_VERSION: (str,required) the version used is v1
    :param dict request: contains paramaters to be added to the message
       
        - :to: (str,REQUIRED) The email of the user to whom the message is sent.
        - :body:  (str,REQUIRED) The message body
        - :cc:  (str) to send an email to multiple people without each recipient knowing the email details of the others.
        - :bcc:  (str) to send an email to multiple people with each recipient knowing the email details of the others.
        - :subject: (str) the subject of the message.
        - :attachments_list: (dict) Attachments are of two types: URL,ByteString
                type,name,url.
        - :type: (str) the type of email.
        
    :return: Details about the reply message 
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        to = request.get("to", None)
        body = request.get("body", None)
        cc = request.get("cc", None)
        bcc = request.get("bcc", None)
        subject = request.get("subject", None)
        attachments = request.get("attachments_list", None)
        type = request.get("type", "plain")
        # Test required fields
        if not to or not body:
            raise Exception("Missing input data")        
        service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
        mimeMessage = MIMEMultipart()

        # Fill mimeMessage fields
        if to:
            mimeMessage["to"] = to
        if cc:
            mimeMessage["cc"] = cc
        if bcc:
            mimeMessage["bcc"] = bcc
        if subject:
            mimeMessage["subject"] = subject

        email_content = MIMEText(body, type)
        # Add body content
        mimeMessage.attach(email_content)

        if attachments:
            for attach in attachments:
                if attach["type"] == "URL":
                    response = requests.get(attach["url"])
                    if response.status_code == 200:
                        content = response.content
                        # Extract the file name from the URL or provide a default name
                        filename = attach["name"]
                        # Create an attachment
                        attachment = MIMEBase("application", "octet-stream")
                        attachment.set_payload(content)
                        encoders.encode_base64(attachment)
                        attachment.add_header(
                            "Content-Disposition", "attachment", filename=filename
                        )
                        mimeMessage.attach(attachment)
                else:  # type = ByteString
                    payload = MIMEBase("application", "octet-stream")
                    payload.set_payload(attach["content"])
                    encoders.encode_base64(payload)
                    payload.add_header(
                        "Content-Disposition", "attachment", filename=attach["name"]
                    )
                    mimeMessage.attach(payload)

        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

        return (
            service.users()
            .messages()
            .send(userId="me", body={"raw": raw_string})
            .execute()
        )

    except Exception as e:
        raise Exception(e)

################################################# Threads #########################################


def gmail_addLabelToThread(creds,API_SERVICE_NAME, API_VERSION, request):
    """
     Adds a list of labels, which is A mechanism for organizing messages and threads, to a specific thread.

    :param str access_token: (str,required) Used for authentication. 
    :param str API_SERVICE_NAME: (str,required) for the calendar, it's 'gmail'
    :param str API_VERSION: (str,required) the version used is v1  
    :param dict request: contains properties to be added to the updated paymentIntent
       
        - :thread_id: (str,REQUIRED) the thread id , to which the label will be added
        - :label_ids: (str,REQUIRED) The Id of the label to be added 
        
    :return: Details containing the Labels added to the thread
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
        thread_id = request.get("thread_id", "")
        ids = request.get("label_ids", None)
        label_ids = [id.strip() for id in ids.split(",")]

        if not (thread_id and label_ids):
            raise Exception("Missing input data")

        return (
            service.users()
            .threads()
            .modify(userId="me", id=thread_id, body={"addLabelIds": label_ids})
            .execute() 
        )

    except Exception as e:
        raise Exception(e)


def gmail_deleteThread(creds,API_SERVICE_NAME, API_VERSION, request):
    """
     Immediately and permanently deletes the specified thread. Any messages that belong to the thread are also deleted.

    :param str access_token: (str,required) Used for authentication. 
    :param str API_SERVICE_NAME: (str,required) for the calendar, it's 'gmail'
    :param str API_VERSION: (str,required) the version used is v1
    :param dict request: contains the id of the thread to be deleted and the user Id
       
        - :userId: (str,REQUIRED) The user's email address. The special value me can be used to 
                                  indicate the authenticated user.
        - :thread_id: (str,REQUIRED) The ID of the thread to delete.
      
        
    :return: Success or failure of the deletion of the thread
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
        thread_id = request.get("thread_id", "")

        if not thread_id:
            raise Exception("Missing input data")

        service.users().threads().delete(userId="me", id=thread_id).execute()
        return {"Result": f"Deleted Thread ID: {thread_id}"}

    except Exception as e:
        raise Exception(e)


def gmail_getThreads(creds,API_SERVICE_NAME, API_VERSION, request):
    """
     Returns a list of threads,where each thread is a collection of related messages forming a conversation.

    :param str api_key: Used for authentication purposes. 
    :param dict params: contains properties to be filtered in the request
       
        - :scope: (str,REQUIRED) possible values are single , all .
        - :thread_id: (str) the id of the thread to be returned 
        - :limit: (str) Maximum number of threads to return. This field defaults to 100.
        - :includeSpamTrash:(bool) Include threads from SPAM and TRASH in the results.
    :return: list of returned threads.
    :rtype: dict
    """
    
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
        scope = request.get("scope", "")
        thread_id = request.get("thread_id", "")
        limit = request.get("limit", 100)

        if scope == "all":
            query = ""
            include_spam_trash = request.get("include_spam_trash", False)
            if include_spam_trash:
                query += "in:spam OR in:trash "

            label_ids = request.get("label_ids", "")
            if label_ids:
                query += "label:" + label_ids + " "

            search = request.get("search", "")
            if search:
                query += search + " "

            read_status = request.get("read_status")
            if read_status:
                if read_status == "all":
                    query += "is:read OR is:unread "
                elif read_status == "unread":
                    query += "is:unread "
                elif read_status == "read":
                    query += "is:read "

            received_after = request.get("received_after", "")
            if received_after:
                query += "after:" + received_after + " "

            received_before = request.get("received_before", "")
            if received_before:
                query += "before:" + received_before + " "

            if query:
                threads = (
                    service.users()
                    .threads()
                    .list(userId="me", q=query, maxResults=limit)
                    .execute()
                )

            else:
                threads = (
                    service.users()
                    .threads()
                    .list(userId="me", maxResults=limit)
                    .execute()
                )

            all_threads = threads.get("threads", [])
            return {"all_threads": all_threads}

        elif scope == "single":
            if not thread_id:
                raise Exception("Missing input data")

            thread = service.users().threads().get(userId="me", id=thread_id).execute()

            return thread
        raise Exception("Missing input data")

    except Exception as e:
        raise Exception(e)


def gmail_removeLabelFromThread(creds,API_SERVICE_NAME, API_VERSION, request):
    """
     Removes a list of labels, which is A mechanism for organizing messages and threads, from a specific thread.

    :param str access_token: (str,required) Used for authentication. 
    :param str API_SERVICE_NAME: (str,required) for the calendar, it's 'gmail'
    :param str API_VERSION: (str,required) the version used is v1  
    :param dict request: contains thread and label ids 
        - :thread_id: (str,REQUIRED) the thread id , to which the label will be added
        - :label_ids: (str,REQUIRED) The Id of the label to be removed 
        
    :return: Success or failure of the operation
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        service = create_service(access_token, API_SERVICE_NAME, API_VERSION)

        thread_id = request.get("thread_id", "")
        label_ids_str = request.get("label_ids", "")

        if not thread_id or not label_ids_str:
            raise Exception("Missing input data")

        label_ids = [id.strip() for id in label_ids_str.split(",")]
        labels = service.users().labels().list(userId="me").execute()
        labels_to_remove = []

        for label_id in label_ids:
            id = None
            for label in labels.get("labels", []):
                if label["id"] == label_id:
                    id = label["id"]
                    break
            if id:
                labels_to_remove.append(id)
            else:
                raise Exception(f"Label with id '{label_id}' not found.")

        return (
            service.users()
            .threads()
            .modify(
                userId="me", id=thread_id, body={"removeLabelIds": labels_to_remove}
            )
            .execute()
        )

    except Exception as e:
        raise Exception(e)


def get_message_subject(id, service):
    """
     Removes a list of labels, which is A mechanism for organizing messages and threads, from a specific thread.

    :param str access_token: (str,required) Used for authentication. 
    :param str API_SERVICE_NAME: (str,required) for the calendar, it's 'gmail'
    :param str API_VERSION: (str,required) the version used is v1  
    :param dict request: contains thread and label ids 
    
        - :thread_id: (str,REQUIRED) the thread id , to which the label will be added
        - :label_ids: (str,REQUIRED) The Id of the label to be removed 
        
    :return: Success or failure of the operation
    :rtype: dict
    """
    message = service.users().messages().get(userId="me", id=id).execute()
    print(f"in get_message_subject : {message['subject']}")
    return message["subject"]


def forge_reply(message_id, service):
    """
        Sends a reply to a certain messsage in a thread 

    :param str access_token: (str,required) Used for authentication. 
    :param str API_SERVICE_NAME: (str,required) for the calendar, it's 'gmail'
    :param str API_VERSION: (str,required) the version used is v1  
    :param dict request: contains thread  id and related details
    
        - :thread_id: (str,REQUIRED) the thread id , to which the message belongs
        
        - :message_id: (str,REQUIRED) The id of the message to reply to
        
    :return: Success or failure of the operation
    :rtype: dict
    """
    message = service.users().messages().get(userId="me", id=message_id).execute()
    reply = {"threadId": message["threadId"]}
    for header in message["payload"]["headers"]:
        if header["name"] == "From":
            reply["to"] = header["value"]
        if header["name"] == "Subject":
            reply["subject"] = header["value"]
    return reply


def gmail_replyToThread(creds,API_SERVICE_NAME, API_VERSION, request):
    """
     Replies to a thread 

    :param str access_token: (str,required) Used for authentication. 
    :param str API_SERVICE_NAME: (str,required) for the calendar, it's 'gmail'
    :param str API_VERSION: (str,required) the version used is v1  
    :param dict request: contains the thread details
    
        - :thread_id: (str,REQUIRED) the id of the thread to reply to 
        - :to_recipients: (arr) recipients of the message
        - :cc_recipients: (arr) to send an email to multiple people with each recipient knowing the email details of the others.
        - :bcc_recipients: (arr) to send an email to multiple people without each recipient knowing the email details of the others.
        - :subject: (str) the message content 
        - :message_body: (str)
        - :in_reply_to: (str) the id of the message to reply to
        - :message_snippet: (str) the message snippet 
        - :email_type: (str) the type of the email 
        - :attachments_list: (dict) Attachments are of two types: URL,ByteString
                     type,name,url.
        
        
    :return: Success or failure of the operation
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
        mimeMessage = MIMEMultipart()
        # Extract the request parameters
        to = request.get("to_recipients", "")
        thread_id = request.get("thread_id", None)
        cc = request.get("cc_recipients", None)
        bcc = request.get("bcc_recipients", None)
        subject = request.get("subject", "")
        message = request.get("message_body", None)
        # message_id for the reply
        in_reply_to = request.get("in_reply_to", None)
        message_snippet_id = request.get("message_snippet", None)
        email_type = request.get("email_type", "plain")
        attachments = request.get("attachments_list", None)

        if not thread_id and not message_snippet_id and not message:
            raise Exception("Missing input data")
        else:
            in_reply_to = message_snippet_id
            # Construct the email body

            mimeMessage["In-Reply-To"] = in_reply_to
            mimeMessage["References"] = in_reply_to
            # Fill the In-Reply-To field with the parent message ID
            reply = forge_reply(message_id=in_reply_to, service=service)
            if cc:
                mimeMessage["cc"] = cc
            if bcc:
                mimeMessage["bcc"] = bcc
            mimeMessage["subject"] = "Re :" + (subject or reply["subject"])
            mimeMessage["to"] = to or reply["to"]

            mimeMessage.attach(MIMEText(message, email_type))

            if attachments:
                for attach in attachments:
                    if attach["type"] == "URL":
                        response = requests.get(attach["url"])
                        if response.status_code == 200:
                            content = response.content
                            # Extract the file name from the URL or provide a default name
                            filename = attach["name"]
                            # Create an attachment
                            attachment = MIMEBase("application", "octet-stream")
                            attachment.set_payload(content)
                            encoders.encode_base64(attachment)
                            attachment.add_header(
                                "Content-Disposition", "attachment", filename=filename
                            )
                            mimeMessage.attach(attachment)
                    else:  # type = ByteString
                        payload = MIMEBase("application", "octet-stream")
                        payload.set_payload(attach["content"])
                        encoders.encode_base64(payload)
                        payload.add_header(
                            "Content-Disposition", "attachment", filename=attach["name"]
                        )
                        mimeMessage.attach(payload)

            # Send the reply
            raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
            reply_message = {
                "raw": raw_string,
                "threadId": thread_id or reply["threadId"],
            }

            return (
                service.users()
                .messages()
                .send(userId="me", body=reply_message)
                .execute()
            )

    except Exception as e:
        raise Exception(e)


def gmail_trashThread(creds,API_SERVICE_NAME, API_VERSION, request):
    """
     Moves the specified thread to the trash. Any messages that belong to the thread are also moved to the trash.

    :param str access_token: (str,required) Used for authentication. 
    :param str API_SERVICE_NAME: (str,required) for the calendar, it's 'gmail'
    :param str API_VERSION: (str,required) the version used is v1
    :param dict request: contains the id of the thread to be trashed
       
        - :thread_id: (str,REQUIRED) The ID of the thread to be moved to trash.
      
        
    :return: If successful, the response body contains an instance of Thread.
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        thread_id = request.get("thread_id", "")
        if not thread_id:
            raise Exception("Missing input data")

        service = create_service(access_token, API_SERVICE_NAME, API_VERSION)

        # Trash the thread
        return service.users().threads().trash(userId="me", id=thread_id).execute()

    except Exception as e:
        raise Exception(e)


def gmail_untrashThread(creds,API_SERVICE_NAME, API_VERSION, request):
    """
     Removes the specified thread from the trash. Any messages that belong to the thread are also removed from the trash.

    :param str access_token: (str,required) Used for authentication. 
    :param str API_SERVICE_NAME: (str,required) for the calendar, it's 'gmail'
    :param str API_VERSION: (str,required) the version used is v1
    :param dict request: contains the id of the thread to be untrashed
       
        - :thread_id: (str,REQUIRED) The ID of the thread to be untrashed
      
    :return: If successful, the response body contains an instance of Thread.
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        thread_id = request.get("thread_id", "")
        if not thread_id:
            raise Exception("Missing input data")

        service = create_service(access_token, API_SERVICE_NAME, API_VERSION)

        # Trash the thread
        return service.users().threads().untrash(userId="me", id=thread_id).execute()

    except Exception as e:
        raise Exception(e)


################################################# Label@@@ #########################################


def gmail_createLabel(creds,API_SERVICE_NAME, API_VERSION, request):
    
    """
     Creates a label, which is A mechanism for organizing messages and threads, to a specific message.

    :param str access_token: (str,required) Used for authentication. 
    :param str API_SERVICE_NAME: (str,required) for the calendar, it's 'gmail'
    :param str API_VERSION: (str,required) the version used is v1
    :param dict request: contains properties to be added to the label
       
        - :name: (str,REQUIRED) The ID of the thread to be untrashed
        - :labelListVisibility: (enum) The visibility of the label in the label list in the Gmail web interface.
        - :messageListVisibility: (enum) The visibility of messages with this label 
      
    :return: If successful, the response body contains a newly created instance of Label.
    :rtype: dict
    """

    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
        name = request.get("name", "")
        if not name:
            raise Exception("Missing input data")
        label = {
            "name": name,
            "labelListVisibility": request.get("labelListVisibility", "labelShow"),
            "messageListVisibility": request.get("messageListVisibility", "show"),
        }

        created_label = (
            service.users().labels().create(userId="me", body=label).execute()
        )

        return created_label

    except Exception as e:
        raise Exception(e)


def gmail_deleteLabel(creds,API_SERVICE_NAME, API_VERSION, request):
    """
     Immediately and permanently deletes the specified label and removes it from any messages and threads that it is applied to.

    :param str access_token: (str,required) Used for authentication. 
    :param str API_SERVICE_NAME: (str,required) for the calendar, it's 'gmail'
    :param str API_VERSION: (str,required) the version used is v1
    :param dict request: contains the id of the label to be deleted 
       
        - :label_id: (str,REQUIRED) the id of the label to be deleted
    :return: Success or failure of the deletion of the label
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
        label_id = request.get("label_id", "")

        if not label_id:
            raise Exception("Missing input data")

        service.users().labels().delete(userId="me", id=label_id).execute()
        return {"Result": f"Deleted Label ID: {label_id}"}
    except Exception as e:
        raise Exception(e)


def gmail_getLabels(creds,API_SERVICE_NAME, API_VERSION, request):
    """
     Lists all labels in the user's mailbox.

    :param str access_token: (str,required) Used for authentication. 
    :param str API_SERVICE_NAME: (str,required) for the calendar, it's 'gmail'
    :param str API_VERSION: (str,required) the version used is v1
    :param dict request: contains the id of the label to be deleted 
       
        - :label_id: (str,REQUIRED) the id of the label to be returned
         - :label_id: (str,REQUIRED) the id of the label to be returned
    :return: Success or failure of the deletion of the label
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
        scope = request.get("scope", "")
        label_id = request.get("label_id", "")
        limit = request.get("limit", 100)

        if scope == "all":
            labels = service.users().labels().list(userId="me").execute()
            all_labels = labels.get("labels", [])
            if limit and limit > 0:
                all_labels = all_labels[:limit]
            return {"labels": all_labels}

        elif scope == "single" and label_id:
            if not label_id:
                raise Exception("Missing input data")
            label = service.users().labels().get(userId="me", id=label_id).execute()
            return label
        raise Exception("Missing input data")

    except Exception as e:
        raise Exception(e)


################################################# Drafts## #########################################


def gmail_createDraft(creds,API_SERVICE_NAME, API_VERSION, request):
    """
     Creates a draft, which is an unsent message. A message contained within the draft can be replaced.

    :param str api_key: Used for authentication purposes. 
    :param dict params: contains properties to be added to the draft
    
    
        - :subject: (str,REQUIRED) the id of the payment to be modified
        - :to: (str,REQUIRED) the recipient email
        - :type: (str) email type
        - :body: (str,REQUIRED) contains the item 'enabled' (bool)
        - :attachments_list: (dict) Attachments are of two types: URL,ByteString
                type,name,url.
        - :cc_recipients: (arr) to send an email to multiple people with each recipient knowing the email details of the others.
        - :bcc_recipients: (arr) to send an email to multiple people without each recipient knowing the email details of the others.
        
    :return: Details about the created draft
    :rtype: dict
    """
    
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
        mimeMessage = MIMEMultipart()
        attachments_list = None
        attachments_type = None

        to = request.get("to", None)
        body = request.get("body", None)
        cc = request.get("cc", None)
        bcc = request.get("bcc", None)
        subject = request.get("subject", None)
        attachments = request.get("attachments_list", None)
        type = request.get("type", "plain")
        # Test required fields
        if not to or not body:
            raise Exception("Missing input data")

        # Fill mimeMessage fields
        if to:
            mimeMessage["to"] = to
        if cc:
            mimeMessage["cc"] = cc
        if bcc:
            mimeMessage["bcc"] = bcc
        if subject:
            mimeMessage["subject"] = subject

        email_content = MIMEText(body, type)
        # Add body content
        mimeMessage.attach(email_content)
        if attachments:
            for attach in attachments:
                if attach["type"] == "URL":
                    response = requests.get(attach["url"])
                    if response.status_code == 200:
                        content = response.content
                        # Extract the file name from the URL or provide a default name
                        filename = attach["name"]
                        # Create an attachment
                        attachment = MIMEBase("application", "octet-stream")
                        attachment.set_payload(content)
                        encoders.encode_base64(attachment)
                        attachment.add_header(
                            "Content-Disposition", "attachment", filename=filename
                        )
                        mimeMessage.attach(attachment)
                else:  # type = ByteString
                    payload = MIMEBase("application", "octet-stream")
                    payload.set_payload(attach["content"])
                    encoders.encode_base64(payload)
                    payload.add_header(
                        "Content-Disposition", "attachment", filename=attach["name"]
                    )
                    mimeMessage.attach(payload)

        draft = {
            "message": {
                "raw": base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
            }
        }

        return service.users().drafts().create(userId="me", body=draft).execute()

    except Exception as e:
        raise Exception(e)


def gmail_deleteDraft(creds,API_SERVICE_NAME, API_VERSION, request):
    """
     Immediately and permanently deletes the specified draft. Does not simply trash it.

    :param str api_key: Used for authentication purposes. 
    :param dict params: contains draft id to be deleted.
    
        - :draft_id: (str,REQUIRED) the id of the draft to be deleted.
       
    :return: Success / Failure of the deletion request
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
        draft_id = request.get("draft_id", "")
        if not draft_id:
            raise Exception("Missing input data")
        service.users().drafts().delete(userId="me", id=request["draft_id"]).execute()
        return {"Result": f"Deleted Draft ID: {draft_id}"}

    except Exception as e:
        raise Exception(e)


def gmail_getDraft(creds,API_SERVICE_NAME, API_VERSION, request):
    """
     Gets the specified draft.

    :param str api_key: Used for authentication purposes. 
    :param dict params: contains draft id to be retrieved and filters
    
        - :draft_id: (str,REQUIRED) the id of the draft to be retrieved.
        - :scope: (str,REQUIRED) possible values are single , all . 
       
    :return: If successful, the response body contains an instance of Draft.
    :rtype: dict
    """
    try:
        cred=json.loads(creds)
        access_token=create_token(cred)
        service = create_service(access_token, API_SERVICE_NAME, API_VERSION)
        scope = request.get("scope", "")
        # Default to 100 if 'limit' is not provided
        limit = request.get("limit", 100)

        if scope == "all":
            all_drafts = service.users().drafts().list(userId="me").execute()
            drafts = all_drafts.get("drafts", [])

            if limit and limit > 0:
                drafts = drafts[:limit]

            return {"drafts": drafts}

        elif scope == "single":
            draft_id = request.get("draft_id", "")
            if not draft_id:
                raise Exception("Missing input data")

            return service.users().drafts().get(userId="me", id=draft_id).execute()

        raise Exception("Missing input data")

    except Exception as e:
        raise Exception(e)
