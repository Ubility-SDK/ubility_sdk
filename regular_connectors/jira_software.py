import io
from jira import JIRA, JIRAError
import requests
import json

def authenticate(creds):
    response = requests.get(creds['domain'])
    if response.status_code == 200:
        jira = JIRA(server=creds['domain'],
                basic_auth=(creds['email'], creds['apiToken']))
        return jira
    else:
        raise Exception('error: Incorrect domain, server responded with status code ' + str(response.status_code))
    
def jira_get_issues(params,cred):
    """
    Retrieve Jira issues based on specified parameters.

    :param dict params:
        - jql_str (dict): Jira Query Language (JQL) string parameters.
            - project (str): Jira project key. (required)
            - status (str): Desired issue status. (optional)
        - maxResults (int): Maximum number of issues to return. (optional)
        - expand (str): Additional information to include in the response. (optional)
        - fields (str): Comma-separated list of fields to include in the response. (optional)
        - properties (str): Comma-separated list of issue properties to include in the response. (optional)

    :param str email: User email for Jira authentication. (required)
    :param str api_token: Jira API token for authentication. (required)
    :param str server: Jira server URL. (required)

    :return: List of Jira issues as dictionaries.
    :rtype: list
    """
    try:
        creds=json.loads(cred)
        if 'email' in creds and 'apiToken' in creds and 'domain' in creds and 'jql_str' in params:
            jira = authenticate(creds)
            data = {}
            jql_parts = []
            for key, value in params.items():
                if key=='jql_str':
                    jql_sub_parts = [f"{sub_key}={sub_value}" for sub_key, sub_value in value.items()]
                    jql_parts.append(' AND '.join(jql_sub_parts))
                elif value:
                    data[key] = value
            jql_query = ' AND '.join(jql_parts)
            issues = jira.search_issues(jql_query,**data)
            issue_list = []
            for issue in issues:
                issue_dict = issue.raw
                issue_list.append(issue_dict)
            return issue_list
        else:
            raise Exception('error: Missing input data')
    except JIRAError as http_error:
        raise JIRAError(f"error: {str(http_error)}")
    except Exception as e:
        raise Exception(f"error: {str(e)}")
    
def jira_get_issue(params,cred):
    """
    Retrieve details of a specific Jira issue.

    :param dict params:
        - id (str): Jira issue ID. (required)
        - expand (str): Additional information to include in the response. (optional)
        - fields (str): Comma-separated list of fields to include in the response. (optional)
        - properties (str): Comma-separated list of issue properties to include in the response. (optional)

    :param str email: User email for Jira authentication. (required)
    :param str api_token: Jira API token for authentication. (required)
    :param str server: Jira server URL. (required)

    :return: Dictionary containing details of the specified Jira issue.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'email' in creds and 'apiToken' in creds and 'domain' in creds and 'id' in params:
            jira = authenticate(creds)
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            get_issue = jira.issue(**data)
            issue_dict = get_issue.raw
            return issue_dict
        else:
            raise Exception('error: Missing input data')
    except JIRAError as http_error:
        raise JIRAError(f"error: {str(http_error)}")
    except Exception as e:
        raise Exception(f"error: {str(e)}")



def jira_create_issue(params,cred):
    """
    Create a new Jira issue.

    :param dict params:
        - project (str): Key or ID of the Jira project. (required)
        - issuetype (str): Type of the issue. (required)
        - summary (str): Summary or title of the issue. (required)
        - description (str): Description of the issue. (optional)
        - reporter (dict): Dictionary containing information about the reporter.
            - id (str): ID of the reporter. (optional)
        - assignee (str): User ID or name to assign the issue. (optional)

    :param str email: User email for Jira authentication. (required)
    :param str api_token: Jira API token for authentication. (required)
    :param str server: Jira server URL. (required)

    :return: Dictionary containing details of the created Jira issue.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'email' in creds and 'apiToken' in creds and 'domain' in creds and 'project' in params and 'issuetype' in params and 'summary' in params:
            jira = authenticate(creds)
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            new_issue = jira.create_issue(**data)
            return new_issue.raw
        else:
            raise Exception('error: Missing input data')
    except JIRAError as http_error:
        raise JIRAError(f"error: {str(http_error)}")
    except Exception as e:
        raise Exception(f"error: {str(e)}")


def jira_delete_issue(params,cred):
    """
    Delete a Jira issue.

    :param dict params:
        - id (str): ID of the Jira issue to delete. (required)

    :param str email: User email for Jira authentication. (required)
    :param str api_token: Jira API token for authentication. (required)
    :param str server: Jira server URL. (required)

    :return: Success message indicating the deletion of the Jira issue.
    :rtype: str
    """
    try:
        creds=json.loads(cred)
        if 'email' in creds and 'apiToken' in creds and 'domain' in creds and 'id' in params:
            jira = authenticate(creds)
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            issue = jira.issue(data['id'])
            optional_params = {}
            for key, value in data.items():
                if key != 'id':
                    optional_params[key] = value
            issue.delete(**optional_params)
            return f"Issue : Deleted successfully."
        else:
            raise Exception('error: Missing input data')
    except JIRAError as http_error:
        raise Exception(f"error: {str(http_error)}")
    except Exception as e:
        raise Exception(f"error: {str(e)}")

def jira_create_comment(params,cred):
    """
    Create a comment for a Jira issue.

    :param dict params:
        - issue (str): Key or ID of the Jira issue to comment on. (required)
        - body (str): Body text of the comment. (required)

    :param str email: User email for Jira authentication. (required)
    :param str api_token: Jira API token for authentication. (required)
    :param str server: Jira server URL. (required)

    :return: Information about the created comment.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'email' in creds and 'apiToken' in creds and 'domain' in creds and  'issue' in params and 'body' in params:
            jira = authenticate(creds)
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            new_comment = jira.add_comment(**data)
            return new_comment.raw
        else:
            raise Exception('error: Missing input data')
    except JIRAError as http_error:
        raise JIRAError(f"error: {str(http_error)}")
    except Exception as e:
        raise Exception(f"error: {str(e)}")

def jira_get_comments(params,cred):
    """
    Retrieve comments for a Jira issue.

    :param dict params:
        - issue (str): Key or ID of the Jira issue to retrieve comments for. (required)
        - expand (str): Additional information to include in the response. (optional)

    :param str email: User email for Jira authentication. (required)
    :param str api_token: Jira API token for authentication. (required)
    :param str server: Jira server URL. (required)

    :return: List of comments for the specified Jira issue.
    :rtype: list
    """
    try:
        creds=json.loads(cred)
        if 'email' in creds and 'apiToken' in creds and 'domain' in creds and 'issue' in params:
            jira = authenticate(creds)
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            get_comments = jira.comments(**data)
            comments_list = [comment.raw for comment in get_comments]
            return comments_list
        else:
            raise Exception('error: Missing input data')
    except JIRAError as http_error:
        raise JIRAError(f"error: {str(http_error)}")
    except Exception as e:
        raise Exception(f"error: {str(e)}")

def jira_get_comment(params,cred):
    """
    Retrieve a specific comment for a Jira issue.

    :param dict params:
        - issue (str): Key or ID of the Jira issue containing the comment. (required)
        - comment (str): ID of the comment to retrieve. (required)
        - expand (str): Additional information to include in the response. (optional)

    :param str email: User email for Jira authentication. (required)
    :param str api_token: Jira API token for authentication. (required)
    :param str server: Jira server URL. (required)

    :return: Information about the specified Jira comment.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'email' in creds and 'apiToken' in creds and 'domain' in creds and 'issue' in params and 'comment' in params:
            jira = authenticate(creds)
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            get_comment = jira.comment(**data)
            return get_comment.raw
        else:
            raise Exception('error: Missing input data')
    except JIRAError as http_error:
        raise JIRAError(f"error: {str(http_error)}")
    except Exception as e:
        raise Exception(f"error: {str(e)}")
    
def jira_delete_comment(params,cred):
    """
    Delete a specific comment for a Jira issue.

    :param dict params:
        - issue (str): Key or ID of the Jira issue containing the comment. (required)
        - comment (str): ID of the comment to delete. (required)

    :param str email: User email for Jira authentication. (required)
    :param str api_token: Jira API token for authentication. (required)
    :param str server: Jira server URL. (required)

    :return: Success message indicating the comment was deleted.
    :rtype: str
    """
    try:
        creds=json.loads(cred)
        if 'email' in creds and 'apiToken' in creds and 'domain' in creds and 'issue' in params and 'comment' in params:
            jira = authenticate(creds)
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            get_comment = jira.comment(**data)
            get_comment.delete()
            return f"Comment : Deleted successfully."
        else:
            raise Exception('error: Missing input data')
    except JIRAError as http_error:
        raise JIRAError(f"error: {str(http_error)}")
    except Exception as e:
        raise Exception(f"error: {str(e)}")
    
def jira_update_comment(params,cred):
    """
    Update a specific comment for a Jira issue.

    :param dict params:
        - issue (str): Key or ID of the Jira issue containing the comment. (required)
        - comment (str): ID of the comment to update. (required)
        - body (str): New body text for the comment. (required)

    :param str email: User email for Jira authentication. (required)
    :param str api_token: Jira API token for authentication. (required)
    :param str server: Jira server URL. (required)

    :return: Success message indicating the comment was updated.
    :rtype: str
    """
    try:
        creds=json.loads(cred)
        if 'email' in creds and 'apiToken' in creds and 'domain' in creds and 'issue' in params and 'body' in params and 'comment' in params:
            jira = authenticate(creds)
            data = {}
            for key, value in params.items():
                if key=='issue' or key=='comment':
                    data[key] = value
            get_comment = jira.comment(**data)
            update_data={}
            for key, value in params.items():
                if key=='issue' or key=='comment':
                    continue
                else:
                    update_data[key] = value
            get_comment.update(**update_data)
            return f"Comment : Updated successfully."
        else:
            raise Exception('error: Missing input data')
    except JIRAError as http_error:
        raise JIRAError(f"error: {str(http_error)}")
    except Exception as e:
        raise Exception(f"error: {str(e)}")
    

def jira_create_attachment(params,cred):
    """
    Create an attachment for a specific Jira issue.

    :param dict params:
        - issue (str): Key or ID of the Jira issue for which to create the attachment. (required)
        - filename (str): Name of the attachment file. (required)
        - attachment (bytes): Binary content of the attachment. (required, if 'url' is not provided)
        - url (str): URL of the file to attach. (required, if 'attachment' is not provided)

    :param str email: User email for Jira authentication. (required)
    :param str api_token: Jira API token for authentication. (required)
    :param str server: Jira server URL. (required)

    :return: Success message indicating the attachment was created successfully.
    :rtype: str
    """
    try:
        creds=json.loads(cred)
        if 'email' in creds and 'apiToken' in creds and 'domain' in creds and 'issue' in params and ('attachment' in params or 'url' in params) and 'filename' in params:
            jira = authenticate(creds)
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            if 'attachment' in data:
                attachment_data = {
                    'issue': data['issue'],
                    'filename': data['filename'],
                    'attachment': io.BytesIO(params['attachment']),
                }
                jira.add_attachment(**attachment_data)
                return "Attachment added successfully"
            elif 'url' in data:
                response = requests.get(data['url'])
                if response.status_code == 200:
                    file_content = response.content
                    attachment_data = {
                        'issue': data['issue'],
                        'filename': data['filename'],
                        'attachment': io.BytesIO(file_content),
                    }
                    jira.add_attachment(**attachment_data)
                return "Attachment added successfully"
        else:
            raise Exception('error: Missing input data')
    except JIRAError as http_error:
        raise JIRAError(f"error: {str(http_error)}")
    except Exception as e:
        raise Exception(f"error: {str(e)}")

def jira_get_attachments(params,cred):
    """
    Retrieve information about attachments for a specific Jira issue.

    :param dict params:
        - id (str): Key or ID of the Jira issue for which to retrieve attachments. (required)

    :param str email: User email for Jira authentication. (required)
    :param str api_token: Jira API token for authentication. (required)
    :param str server: Jira server URL. (required)

    :return: List of dictionaries containing information about attachments for the specified Jira issue.
    :rtype: list[dict]
    """
    try:
        creds=json.loads(cred)
        if 'email' in creds and 'apiToken' in creds and 'domain' in creds and 'id' in params:
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            jira = authenticate(creds)
            issue = jira.issue(data['id'])
            attachments = issue.fields.attachment 
            attachment_info = []
            for attachment in attachments:
                attachment_dict = attachment.raw
                attachment_info.append(attachment_dict)
            return attachment_info
        else:
            raise Exception('error: Missing input data')
    except JIRAError as http_error:
        raise JIRAError(f"error: {str(http_error)}")
    except Exception as e:
        raise Exception(f"error: {str(e)}")

def jira_get_attachment(params,cred):
    """
    Retrieve information about a specific attachment in Jira.

    :param dict params:
        - id (str): ID of the attachment to retrieve. (required)

    :param str email: User email for Jira authentication. (required)
    :param str api_token: Jira API token for authentication. (required)
    :param str server: Jira server URL. (required)

    :return: Dictionary containing information about the specified Jira attachment.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'email' in creds and 'apiToken' in creds and 'domain' in creds and 'id' in params:
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            jira = authenticate(creds)
            attachment = jira.attachment(data['id'])
            attachment_dict = attachment.raw
            return attachment_dict
        else:
            raise Exception('error: Missing input data')
    except JIRAError as http_error:
        raise JIRAError(f"error: {str(http_error)}")
    except Exception as e:
        raise Exception(f"error: {str(e)}")
    
def jira_delete_attachment(params,cred):
    """
    Delete a specific attachment in Jira.

    :param dict params:
        - id (str): ID of the attachment to delete. (required)

    :param str email: User email for Jira authentication. (required)
    :param str api_token: Jira API token for authentication. (required)
    :param str server: Jira server URL. (required)

    :return: Success message indicating the attachment was deleted.
    :rtype: str
    """
    try:
        creds=json.loads(cred)
        if 'email' in creds and 'apiToken' in creds and 'domain' in creds and 'id' in params:
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            jira = authenticate(creds)
            attachment = jira.delete_attachment(data['id'])
            if attachment:
                return "Attachment deleted successfully"
            else:
                raise Exception('Failed to delete')
        else:
            raise Exception('error: Missing input data')
    except JIRAError as http_error:
        raise JIRAError(f"error: {str(http_error)}")
    except Exception as e:
        raise Exception(f"error: {str(e)}")

def jira_create_user(params,cred):
    """
    Create a new user in Jira.

    :param dict params:
        - username (str): Username for the new user. (required)
        - email (str): Email address for the new user. (required)

    :param str email: User email for Jira authentication. (required)
    :param str api_token: Jira API token for authentication. (required)
    :param str server: Jira server URL. (required)

    :return: Success message indicating the user was created.
    :rtype: str
    """
    try:
        creds=json.loads(cred)
        if 'email' in creds and 'apiToken' in creds and 'domain' in creds and 'username' in params and 'email' in params:
            jira = authenticate(creds)
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            new_user = jira.add_user(**data)
            return "Success"
        else:
            raise Exception('error: Missing input data')
    except JIRAError as http_error:
        raise JIRAError(f"error: {str(http_error)}")
    except Exception as e:
        raise Exception(f"error: {str(e)}")
    
def jira_get_users(params,cred):
    """
    Get a list of users from Jira based on the specified query.

    :param dict params:
        - query (str): Query string to search for users. (required)

    :param str email: User email for Jira authentication. (required)
    :param str api_token: Jira API token for authentication. (required)
    :param str server: Jira server URL. (required)

    :return: List of users matching the specified query.
    :rtype: list
    """
    try:
        creds=json.loads(cred)
        if 'email' in creds and 'apiToken' in creds and 'domain' in creds and 'query' in params:
            jira = authenticate(creds)
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            get_users = jira.search_users(**data)
            users_list = [user.raw for user in get_users]
            return users_list
        else:
            raise Exception('error: Missing input data')
    except JIRAError as http_error:
        raise JIRAError(f"error: {str(http_error)}")
    except Exception as e:
        raise Exception(f"error: {str(e)}")
    
def jira_get_user(params,cred):
    """
    Get information about a user from Jira based on the specified user ID.

    :param dict params:
        - id (str): User ID for fetching user information. (required)
        - expand (str): Additional information to include in the response. (optional)

    :param str email: User email for Jira authentication. (required)
    :param str api_token: Jira API token for authentication. (required)
    :param str server: Jira server URL. (required)

    :return: Information about the specified user.
    :rtype: dict
    """
    try:
        creds=json.loads(cred)
        if 'email' in creds and 'apiToken' in creds and 'domain' in creds and 'id' in params:
            jira = authenticate(creds)
            data = {}
            for key, value in params.items():
                if value:
                    data[key] = value
            get_users = jira.user(**data)
            return get_users.raw
        else:
            raise Exception('error: Missing input data')
    except JIRAError as http_error:
        raise JIRAError(f"error: {str(http_error)}")
    except Exception as e:
        raise Exception(f"error: {str(e)}")
    