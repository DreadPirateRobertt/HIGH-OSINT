import requests
import json
import os
from requests.auth import HTTPBasicAuth
import base64
from time import sleep
import time

from colorama import init
from colorama import Fore
init(autoreset=True)

def __Api_Token_Access():
    __username = base64.b64decode('')
    __password = base64.b64decode('')
    __accessToken = ''

    data = {
        'username': __username,
        'password': __password,
    }
    jsonData = json.dumps(data, indent=4)
    try:
        r = requests.post('https://api.zoomeye.org/user/login', data=jsonData)
        result = json.loads(r.text)
        __accessToken = result['access_token']
        #print "\n Token: {}".format(__accessToken)
        return str(__accessToken)
    except Exception as e:
        print('[-] Username or password is wrong')
        os._exit(1)

__Token = __Api_Token_Access()
print __Token.strip()

def __getQuery( flag, query, page='', facets=''):
    query = '?query=' + query
    page = '' if not page else ('&page='+str(page))
    facets = '' if not facets else ('&facets='+str(facets))
    queryUrl = 'https://api.zoomeye.org/'+flag+'/search'+query+page+facets
    return queryUrl


def search( __Token, flag, query, facets=''):
    page = 1
    try:
        while True:
            queryUrl = __getQuery(flag, query, page=page, facets=facets)
            r = requests.get(queryUrl, headers={'Authorization': 'JWT '+__Token})
            #print r.text
            __json = r.json()
            ZoomEyeBanner(__json)
            #raw_input('SFF')
            time.sleep(1.5)
            if 'error' in json.loads(r.text).keys():
                print('[-] Account was break, excceeding the max limitations. The page is', page)
                break
            page += 1
    except KeyboardInterrupt:
        print "Exit"
        exit()

def ZoomEyeBanner(__data):
   for __loop_markup in range(0,19):
        time.sleep(3)
        print "\n[!] ZoomEye Advanced Search Enginne\n"
        try:
            try:
                print Fore.CYAN + "[!] Organization: ", Fore.BLUE + __data["matches"][__loop_markup]["geoinfo"]["organization"]
            except:
                pass
            try:
                print Fore.CYAN + "[-] IP: ",Fore.BLUE + __data["matches"][__loop_markup]["ip"]
            except:
                pass
            try:
                print Fore.CYAN + "[-] Port: ", Fore.BLUE +str(__data["matches"][__loop_markup]["portinfo"]["port"])
            except:
                pass
            try:
                print Fore.CYAN + "[-] City: ", Fore.GREEN +__data["matches"][__loop_markup]["geoinfo"]["city"]["names"]["en"]
            except:
                pass
            try:
                print Fore.CYAN + "[-] Country: ", Fore.BLUE +__data["matches"][__loop_markup]["geoinfo"]["country"]["names"]["en"]+" - "+Fore.RED +"["+__data["matches"][__loop_markup]["geoinfo"]["country"]["code"]+"]"
            except:
                pass
            try:
                print Fore.CYAN + "[-] Continent: ", Fore.BLUE +__data["matches"][__loop_markup]["geoinfo"]["continent"]["names"]["en"]
            except:
                pass
            try:
                print Fore.CYAN + "[-] isp: ", Fore.BLUE +__data["matches"][__loop_markup]["geoinfo"]["isp"]
            except:
                pass
            try:
                print Fore.CYAN + "[-] Subdivisions: ", Fore.BLUE +__data["matches"][__loop_markup]["geoinfo"]["subdivisions"]["names"]["en"]
            except:
                pass
            try:
                print Fore.CYAN + "[-] GeoInfo Location: lat: {} long: {}  (Google Maps)".format(__data["matches"][__loop_markup]["geoinfo"]["location"]["lat"], __data["matches"][__loop_markup]["geoinfo"]["location"]["lon"])
            except:
                pass
            print ''
            #raw_input('[!] Enter to Skip')
            __cam = str(__data["matches"][__loop_markup]["ip"])+":"+str(__data["matches"][__loop_markup]["portinfo"]["port"])
            ImpropperControlPrivilege(__cam)
        except KeyboardInterrupt:
            print "Exit"
            exit()

search(__Token, 'host', 'Brickcom', 'os')
