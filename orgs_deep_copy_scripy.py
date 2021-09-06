import requests
import json
import argparse

HTTP_COOKIE = None


def login(username, password):

    """
    Login to the Rossum's API
    :param username: Rossum username
    :param password: Password of the user
    :return:
    """

    payload = {
        "username": username,
        "password": password
        }

    response = requests.post("https://api.elis.rossum.ai/v1/auth/login", data=payload)

    if response.status_code == 200:
        print("Logging in - OK")
    else:
        print("Logging in - ERROR")

    return response.json()["key"]


def login_to_specific_organization(organization_url, token):

    """
    Users in Rossum can belong to multiple organizations. User is a member of a primary organization when created.
    Secondary organizations can be assigned afterwards. Authentication token is issued for each organization separately.
    :param organization_url: Organization where to log in
    :param token: Token from the primary organization.
    :return: dict
    """

    payload = {
        "organization": organization_url
    }

    headers = {"Authorization": "token {0}".format(token)}
    response = requests.post("https://api.elis.rossum.ai/v1/auth/membership_token", headers=headers, data=payload)

    if response.status_code == 200:
        print("Logging in to secondary organization - OK")
    else:
        print("Logging in to secondary organization - ERROR")

    return response.json()["key"]


def assign_membership(user_url, organization_url, token):

    """
    User can be assigned to non-primary organization. Memberships can be created only by organization group admin user.
    Such a user role can be assigned only by Rossum's support team.
    :param user_url: The user of the user to be assigned.
    :param organization_url: The organization where the user should be assigned
    :param token: Auth token from the primary organization.
    :return: dict
    """

    payload = {
        "user": user_url,
        "organization": organization_url
    }

    headers = {"Authorization": "token {0}".format(token)}
    response = requests.post("https://api.elis.rossum.ai/v1/memberships", headers=headers, data=payload)

    return response


def get_all_organizations(token):

    """
    Getting all organizations in organization group - organization group admin can list all the available organizations.
    :param token: Authentication token to the primary organization.
    :return: List of results
    """

    # TODO perform pagination for big orgs

    page_size = 100

    headers = {"Authorization": "token {0}".format(token)}
    response = requests.get("https://api.elis.rossum.ai/v1/organizations?page_size={0}".format(page_size),
                            headers=headers)

    if response.status_code == 200:
        print("Fetching organizations - OK")
    else:
        print("Fetching organizations - ERROR")

    return response.json()["results"]


def get_master_data_organization(organizations_list):

    """
    We will be performing a deep-copy of one template organization.
    We have marked up this organization with ID "master_data_organization" in the organization metadata
    :param organizations_list: List of organizations
    :return: dict representing the selected organization
    """

    for org in organizations_list:

        if "metadata" in org:
            print(org["metadata"])

        if "metadata" in org and "id" in org["metadata"] and org["metadata"]["id"] == "master_data_organization":
            return org

    return None


def get_all_workspaces(organization_dict, token):

    """
    Getting all workspaces of a specific organization.
    :param organization_dict: Dict representing the selected organization.
    :param token: Auth token to the selected organization.
    :return: List of workspaces
    """

    headers = {"Authorization": "token {0}".format(token)}

    response = requests.get("https://api.elis.rossum.ai/v1/workspaces?organization={0}".format(organization_dict["id"]),
                            headers=headers)

    if response.status_code == 200:
        print("Fetched workspaces - OK")
    else:
        print("Fetched workspaces - ERROR")

    return response.json()["results"]


def get_all_queues(organization_dict, token):

    """
    Getting all queues of a specific organization.
    :param organization_dict: Dict representing the selected organization.
    :param token: Auth token to the selected organization.
    :return: List of queues
    """

    headers = {"Authorization": "token {0}".format(token)}
    response = requests.get("https://api.elis.rossum.ai/v1/queues?organization={0}".format(organization_dict["id"]),
                            headers=headers)

    if response.status_code == 200:
        print("Fetching queues - OK")
    else:
        print("Fetching queues - ERROR")

    return response.json()["results"]


def get_schema(schema, token):

    """
    Getting schema.
    :param schema: The url of the schema.
    :param token: Authentication token.
    :return:
    """

    headers = {"Authorization": "token {0}".format(token)}
    response = requests.get(schema, headers=headers)

    if response.status_code == 200:
        print("Fetching schema - OK")
    else:
        print("Fetching schema - ERROR")

    return response.json()


def get_document(document_url, token):

    """
    Get a specific document.
    :param document_url: Url of the document
    :param token: Authentication token
    :return:
    """

    headers = {"Authorization": "token {0}".format(token)}
    response = requests.get(document_url, headers=headers)

    if response.status_code == 200:
        print("Fetching document - OK")
    else:
        print("Fetching document - ERROR")

    return response.json()


def get_original_document(document, token):

    """
    Download original of the document from Rossum's API.
    :param document: Dict representing the document/
    :param token: Authentication token
    :return: The content of the original document
    """

    headers = {"Authorization": "token {0}".format(token)}
    response = requests.get("https://api.elis.rossum.ai/v1/original/{0}".format(document["s3_name"]), headers=headers)

    if response.status_code == 200:
        print("Getting original document - OK")
    else:
        print("Getting original document - ERROR")

    return response


def get_all_extensions(organization_dict, token):

    """
    Get all extensions from a specific organization.
    :param organization_dict: Dict representing the organization
    :param token: Authentication token
    :return: List of extensions
    """

    headers = {"Authorization": "token {0}".format(token)}
    response = requests.get("https://api.elis.rossum.ai/v1/hooks?organization={0}".format(organization_dict["id"]),
                            headers=headers)

    if response.status_code == 200:
        print("Fetching extensions - OK")
    else:
        print("Fetching extensions - ERROR")

    return response.json()["results"]


def get_all_annotations(organization_dict, token):

    """
    Get all annotations from a specific organization
    :param organization_dict: Dict representing the organization
    :param token: Authentication token
    :return: List of annotations
    """

    headers = {"Authorization": "token {0}".format(token)}
    response = requests.get("https://api.elis.rossum.ai/v1/annotations?organization={0}".format(organization_dict["id"]),
                            headers=headers)

    if response.status_code == 200:
        print("Fetching annotations - OK")
    else:
        print("Fetching annotations - ERROR")

    return response.json()["results"]


def create_schema(schema, token):

    """
    Create schema from template in selected organization defined by the authentication token.
    :param schema: Dict representing the original schema
    :param token: Auth token from the organization where the object should be created.
    :return:
    """

    headers = {"Authorization": "token {0}".format(token)}

    payload = {"name": schema["name"],
               "content": schema["content"]
               }

    response = requests.post("https://api.elis.rossum.ai/v1/schemas", json=payload, headers=headers)

    if response.status_code == 201:
        print("Creating new schema - OK")
    else:
        print("Creating new schema - ERROR")

    return response.json()


def create_organization(create_key, org_name, user_fullname, user_email, user_password):

    """
    Create a fresh new organization
    :param create_key: Create key of the given organization group provided by Rossum team
    :param org_name: Name of the new organization
    :param user_fullname: Full name of the admin to be created in the new organization
    :param user_email: Full email of the admin to be created in the new organization
    :param user_password: Password of the new admin
    :return: Dict representing the new organization
    """

    payload = {
        "template_name": "Empty Organization Template",
        "organization_name": org_name,
        "user_fullname": user_fullname,
        "user_email": user_email,
        "user_password": user_password,
        "user_ui_settings": json.dumps({"locale": "en"}),
        "create_key": create_key
        }

    response = requests.post("https://api.elis.rossum.ai/v1/organizations/create", data=payload)

    if response.status_code == 201:
        print("Creating new organization - OK")
    else:
        print("Creating new organization - ERROR")

    return response.json()["organization"]


def create_workspaces(organization_url, token, workspaces_list):

    """
    Create new workspaces in the new organization
    :param organization_url: The new organization where workspaces will be created.
    :param token: Auth token to the new organization
    :param workspaces_list: List of original workspaces to be copied.
    :return: Mapping of the original workspaces from master organization to new workspaces URL in the new org.
    """

    headers = {"Authorization": "token {0}".format(token)}

    new_workspaces_mapping = {}

    for workspace in workspaces_list:

        payload = {"name": workspace["name"],
                   "organization": organization_url,
                   "metadata": json.dumps(workspace["metadata"])}

        response = requests.post("https://api.elis.rossum.ai/v1/workspaces", data=payload, headers=headers)

        if response.status_code == 201:
            print("Creating workspace '{0}' - OK".format(workspace["name"]))
        else:
            print("Creating workspace '{0}' - ERROR".format(workspace["name"]))

        new_workspaces_mapping[workspace["url"]] = response.json()["url"]

    return new_workspaces_mapping


def create_queues(new_workspaces_mapping, token, master_org_auth_token, queues_list):

    """
    :param new_workspaces_mapping: Mapping of the original workspaces from master organization
    to new workspaces in the new org.
    :param token: Auth token to the new organization
    :param master_org_auth_token: Auth token to the original organization where we copy objects from.
    :param queues_list: List of original queues to be copied.
    :return: Mapping of the original queues from master organization to new queues URL in the new org.
    """

    headers = {"Authorization": "token {0}".format(token)}

    new_queues_mapping = {}

    for queue in queues_list:

        schema = get_schema(queue["schema"], master_org_auth_token)

        new_schema = create_schema(schema, token)

        payload = {"name": queue["name"],
                   "workspace": new_workspaces_mapping[queue["workspace"]],
                   "metadata": queue["metadata"],
                   "schema": new_schema["url"]
                   }

        response = requests.post("https://api.elis.rossum.ai/v1/queues", json=payload, headers=headers)

        if response.status_code == 201:
            print("Creating queue '{0}' - OK".format(queue["name"]))
        else:
            print("Creating queue '{0}' - ERROR".format(queue["name"]))

        new_queues_mapping[queue["url"]] = response.json()["url"]

    return new_queues_mapping


def create_annotations(new_queues_mapping, original_annotations, token, master_org_auth_token):

    """

    :param new_queues_mapping: Mapping of the original queues from master organization to new queues URL in the new org.
    :param original_annotations: List of original annotation to be copied.
    :param token: Auth token to the new organization
    :param master_org_auth_token: Auth token to the original organization where we copy objects from.
    :return: None
    """

    for annotation in original_annotations:

        document = get_document(annotation["document"], master_org_auth_token)

        original_file = get_original_document(document, master_org_auth_token)

        target_queue = new_queues_mapping[annotation["queue"]].split("/")[-1]

        upload_document(document["original_file_name"], original_file, target_queue, token)

    return None


def create_extensions(new_queues_mapping, original_extensions, token, user_url):

    """
    Create new extensions from a list of original extensions
    :param new_queues_mapping: The extension should be mapped to the same queues as in the template organization.
    :param original_extensions: List of original extensions.
    :param token: Auth token to the new organization.
    :param user_url: User ID which will be assigned as a token owner for accessing the Rossum's API from extension.
    :return: List of extensions
    """

    headers = {"Authorization": "token {0}".format(token)}

    new_extensions = []

    for extension in original_extensions:

        payload = extension.copy()
        payload["queues"] = [new_queues_mapping[x] for x in extension["queues"]]
        payload["token_owner"] = user_url

        response = requests.post("https://api.elis.rossum.ai/v1/hooks", json=payload, headers=headers)

        new_extensions.append(response)

    return new_extensions


def upload_master_data_to_data_matching(token, target_queues, file, matching_code_column, entity):

    """
    Upload sample data to data matching database.
    :param token: Token of the organization where data should be uploaded.
    :param target_queues: List of where the master data should be uploaded.
    :param file: Master data to be uploaded - in JSON format.
    :param matching_code_column: Primary key of the master data, required when uploading.
    :param entity: The entity name of the data - (Purchase Orders, Suppliers, etc.)
    :return: Dict representing the response
    """

    login_to_data_matching_with_token(token)

    files = [('files', ('master_data.json', json.dumps(file), 'application/json'))]

    payload = {
            "encoding": "utf-8",
            "queues": target_queues,
            "matching_code_column": matching_code_column,
            "dataset": entity
    }

    cookies = {"session": HTTP_COOKIE}

    response = requests.post("https://data-matching.elis.rossum.ai/api/v1/import",
                             files=files,
                             data=payload,
                             cookies=cookies)

    if response.status_code == 200:
        print("Uploading data to data matching - OK")
    else:
        print("Uploading data to data matching - ERROR")

    return response.json()


def login_to_data_matching_with_token(token):

    """
    Login to the Data Matching API. User has to be logged in when using other endpoints.
    The Data Matching currently uses session cookie authentication. Therefore global Cookie is set.
    :param token: auth token provided by the Rossum API /login endpoint - https://api.elis.rossum.ai/docs/#login
    :return: dict with the API response
    """

    headers = {"Authorization": "Token {0}".format(token)}
    session = requests.Session()
    response = session.post("https://data-matching.elis.rossum.ai/api/v1/auth/token_login", headers=headers)

    global HTTP_COOKIE

    HTTP_COOKIE = session.cookies.get_dict()["session"]

    if response.status_code == 200:
        print("Logging in to data matching - OK")
    else:
        print("Logging in to data matching - ERROR")

    print(response.text)

    return response.json()


def upload_document(filename, content, queue_id, token):

    """
    Upload a document to a specific queue in the new organization
    :param filename: Filename to be uploaded.
    :param content: Content of the new file.
    :param queue_id: Queue where the file should be uploaded.
    :param token: Authentication token to the new organization.
    :return: Dict representing the new annotation
    """

    headers = {"Authorization": "token {0}".format(token)}

    response = requests.post("https://api.elis.rossum.ai/v1/queues/{0}/upload/{1}".format(queue_id, filename),
                             data=content,
                             headers=headers)

    if response.status_code == 201:
        print("Uploading new document - OK")
    else:
        print("Uploading new document - ERROR")

    return response.json()


def get_parser():

    """
    Parser for obtaining the parameters needed for running the script.
    :return:
    """

    arg_parser = argparse.ArgumentParser(description="Script for creating new organizations from master organization.")
    arg_parser.add_argument('--org_name', help='Organization name that will be created', metavar="org_name", type=str)
    arg_parser.add_argument('--username', help='Username of the new admin user.', metavar="username", type=str)
    arg_parser.add_argument('--email', help='Email of the new admin user.', metavar="email", type=str)
    arg_parser.add_argument('--password', help='Password of the new user.', metavar="password", type=str)
    arg_parser.add_argument('--create_key', help='Create key for creating new organizations in organization group.',
                            metavar="create_key", type=str)
    arg_parser.add_argument('--token', help='Token gained after logging to the Rossum API', metavar="token", type=str)

    # other arguments here ...
    return arg_parser


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    parser = get_parser()
    args = parser.parse_args()

    master_org_token = args.token

    organizations = get_all_organizations(master_org_token)

    master_data_org = get_master_data_organization(organizations)

    workspaces = get_all_workspaces(master_data_org, master_org_token)
    queues = get_all_queues(master_data_org, master_org_token)
    extensions = get_all_extensions(master_data_org, master_org_token)
    annotations = get_all_annotations(master_data_org, master_org_token)

    CREATE_KEY = args.create_key
    ORG_NAME = args.org_name
    USERNAME = args.username
    EMAIL = args.email
    PASSWORD = args.password

    organization = create_organization(CREATE_KEY, ORG_NAME, USERNAME, EMAIL, PASSWORD)

    new_org_token = login_to_specific_organization("https://api.elis.rossum.ai/v1/organizations/{0}".format(organization["id"]),
                                                   master_org_token)

    workspaces_mapping = create_workspaces("https://api.elis.rossum.ai/v1/organizations/{0}".format(organization["id"]),
                                           new_org_token,
                                           workspaces_list=workspaces)

    print("Workspaces mapping")
    print(workspaces_mapping)

    queues_mapping = create_queues(workspaces_mapping, new_org_token, master_org_token, queues_list=queues)

    print("Queues mapping")
    print(queues_mapping)

    extensions = create_extensions(queues_mapping, extensions, new_org_token, organization["users"][0])

    annotations = get_all_annotations(master_data_org, master_org_token)

    create_annotations(queues_mapping, annotations, new_org_token, master_org_token)

