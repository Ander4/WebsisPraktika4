import requests
import urllib
import webbrowser
from socket import AF_INET, socket, SOCK_STREAM
import json
import helper

app_key = 'cteaexf730n96we'
app_secret = 'qs7mufd0v82rncp'
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

        # 8090. portuan entzuten dagoen zerbitzaria sortu
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind((server_addr, server_port))
        listen_socket.listen(1)
        print("\t\tSocket listening on port " + str(server_port))

        # nabitzailetik 302 eskaera jaso
        # ondorengo lerroan programa gelditzen da, zerbitzariak 302 eskaera jasotzen duen arte
        client_connection, client_address = listen_socket.accept()
        eskaera = client_connection.recv(1024).decode()
        print("\t\tNabigatzailetik ondorengo eskaera jaso da:")
        print("\n" + eskaera)

        # eskaeran "auth_code"-a bilatu
        lehenengo_lerroa = eskaera.split('\n')[0]
        aux_auth_code = lehenengo_lerroa.split(' ')[1]
        auth_code = aux_auth_code[7:].split('&')[0]
        print("auth_code: " + auth_code)

        # erabiltzaileari erantzun bat bueltatu
        http_response = """\
            HTTP/1.1 200 OK

            <html> 
            <head>
            <title>Proba</title>
            </head> 
            <body> The authentication flow has completed. Close this window. </body> 
            </html> """
        client_connection.sendall(str.encode(http_response))
        client_connection.close()

        return auth_code

    def do_oauth(self):

        # Authorization
        uri = "https://www.dropbox.com/oauth2/authorize"
        datuak = {'response_type': 'code',
                  'client_id': app_key,
                  'redirect_uri': redirect_uri}
        datuak_kodifikatuta = urllib.parse.urlencode(datuak)
        step2_uri = uri + '?' + datuak_kodifikatuta
        print("\t" + step2_uri)
        webbrowser.open_new(step2_uri)  # eskaera nabigatzailean egin

        auth_code = self.local_server()

        # Exchange authorization code for access token

        print("auth_code: " + auth_code)
        uri = "https://api.dropboxapi.com/oauth2/token"
        goiburuak = {'Host': 'api.dropboxapi.com', 'Content-Type': 'application/x-www-form-urlencoded'}
        datuak = {'code': auth_code, 'client_id': app_key, 'client_secret': app_secret, 'redirect_uri': redirect_uri,
                  'grant_type': 'authorization_code'}
        erantzuna = requests.post(uri, headers=goiburuak, data=datuak, allow_redirects=False)
        status = erantzuna.status_code
        edukia = erantzuna.text
        edukia_json = json.loads(edukia)
        access_token = edukia_json['access_token']
        print("Status: ")
        print(str(status))
        print("Edukia: ")
        print(edukia)
        print("access_token: ")
        print(access_token)

        self._access_token = access_token
        self._root.destroy()

    def list_folder(self, msg_listbox, cursor="", edukia_json_entries=[]):
        if not cursor:
            print("/list_folder")
            uri = "https://api.dropboxapi.com/2/files/list_folder"
            datuak = {'path': ''}
            # sartu kodea hemen
        else:
            print("/list_folder/continue")
            uri = "https://api.dropboxapi.com/2/files/list_folder/continue"
            datuak = {"cursor": cursor}
            # sartu kodea hemen

        # Call Dropbox API
        goiburuak = {'Host': 'api.dropboxapi.com',
                     'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json'}

        datuak_json = json.dumps(datuak)
        erantzuna = requests.post(uri, headers=goiburuak, data=datuak_json, allow_redirects=False)
        status = erantzuna.status_code
        print("\tStatus: " + str(status))
        edukia = erantzuna.text
        print("\tEdukia:")
        print(edukia)

        edukia_json = json.loads(edukia)
        if edukia_json['has_more']:
            # sartu kodea hemen
            self.list_folder(msg_listbox, edukia_json['cursor'], edukia_json_entries)
        else:
            print("\n\t ############ FITXATEGIEN ZERRENDA ############\n")
            for izena in edukia_json['entries']:
                print(izena['name'] + "\n")
                self._files = helper.update_listbox2(msg_listbox, self._path, edukia_json_entries)

    def transfer_file(self, file_path, file_data):
        print("/upload " + file_path)
        # sartu kodea hemen

    def delete_file(self, file_path):
        print("/delete_file " + file_path)
        uri = "https://api.dropboxapi.com/2/files/delete_v2"
        datuak = {'path': file_path}
        datuak_json = json.dumps(datuak)

        # Call Dropbox API
        goiburuak = {'Host': 'api.dropboxapi.com',
                     'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json'}
        erantzuna = requests.post(uri, headers=goiburuak, data=datuak_json, allow_redirects=False)
        status = erantzuna.status_code
        print("\tStatus: " + str(status))

    def create_folder(self, path):
        print("/create_folder " + path)
        uri = "https://api.dropboxapi.com/2/files/create_folder_v2"
        datuak = {'path': path}
        datuak_json = json.dumps(datuak)

        # Call Dropbox API
        goiburuak = {'Host': 'api.dropboxapi.com',
                     'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json'}
        erantzuna = requests.post(uri, headers=goiburuak, data=datuak_json, allow_redirects=False)
        status = erantzuna.status_code
        print("\tStatus: " + str(status))
