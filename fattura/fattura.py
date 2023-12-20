## Licenza Libera progetto originario di Claudio Pizzillo (codice per accesso al sito)
## Antonino Accardo (codice per il controllo del file)
## Per effettuare il controllo sul portale ivaservizi.agenziaentrate.gov.it, inserire il nome del file nella relativa parte del codice. 

import base64
from datetime import timedelta, datetime, tzinfo, timezone
import json
from lxml import etree
import os
import pytz
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import re
import sys
import time


class Fattura():
    DOMAIN : str = 'ivaservizi.agenziaentrate.gov.it'
    SCHEMA : str = '../data/Schema_del_file_xml_FatturaPA_v1.2.2.xsd'
    
    def __init__(self, name:str=''):
        self.name = name

    @staticmethod
    def unixTime():
        dt = datetime.now(tz=pytz.utc)
        return str(int(dt.timestamp() * 1000))

    def create(self):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        now = datetime.now() # current date and time

        CF = sys.argv[1]
        PIN = sys.argv[2]
        Password  = sys.argv[3]
        PIVA  = sys.argv[4]

        s = requests.Session()
        s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'})
        s.headers.update({'Connection': 'keep-alive'})

        cookie_obj1 = requests.cookies.create_cookie(domain=self.DOMAIN,name='LFR_SESSION_STATE_20159',value='expired')
        s.cookies.set_cookie(cookie_obj1)
        cookie_obj2 = requests.cookies.create_cookie(domain=self.DOMAIN,name='LFR_SESSION_STATE_10811916',value=unixTime())
        s.cookies.set_cookie(cookie_obj2)
        r = s.get(f'https://{self.DOMAIN}/portale/web/guest', verify=False)

        print('Collegamento alla homepage')
        cookieJar = s.cookies

        print('Effettuo il login')
        payload = {'_58_saveLastPath': 'false', '_58_redirect' : '', '_58_doActionAfterLogin': 'false', '_58_login': CF , '_58_pin': PIN, '_58_password': Password}    
        r = s.post(f'https://{self.DOMAIN}/portale/home?p_p_id=58&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_pos=3&p_p_col_count=4&_58_struts_action=%2Flogin%2Flogin', data=payload)
        cookieJar = s.cookies

        liferay = re.findall(r"Liferay.authToken = '.*';", r.text)[0]
        p_auth = liferay.replace("Liferay.authToken = '","")
        p_auth = p_auth.replace("';", "")

        r = s.get(f'https://{self.DOMAIN}/dp/api?v=' + unixTime())
        cookieJar = s.cookies

        print('Seleziono il tipo di incarico')
        payload = {'sceltaincarico': PIVA + '-FOL', 'tipoincaricante' : 'incDiretto'}    
        r = s.post(f'https://{self.DOMAIN}/portale/scelta-utenza-lavoro?p_auth='+ p_auth + '&p_p_id=SceltaUtenzaLavoro_WAR_SceltaUtenzaLavoroportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_SceltaUtenzaLavoro_WAR_SceltaUtenzaLavoroportlet_javax.portlet.action=incarichiAction', data=payload)

        print('Aderisco al servizio')
        r = s.get(f'https://{self.DOMAIN}/ser/api/fatture/v1/ul/me/adesione/stato/')
        cookieJar = s.cookies

        headers_token = {'x-xss-protection': '1; mode=block',
                'strict-transport-security': 'max-age=16070400; includeSubDomains',
                'x-content-type-options': 'nosniff',
                'x-frame-options': 'deny'}
        r = s.get(f'https://{self.DOMAIN}/cons/cons-services/sc/tokenB2BCookie/get?v='+unixTime() , headers = headers_token )
        cookieJar = s.cookies
        tokens = r.headers

        xb2bcookie = r.headers.get('x-b2bcookie')
        xtoken = r.headers.get('x-token')

        s.headers.update({'Host': self.DOMAIN})
        s.headers.update({'Referer': 'https://{self.DOMAIN}/cons/cons-web/?v=' + unixTime()})
        s.headers.update({'Accept': 'application/json, text/plain, */*'})
        s.headers.update({'Accept-Encoding': 'gzip, deflate, br'})
        s.headers.update({'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6'})
        s.headers.update({'DNT': '1'})
        s.headers.update({'X-XSS-Protection': '1; mode=block'})
        s.headers.update({'Strict-Transport-Security': 'max-age=16070400; includeSubDomains'})
        s.headers.update({'X-Content-Type-Options': 'nosniff'})
        s.headers.update({'X-Frame-Options': 'deny'})
        s.headers.update({'x-b2bcookie': xb2bcookie})
        s.headers.update({'x-token': xtoken})

        headers = {'Host': self.DOMAIN,
                'referer': f'https://{self.DOMAIN}/cons/cons-web/?v=' + unixTime(),
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6',
                'DNT': '1',
                'x-xss-protection': '1; mode=block',
                'strict-transport-security': 'max-age=16070400; includeSubDomains',
                'x-content-type-options': 'nosniff',
                'x-frame-options': 'deny',
                'x-b2bcookie': xb2bcookie,
                'x-token': xtoken,
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}

        print('Accetto le condizioni')
        r = s.get(f'https://{self.DOMAIN}/cons/cons-services/rs/disclaimer/accetta?v='+unixTime() , headers = headers_token )
        cookieJar = s.cookies

        print('controllo file')
        r = s.get(f'https://{self.DOMAIN}/ser/fatturewizard/html/partials/supporto/controllo.html?v='+now.strftime("%Y-%m-%d"), headers = headers)

        #seleziona file 
        nome_file='inserire nome file'
        with open(nome_file, "rb") as f:
            headers_file= { 
                'Host': self.DOMAIN,
                'referer': f'https://{self.DOMAIN}/ser/fatturewizard/',
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6',
                'x-xss-protection': '1; mode=block',
                'strict-transport-security': 'max-age=16070400; includeSubDomains',
                'x-content-type-options': 'nosniff',
                'x-frame-options': 'deny',
                'x-b2bcookie': xb2bcookie,
                'x-token': xtoken,
                'sec-fetch-site': 'same-origin',
                'content-length':'9049',
                'content-type': 'application/octet-stream',
                'sec-fetch-mode': 'cors',
                'connection': 'keep-alive',
                'x-nome-file': nome_file,
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
            }    

            print(f)
            r = s.post(f'https://{self.DOMAIN}/ser/api/fatture/v1/controllo/fatture/?v=' + unixTime(),
                       headers=headers_file, data=f)
            print(r.status_code)
            if r.status_code == 500:
                print('Servizio dell''Azenzia delle entrate non disponibile')
                print('Controllo non andato a buon fine, riprovare più tardi')
                print('Disconnessione in corso')
                r = s.get(f'https://{self.DOMAIN}/portale/c/portal/logout')
                sys.exit()
            elif r.status_code == 200:
                print('ok')
                print(r.text)
            c = str(r.text)
            time.sleep(10)
            r = s.get(f'https://{self.DOMAIN}/ser/api/fatture/v1/controllo/fatture/'+c+'/?v='+unixTime(), headers=headers)
            if r.status_code == 200:
                print('ok')
            time.sleep(10) 
            with open('fe_controllo.json', 'wb') as data_file:
                data_file.write(r.content)

            with open('fe_controllo.json') as data_file:    
                datas = json.load(data_file)
                control= (datas['completato'])
                print (control)
            if control != 'True':
                print('Controllo andato a buon fine')
                print('Lavoro finito disconnessione in corso')
                r = s.get(f'https://{self.DOMAIN}/portale/c/portal/logout')
                if r.status_code == 200:
                    print('Fine sessione')   
            else:
                print('Controllo non andato a buon fine')
                print('Lavoro finito disconnessione in corso')
                r = s.get(f'https://{self.DOMAIN}/portale/c/portal/logout')
                if r.status_code == 200:
                    print('Fine sessione')

            sys.exit()

    def validate(self, filename:str):
        # Load the schema
        with open(self.SCHEMA, 'rb') as f:
            schema_root = etree.XML(f.read())
        schema = etree.XMLSchema(schema_root)

        # Parse the XML file
        xml_doc = etree.parse(filename)

        # Validate
        if schema.validate(xml_doc):
            print("XML is valid.")
        else:
            print("XML is invalid.")
            print(schema.error_log)
