import os
import onedrivesdk
from onedrivesdk.helpers import GetAuthCodeServer
from MoodleWrangler.secret import onedrive


def upload_courses(location):
    scopes = ['wl.signin', 'wl.offline_access', 'onedrive.readwrite']

    client = onedrivesdk.get_default_client(
        client_id=onedrive['client_id'], scopes=scopes)

    auth_url = client.auth_provider.get_auth_url(onedrive['redirect_uri'])

    # This will block until we have the code
    code = GetAuthCodeServer.get_auth_code(auth_url, onedrive['redirect_uri'])

    client.auth_provider.authenticate(code, onedrive['redirect_uri'], onedrive['client_secret'])

    # Create app folder
    app_folder = onedrivesdk.Folder()
    item = onedrivesdk.Item()
    item.name = 'MoodleWrangler'
    item.folder = app_folder

    returned_root_folder = client.item(drive='me', id='root').children.add(item)
    path = location + '/'
    for folder in os.listdir(path):
        course_folder = onedrivesdk.Folder()
        course_item = onedrivesdk.Item()
        course_item.name = folder.title().strip()
        print(course_item.name)
        course_item.folder = course_folder
        returned_course_folder = client.item(drive='me', id=returned_root_folder.id).children.add(course_item)
        sub_directory = path + folder.title()
        for file in os.listdir(sub_directory):
            file_name = file.title().strip()
            client.item(drive='me', id=returned_course_folder.id).children[file_name].upload(sub_directory + '/' + file_name)
            print("Uploaded: " + file_name)
    print("Finished uploads.")
