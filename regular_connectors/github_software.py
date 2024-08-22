from github import Github
import json


def login_token(access_token):
    github_service = Github(access_token)
    return github_service


def handle_auth(credentials):
    if "accessToken" in credentials:
        github_service = login_token(access_token=credentials["accessToken"])
    else:
        raise Exception("Invalid Credentials")
    return github_service


def convertdateToString(date):
    if type(date) == str:
        return date
    date_format = "%Y-%m-%dT%H:%M"
    date_string = date.strftime(date_format)
    return date_string


def jsonify_repo(repo):
    return {
        "id": repo.id,
        "name": repo.name,
        "full_name": repo.full_name,
        "owner": repo.owner.login,
        "description": repo.description,
        "private": repo.private,
        "size": repo.size,
        "url": repo.url,
        "html_url": repo.html_url,
        "created_at": convertdateToString(repo.created_at),
        "updated_at": convertdateToString(repo.updated_at),
        "pushed_at": convertdateToString(repo.pushed_at),
    }


def jsonify_isssue(issue):
    return {
        "id": issue.id,
        "title": issue.title,
        "body": issue.body,
        "locked": issue.locked,
        "url": issue.url,
        "html_url": issue.html_url,
        "created_at": convertdateToString(issue.created_at),
        "updated_at": convertdateToString(issue.updated_at),
        "number": issue.number,
    }


def jsonify_release(release):
    return {
        "id": release.id,
        "tag_name": release.tag_name,
        "name": release.title,
        "body": release.body,
        "url": release.url,
        "html_url": release.html_url,
        "created_at": convertdateToString(release.created_at),
    }


def jsonify_file(file):
    return {
        "name": file.name,
        "path": file.path,
        "sha": file.sha,
        "url": file.url,
        "html_url": file.html_url,
        "type": file.type,
        "content": file.content,
        "encoding": file.encoding,
        "size": file.size,
        "decoded_content": file.decoded_content.decode("utf-8"),
    }



def github_get_user_repos(creds, params):
    """
    Get a list of repositories for a GitHub user.

    :param credentials: Dictionary containing GitHub authentication credentials.
    :type credentials: dict
    :param params: Dictionary containing parameters.
    
        - :username: (str, required) - The GitHub username for which to retrieve repositories.

    :return: A list of repositories for the specified GitHub user.
    :rtype: list
    :raises Exception: If there is an issue with the GitHub API or missing input data.
    """
    try:
        credentials=json.loads(creds)
        github_service = handle_auth(credentials)
        if (
            "username" in params
            and params["username"] is not None
            and params["username"] != ""
        ):
            user = github_service.get_user(params["username"])
            repos = user.get_repos()
            return [jsonify_repo(repo) for repo in repos]
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def github_get_repo_license(creds,params):
    """
    Get the license information for a GitHub repository.

    :param credentials: Dictionary containing GitHub authentication credentials.
    :type credentials: dict
    :param params: Dictionary containing parameters.

        - :owner: (str, required) - The owner of the GitHub repository.
        - :repo_name: (str, required) - The name of the GitHub repository.

    :return: License information for the specified GitHub repository.
    :rtype: dict
    :raises Exception: If there is an issue with the GitHub API or missing input data.
    """
    try:
        credentials=json.loads(creds)
        github_service = handle_auth(credentials)
        if (
            "owner" in params
            and params["owner"] is not None
            and params["owner"] != ""
            and "repo_name" in params
            and params["repo_name"] is not None
            and params["repo_name"] != ""
        ):
            owner = github_service.get_user(params["owner"])
            repo = owner.get_repo(params["repo_name"])
            contents = repo.get_contents("LICENSE")
            return contents._rawData
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def github_get_repo_issues(creds, params):
    """
    Get a list of issues for a GitHub repository.

    :param credentials: Dictionary containing GitHub authentication credentials.
    :type credentials: dict
    :param params: Dictionary containing parameters.

        - :owner: (str, required) - The owner of the GitHub repository.
        - :repo_name: (str, required) - The name of the GitHub repository.

    :return: A list of issues for the specified GitHub repository.
    :rtype: list
    :raises Exception: If there is an issue with the GitHub API or missing input data.
    """
    try:
        credentials=json.loads(creds)
        github_service = handle_auth(credentials)
        if (
            "owner" in params
            and params["owner"] is not None
            and params["owner"] != ""
            and "repo_name" in params
            and params["repo_name"] is not None
            and params["repo_name"] != ""
        ):
            owner = github_service.get_user(params["owner"])
            repo = owner.get_repo(params["repo_name"])
            issues = repo.get_issues()
            return [jsonify_isssue(issue=issue) for issue in issues]
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def github_get_repo(creds, params):
    """
    Get information about a GitHub repository.

    :param credentials: Dictionary containing GitHub authentication credentials.
    :type credentials: dict
    :param params: Dictionary containing parameters.

        - :owner: (str, required) - The owner of the GitHub repository.
        - :repo_name: (str, required) - The name of the GitHub repository.

    :return: Information about the specified GitHub repository.
    :rtype: dict
    :raises Exception: If there is an issue with the GitHub API or missing input data.
    """
    try:
        credentials=json.loads(creds)
        github_service = handle_auth(credentials)
        if (
            "owner" in params
            and params["owner"] is not None
            and params["owner"] != ""
            and "repo_name" in params
            and params["repo_name"] is not None
            and params["repo_name"] != ""
        ):
            owner = github_service.get_user(params["owner"])
            repo = owner.get_repo(params["repo_name"])
            return jsonify_repo(repo)
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def github_create_repo_release(creds, params):
    """
    Create a release for a GitHub repository.

    :param credentials: Dictionary containing GitHub authentication credentials.
    :type credentials: dict
    :param params: Dictionary containing parameters.

        - :owner: (str, required) - The owner of the GitHub repository.
        - :repo_name: (str, required) - The name of the GitHub repository.
        - :tag_name: (str, required) - The name of the tag for the release.
        - :additionals: (dict, optional) - Additional parameters for creating the release.

    :return: Information about the created release.
    :rtype: dict
    :raises Exception: If there is an issue with the GitHub API or missing input data.
    """
    try:
        credentials=json.loads(creds)
        github_service = handle_auth(credentials)
        if (
            "owner" in params
            and params["owner"] is not None
            and params["owner"] != ""
            and "repo_name" in params
            and params["repo_name"] is not None
            and params["repo_name"] != ""
            and "tag_name" in params
            and params["tag_name"] is not None
            and params["tag_name"] != ""
        ):
            owner = github_service.get_user(params["owner"])
            repo = owner.get_repo(params["repo_name"])
            args = {}
            if (
                "additionals" in params
                and params["additionals"] is not None
                and params["additionals"] != {}
            ):
                args = params["additionals"]
            release = repo.create_git_release(tag=params["tag_name"], **args)
            return jsonify_release(release)
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def github_get_repo_releases(creds, params):
    """
    Get a list of releases for a GitHub repository.

    :param credentials: Dictionary containing GitHub authentication credentials.
    :type credentials: dict
    :param params: Dictionary containing parameters.

        - :owner: (str, required) - The owner of the GitHub repository.
        - :repo_name: (str, required) - The name of the GitHub repository.

    :return: A list of releases for the specified GitHub repository.
    :rtype: list
    :raises Exception: If there is an issue with the GitHub API or missing input data.
    """
    try:
        credentials=json.loads(creds)
        github_service = handle_auth(credentials)
        if (
            "owner" in params
            and params["owner"] is not None
            and params["owner"] != ""
            and "repo_name" in params
            and params["repo_name"] is not None
            and params["repo_name"] != ""
        ):
            owner = github_service.get_user(params["owner"])
            repo = owner.get_repo(params["repo_name"])
            releases = repo.get_releases()
            return [jsonify_release(release=release) for release in releases]
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def github_get_release(creds, params):
    """
    Get information about a GitHub release.

    :param credentials: Dictionary containing GitHub authentication credentials.
    :type credentials: dict
    :param params: Dictionary containing parameters.

        - :owner: (str, required) - The owner of the GitHub repository.
        - :repo_name: (str, required) - The name of the GitHub repository.
        - :tag_name: (str, required) - The name of the tag for the release.

    :return: Information about the specified GitHub release.
    :rtype: dict
    :raises Exception: If there is an issue with the GitHub API or missing input data.
    """
    try:
        credentials=json.loads(creds)
        github_service = handle_auth(credentials)
        if (
            "owner" in params
            and params["owner"] is not None
            and params["owner"] != ""
            and "repo_name" in params
            and params["repo_name"] is not None
            and params["repo_name"] != ""
            and "tag_name" in params
            and params["tag_name"] is not None
            and params["tag_name"] != ""
        ):
            owner = github_service.get_user(params["owner"])
            repo = owner.get_repo(params["repo_name"])
            release = repo.get_release(params["tag_name"])
            return jsonify_release(release)
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def github_update_release(creds, params):
    """
    Update information about a GitHub release.

    :param credentials: Dictionary containing GitHub authentication credentials.
    :type credentials: dict
    :param params: Dictionary containing parameters.

        - :owner: (str, required) - The owner of the GitHub repository.
        - :repo_name: (str, required) - The name of the GitHub repository.
        - :tag_name: (str, required) - The name of the tag for the release.
        - :additionals: (dict, optional) - Additional parameters for updating the release.

    :return: Updated information about the GitHub release.
    :rtype: dict
    :raises Exception: If there is an issue with the GitHub API or missing input data.
    """
    try:
        credentials=json.loads(creds)
        github_service = handle_auth(credentials)
        if (
            "owner" in params
            and params["owner"] is not None
            and params["owner"] != ""
            and "repo_name" in params
            and params["repo_name"] is not None
            and params["repo_name"] != ""
            and "tag_name" in params
            and params["tag_name"] is not None
            and params["tag_name"] != ""
        ):
            owner = github_service.get_user(params["owner"])
            repo = owner.get_repo(params["repo_name"])
            release = repo.get_release(params["tag_name"])
            args = {}
            if (
                "additionals" in params
                and params["additionals"] is not None
                and params["additionals"] != {}
            ):
                args = params["additionals"]
            release = release.update_release(**args)
            return jsonify_release(release)
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def gihtub_delete_release(creds, params):
    """
    Delete a GitHub release.

    :param credentials: Dictionary containing GitHub authentication credentials.
    :type credentials: dict
    :param params: Dictionary containing parameters.

        - :owner: (str, required) - The owner of the GitHub repository.
        - :repo_name: (str, required) - The name of the GitHub repository.
        - :tag_name: (str, required) - The name of the tag for the release.

    :return: A message indicating successful deletion of the GitHub release.
    :rtype: str
    :raises Exception: If there is an issue with the GitHub API or missing input data.
    """
    try:
        credentials=json.loads(creds)
        github_service = handle_auth(credentials)
        if (
            "owner" in params
            and params["owner"] is not None
            and params["owner"] != ""
            and "repo_name" in params
            and params["repo_name"] is not None
            and params["repo_name"] != ""
            and "tag_name" in params
            and params["tag_name"] is not None
            and params["tag_name"] != ""
        ):
            owner = github_service.get_user(params["owner"])
            repo = owner.get_repo(params["repo_name"])
            release = repo.get_release(params["tag_name"])
            release.delete_release()
            return "Release deleted successfully"
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def github_get_organization_repos(creds, params):
    """
    Get a list of repositories for a GitHub organization.

    :param credentials: Dictionary containing GitHub authentication credentials.
    :type credentials: dict
    :param params: Dictionary containing parameters.

        - :organization: (str, required) - The name of the GitHub organization.

    :return: A list of repositories for the specified GitHub organization.
    :rtype: list
    :raises Exception: If there is an issue with the GitHub API or missing input data.
    """
    try:
        credentials=json.loads(creds)
        github_service = handle_auth(credentials)
        if (
            "organization" in params
            and params["organization"] is not None
            and params["organization"] != ""
        ):
            organization = github_service.get_organization(params["organization"])
            repos = organization.get_repos()
            return [jsonify_repo(repo) for repo in repos]
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def github_create_issue(creds, params):
    """
    Create a GitHub issue for a repository.

    :param credentials: Dictionary containing GitHub authentication credentials.
    :type credentials: dict
    :param params: Dictionary containing parameters.

        - :owner: (str, required) - The owner of the GitHub repository.
        - :repo_name: (str, required) - The name of the GitHub repository.
        - :title: (str, required) - The title of the GitHub issue.
        - :additionals: (dict, optional) - Additional parameters for creating the issue.

    :return: Information about the created GitHub issue.
    :rtype: dict
    :raises Exception: If there is an issue with the GitHub API or missing input data.
    """
    try:
        credentials=json.loads(creds)
        github_service = handle_auth(credentials)
        if (
            "owner" in params
            and params["owner"] is not None
            and params["owner"] != ""
            and "repo_name" in params
            and params["repo_name"] is not None
            and params["repo_name"] != ""
            and "title" in params
            and params["title"] is not None
            and params["title"] != ""
        ):
            owner = github_service.get_user(params["owner"])
            repo = owner.get_repo(params["repo_name"])
            title = params["title"]
            args = {}
            if (
                "additionals" in params
                and params["additionals"] is not None
                and params["additionals"] != {}
            ):
                args = params["additionals"]
            issue = repo.create_issue(title=title, **args)
            return jsonify_isssue(issue)
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def github_get_issue(creds, params):
    """
    Get information about a GitHub issue.

    :param credentials: Dictionary containing GitHub authentication credentials.
    :type credentials: dict
    :param params: Dictionary containing parameters.

        - :owner: (str, required) - The owner of the GitHub repository.
        - :repo_name: (str, required) - The name of the GitHub repository.
        - :issue_number: (str, required) - The number of the GitHub issue.

    :return: Information about the specified GitHub issue.
    :rtype: dict
    :raises Exception: If there is an issue with the GitHub API or missing input data.
    """
    try:
        credentials=json.loads(creds)
        github_service = handle_auth(credentials)
        if (
            "owner" in params
            and params["owner"] is not None
            and params["owner"] != ""
            and "repo_name" in params
            and params["repo_name"] is not None
            and params["repo_name"] != ""
            and "issue_number" in params
            and params["issue_number"] is not None
            and params["issue_number"] != ""
        ):
            owner = github_service.get_user(params["owner"])
            repo = owner.get_repo(params["repo_name"])
            issue = repo.get_issue(params["issue_number"])
            return jsonify_isssue(issue)
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def github_create_issue_comment(creds, params):
    """
    Create a comment for a GitHub issue.

    :param credentials: Dictionary containing GitHub authentication credentials.
    :type credentials: dict
    :param params: Dictionary containing parameters.

        - :owner: (str, required) - The owner of the GitHub repository.
        - :repo_name: (str, required) - The name of the GitHub repository.
        - :issue_number: (str, required) - The number of the GitHub issue.
        - :body: (str, required) - The body of the comment.

    :return: Information about the GitHub issue after creating the comment.
    :rtype: dict
    :raises Exception: If there is an issue with the GitHub API or missing input data.
    """
    try:
        credentials=json.loads(creds)
        github_service = handle_auth(credentials)
        if (
            "owner" in params
            and params["owner"] is not None
            and params["owner"] != ""
            and "repo_name" in params
            and params["repo_name"] is not None
            and params["repo_name"] != ""
            and "issue_number" in params
            and params["issue_number"] is not None
            and params["issue_number"] != ""
            and "body" in params
            and params["body"] is not None
            and params["body"] != ""
        ):
            owner = github_service.get_user(params["owner"])
            repo = owner.get_repo(params["repo_name"])
            issue = repo.get_issue(params["issue_number"])
            comment = issue.create_comment(params["body"])
            return jsonify_isssue(issue)
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def github_edit_issue(creds, params):
    """
    Edit details of a GitHub issue.

    :param credentials: Dictionary containing GitHub authentication credentials.
    :type credentials: dict
    :param params: Dictionary containing parameters.

        - :owner: (str, required) - The owner of the GitHub repository.
        - :repo_name: (str, required) - The name of the GitHub repository.
        - :issue_number: (str, required) - The number of the GitHub issue.
        - :additionals: (dict, optional) - Additional parameters for editing the issue.

    :return: Information about the GitHub issue after editing.
    :rtype: dict
    :raises Exception: If there is an issue with the GitHub API or missing input data.
    """
    try:
        credentials=json.loads(creds)
        github_service = handle_auth(credentials)
        if (
            "owner" in params
            and params["owner"] is not None
            and params["owner"] != ""
            and "repo_name" in params
            and params["repo_name"] is not None
            and params["repo_name"] != ""
            and "issue_number" in params
            and params["issue_number"] is not None
            and params["issue_number"] != ""
        ):
            owner = github_service.get_user(params["owner"])
            repo = owner.get_repo(params["repo_name"])
            issue = repo.get_issue(params["issue_number"])
            args = {}
            if (
                "additionals" in params
                and params["additionals"] is not None
                and params["additionals"] != {}
            ):
                args = params["additionals"]
            issue.edit(**args)
            return jsonify_isssue(issue)
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def github_list_file(creds, params):
    """
    List the content of a file in a GitHub repository.

    :param credentials: Dictionary containing GitHub authentication credentials.
    :type credentials: dict
    :param params: Dictionary containing parameters.

        - :path: (str, required) - The path to the file.
        - :owner: (str, required) - The owner of the GitHub repository.
        - :repo_name: (str, required) - The name of the GitHub repository.

    :return: Information about the specified file in the GitHub repository.
    :rtype: dict
    :raises Exception: If there is an issue with the GitHub API or missing input data.
    """
    try:
        credentials=json.loads(creds)
        github_service = handle_auth(credentials)
        if (
            "path" in params
            and params["path"] is not None
            and params["path"] != ""
            and "owner" in params
            and params["owner"] is not None
            and params["owner"] != ""
            and "repo_name" in params
            and params["repo_name"] is not None
            and params["repo_name"] != ""
        ):
            owner = github_service.get_user(params["owner"])
            repo = owner.get_repo(params["repo_name"])
            content = repo.get_contents(params["path"])
            return jsonify_file(content)
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def github_create_file(creds, params):
    """
    Create a new file in a GitHub repository.

    :param credentials: Dictionary containing GitHub authentication credentials.
    :type credentials: dict
    :param params: Dictionary containing parameters.

        - :path: (str, required) - The path to the file.
        - :owner: (str, required) - The owner of the GitHub repository.
        - :repo_name: (str, required) - The name of the GitHub repository.
        - :message: (str, required) - A commit message for creating the file.
        - :content: (str, required) - The content of the file.

    :return: Information about the created file in the GitHub repository.
    :rtype: dict
    :raises Exception: If there is an issue with the GitHub API or missing input data.
    """
    try:
        credentials=json.loads(creds)
        github_service = handle_auth(credentials)
        if (
            "path" in params
            and params["path"] is not None
            and params["path"] != ""
            and "owner" in params
            and params["owner"] is not None
            and params["owner"] != ""
            and "repo_name" in params
            and params["repo_name"] is not None
            and params["repo_name"] != ""
            and "message" in params
            and params["message"] is not None
            and params["message"] != ""
            and "content" in params
            and params["content"] is not None
            and params["content"] != ""
        ):
            owner = github_service.get_user(params["owner"])
            repo = owner.get_repo(params["repo_name"])
            content = repo.create_file(
                params["path"], params["message"], params["content"]
            )
            return jsonify_file(content["content"])
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def github_delete_file(creds, params):
    """
    Delete a file from a GitHub repository.

    :param credentials: Dictionary containing GitHub authentication credentials.
    :type credentials: dict
    :param params: Dictionary containing parameters.

        - :path: (str, required) - The path to the file.
        - :owner: (str, required) - The owner of the GitHub repository.
        - :repo_name: (str, required) - The name of the GitHub repository.
        - :message: (str, required) - A commit message for deleting the file.

    :return: A message indicating successful deletion of the file.
    :rtype: str
    :raises Exception: If there is an issue with the GitHub API or missing input data.
    """
    try:
        credentials=json.loads(creds)
        github_service = handle_auth(credentials)
        if (
            "path" in params
            and params["path"] is not None
            and params["path"] != ""
            and "owner" in params
            and params["owner"] is not None
            and params["owner"] != ""
            and "repo_name" in params
            and params["repo_name"] is not None
            and params["repo_name"] != ""
            and "message" in params
            and params["message"] is not None
            and params["message"] != ""
        ):
            owner = github_service.get_user(params["owner"])
            repo = owner.get_repo(params["repo_name"])
            content = repo.get_contents(params["path"])
            repo.delete_file(params["path"], params["message"], content.sha)
            return "File deleted successfully"
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)


def github_edit_file(creds, params):
    """
    Edit an existing file in a GitHub repository.

    :param credentials: Dictionary containing GitHub authentication credentials.
    :type credentials: dict
    :param params: Dictionary containing parameters.

        - :path: (str, required) - The path to the file.
        - :owner: (str, required) - The owner of the GitHub repository.
        - :repo_name: (str, required) - The name of the GitHub repository.
        - :message: (str, required) - A commit message for editing the file.
        - :content: (str, required) - The new content of the file.

    :return: A message indicating successful update of the file.
    :rtype: str
    :raises Exception: If there is an issue with the GitHub API or missing input data.
    """
    try:
        credentials=json.loads(creds)
        github_service = handle_auth(credentials)
        if (
            "path" in params
            and params["path"] is not None
            and params["path"] != ""
            and "owner" in params
            and params["owner"] is not None
            and params["owner"] != ""
            and "repo_name" in params
            and params["repo_name"] is not None
            and params["repo_name"] != ""
            and "message" in params
            and params["message"] is not None
            and params["message"] != ""
            and "content" in params
            and params["content"] is not None
            and params["content"] != ""
        ):
            owner = github_service.get_user(params["owner"])
            repo = owner.get_repo(params["repo_name"])
            content = repo.get_contents(params["path"])
            repo.update_file(
                params["path"], params["message"], params["content"], content.sha
            )
            return "File updated successfully"
        else:
            raise Exception("Missing input data")
    except Exception as e:
        raise Exception(e)
