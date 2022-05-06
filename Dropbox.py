import requests
import urllib
import webbrowser
from socket import AF_INET, socket, SOCK_STREAM
import json
import helper

app_key = ''
app_secret = ''
server_addr = "localhost"
server_port = 8090
redirect_uri = "http://" + server_addr + ":" + str(server_port)

class Dropbox:
    _access_token = ""
    _path = "/"
    _files = []
    _root = None
    _msg_listbox = None

    def __init__(self, root):
        self._root = root

    def local_server(self):
        # sartu kodea hemen

        return auth_code

    def do_oauth(self):
        # sartu kodea hemen

        self._access_token = access_token
        self._root.destroy()

    def list_folder(self, msg_listbox, cursor="", edukia_json_entries=[]):
        if not cursor:
            print("/list_folder")
            uri =
            datuak =
            # sartu kodea hemen
        else:
            print("/list_folder/continue")
            uri =
            datuak =
            # sartu kodea hemen

        # Call Dropbox API
        # sartu kodea hemen

        edukia_json = json.loads(edukia)
        if edukia_json['has_more']:
            # sartu kodea hemen
            self.list_folder(msg_listbox, edukia_json['cursor'], edukia_json_entries)
        else:
            # sartu kodea hemen
            self._files = helper.update_listbox2(msg_listbox, self._path, edukia_json_entries)

    def transfer_file(self, file_path, file_data):
        print("/upload " + file_path)
        # sartu kodea hemen

    def delete_file(self, file_path):
        print("/delete_file " + file_path)
        # sartu kodea hemen

    def create_folder(self, path):
        print("/create_folder " + path)
        # sartu kodea hemen
