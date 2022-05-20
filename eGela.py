from tkinter import messagebox as tkMessageBox
import requests
import urllib
from bs4 import BeautifulSoup
import time
import helper

class eGela:
    _login = 0
    _cookiea = ""
    _ikasgaia = ""
    _refs = []
    _root = None

    def __init__(self, root):
        self._root = root

    def check_credentials(self, username, password, event=None):
        popup, progress_var, progress_bar = helper.progress("check_credentials", "Logging into eGela...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("##### 1. ESKAERA (Login inprimakia lortu 'logintoken' ateratzeko #####")

        metodoa = 'GET'
        uria = "https://egela.ehu.eus/login/index.php"
        goiburuak = {'Host': 'egela.ehu.eus'}

        print(metodoa + "\n")
        print(uria + "\n")

        print("##### HTML-aren azterketa... #####")
        # sartu kodea hemen

        erantzuna = requests.request(metodoa, uria, headers=goiburuak, allow_redirects=False)

        kodea = erantzuna.status_code
        deskribapena = erantzuna.reason
        print("STATUS: " + str(kodea) + " DESKRIBAPENA: " + deskribapena)
        edukia = erantzuna.content

        self._cookiea = erantzuna.headers['Set-Cookie'].split(";")[0]
        print("Set-Cookie: " + self._cookiea + "\n")

        soup = BeautifulSoup(edukia, 'html.parser')
        logint = soup.find('input', {'name': 'logintoken'})
        logintoken = logint["value"]
        print("Logintoken: " + logintoken + "\n")

        action = soup.find('form')
        Location = action["action"]
        print("Location: " + Location + "\n")

        progress = 25
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)

        print("\n##### 2. ESKAERA (Kautotzea -datu bidalketa-) #####")
        # sartu kodea hemen
        metodoa = 'POST'
        uria = Location
        goiburuak = {'Host': 'egela.ehu.eus',
                     'Cookie': self._cookiea,
                     'Content-Type': "application/x-www-form-urlencoded"}
        edukia = {'logintoken': logintoken, 'username': username.get(), 'password': password.get()}
        print(metodoa + "\n")
        print(uria + "\n")

        print("---------------BIGARREN ESKAERAREN ERANTZUNA--------------\n")

        edukia_encoded = urllib.parse.urlencode(edukia)
        erantzuna2 = requests.request(metodoa, uria, data=edukia_encoded, headers=goiburuak, allow_redirects=False)

        kodea = erantzuna2.status_code
        deskribapena = erantzuna2.reason
        print("STATUS: " + str(kodea) + " DESKRIBAPENA: " + deskribapena)
        edukia = erantzuna2.content

        self._cookiea = erantzuna2.headers['Set-Cookie'].split(";")[0]
        print("Set-Cookie: " + self._cookiea)
        locationTestSession = erantzuna2.headers['Location'].split("?testsession=")[1]
        print("Location: " + locationTestSession)

        progress = 50
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)

        print("\n##### 3. ESKAERA (berbidalketa) #####")
        # sartu kodea hemen

        metodoa = 'GET'
        uria = "https://egela.ehu.eus/login/index.php?testsession=" + locationTestSession
        goiburuak = {'Host': 'egela.ehu.eus', 'Cookie': self._cookiea, 'Content-Type': 'application/x-www-form-urlencoded'}

        print(metodoa + "\n")
        print(uria + "\n")

        print("---------------HIRUGARREN ESKAERAREN ERANTZUNA--------------\n")

        erantzuna = requests.request(metodoa, uria, headers=goiburuak, allow_redirects=False)

        kodea = erantzuna.status_code
        deskribapena = erantzuna.reason
        print("STATUS: " + str(kodea) + " DESKRIBAPENA: " + deskribapena)
        location = erantzuna.headers['Location']
        print("Location: " + location)

        progress = 75
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)

        print("\n##### 4. ESKAERA (eGelako orrialde nagusia) #####")
        # sartu kodea hemen

        metodoa = 'GET'
        uria = location
        goiburuak = {'Host': 'egela.ehu.eus', 'Cookie': self._cookiea, 'Content-Type': 'application/x-www-form-urlencoded'}

        print("---------------LAUGARREN ESKERA--------------\n")
        print(metodoa + "\n")
        print(uria + "\n")

        erantzuna = requests.request(metodoa, uria, headers=goiburuak, allow_redirects=False)

        kodea = erantzuna.status_code
        deskribapena = erantzuna.reason
        print("STATUS: " + str(kodea) + " DESKRIBAPENA: " + deskribapena)

        edukia = erantzuna.content
        soup = BeautifulSoup(edukia, 'html.parser')
        usern = str(soup.find('span', {'class': 'usertext mr-1'}))
        bigarrenZatia = usern.split(">")[1]
        izena = bigarrenZatia.split("<")[0]

        bilaketa = soup.find('div', {'data-courseid': '57996'})
        a = str(bilaketa.find('a'))

        nextUriESKUINA = a.split('href="')[1]
        self._ikasgaia = nextUriESKUINA.split('">')[0]



        progress = 100
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)
        popup.destroy()

        edukia_Str = erantzuna.text
        print("\n##### LOGIN EGIAZTAPENA #####")
        aurkituta = edukia_Str.find("Saio-hasiera baliogabea, saiatu berriz, mesedez")
        if aurkituta == -1:
            # sartu kodea hemen
            self._login = 1
            # KLASEAREN ATRIBUTUAK EGUNERATU
            print("LOGIN CORRECT")
            self._root.destroy()
            # sartu kodea hemen

        else:
            tkMessageBox.showinfo("Alert Message", "Login incorrect!")

    def get_pdf_refs(self):
        popup, progress_var, progress_bar = helper.progress("get_pdf_refs", "Downloading PDF list...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("\n##### 5. ESKAERA (Ikasgairen eGelako orrialdea) #####")
        # sartu kodea hemen

        metodoa = 'GET'
        uria = self._ikasgaia
        goiburuak = {'Host': 'egela.ehu.eus', 'Cookie': self._cookiea, 'Content-Type': 'application/x-www-form-urlencoded'}

        erantzuna = requests.request(metodoa, uria, headers=goiburuak, allow_redirects=False)

        print("\n##### HTML-aren azterketa... #####")
        # sartu kodea hemen
        kodea = erantzuna.status_code
        deskribapena = erantzuna.reason
        print("WebSistemak eskaera: " + str(kodea) + " " + deskribapena)
        edukia = erantzuna.content

        self._refs = []
        soup = BeautifulSoup(edukia, 'html.parser')

        item_results = soup.find_all('img', {'class': 'iconlarge activityicon'})
        for each in item_results:
            if each['src'].find("/pdf") != -1:
                print("\nPDF-dun linka aurkitu da:")
                pdf_link = each.parent['href']
                uria = pdf_link
                headers = {'Host': 'egela.ehu.eus', 'Cookie': self._cookiea}
                erantzuna = requests.get(uria, headers=headers, allow_redirects=False)
                print("GET " + uria)
                kodea = erantzuna.status_code
                deskribapena = erantzuna.reason
                print(str(kodea) + " " + deskribapena)
                edukia = erantzuna.content

                soup2 = BeautifulSoup(edukia, 'html.parser')
                div_pdf = soup2.find('div', {'class': 'resourceworkaround'})
                pdf_link = div_pdf.a['href']
                pdf_izena = pdf_link.split('/')[-1]
                hizt = {pdf_link, pdf_izena}
                self._refs.append({'pdf-name': pdf_izena, 'pdf-link': pdf_link})

        progress_step = float(100.0 / len(self._refs))


        progress += progress_step
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)



        print(self._refs)
        popup.destroy()

        return self._refs

    def get_pdf(self, selection):
        print("##### PDF-a deskargatzen... #####")
        # sartu kodea hemen
        pdf_linka = self._refs[selection]['pdf-link']
        pdf_name = self._refs[selection]['pdf-name']
        metodoa = 'GET'
        uria = pdf_linka
        goiburuak = {'Host': 'egela.ehu.eus', 'Cookie': self._cookiea, 'Content-Type': 'application/x-www-form-urlencoded'}

        erantzuna = requests.request(metodoa, uria, headers=goiburuak, allow_redirects=False)

        print("Deskargatzen ari den pdf-a: ", pdf_linka)

        pdf_file = open(pdf_name, 'wb')
        pdf_file.write(erantzuna.content)
        pdf_file.close()
        print("DESKARGATUTA!!!")
        return pdf_name, pdf_file
