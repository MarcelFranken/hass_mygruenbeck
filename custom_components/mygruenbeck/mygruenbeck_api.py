# mygruenbeck_api.py

import requests
import logging
import re
import time
from urllib.parse import urlparse, parse_qs, urlencode
from .utils import generate_code_verifier, generate_code_challenge
from .const import DOMAIN, USER_AGENT


_LOGGER = logging.getLogger(__name__)

async def login(username, password, hass):
    try:
        code_verifier = generate_code_verifier()
        code_challenge = generate_code_challenge(code_verifier)
        # Step 1: Perform initial GET request
        url = "https://gruenbeckb2c.b2clogin.com/a50d35c1-202f-4da7-aa87-76e51a3098c6/b2c_1a_signinup/oauth2/v2.0/authorize"
        params = {
            "x-client-Ver": "0.8.0",
            "state": "NjkyQjZBQTgtQkM1My00ODBDLTn3MkYtOTZCQ0QyQkQ2NEE5",
            "client_info": "1",
            "response_type": "code",
            "code_challenge_method": "S256",
            "x-app-name": "Grünbeck",
            "x-client-OS": "14.3",
            "x-app-ver": "1.2.1",
            "scope": "https%3A%2F%2Fgruenbeckb2c.onmicrosoft.com%2Fiot%2Fuser_impersonation%20openid%20profile%20offline_access",
            "x-client-SKU": "MSAL.iOS",
            "code_challenge": code_challenge,
            "x-client-CPU": "64",
            "client-request-id": "F2929DED-2C9D-49F5-A0F4-31215427667C",
            "redirect_uri": "msal5a83cc16-ffb1-42e9-9859-9fbf07f36df8://auth",
            "client_id": "5a83cc16-ffb1-42e9-9859-9fbf07f36df8",
            "haschrome": "1",
            "return-client-request-id": "true",
            "x-client-DM": "iPhone"
        }

        # Header für die Anfrage
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "br, gzip, deflate",
            "Connection": "keep-alive",
            "Accept-Language": "de-de",
            "User-Agent": USER_AGENT  # Geben Sie Ihren User-Agent ein
        }
        
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            # Die Anfrage war erfolgreich
            # Step 2: Extract CSRF token and other required parameters from the response
            csrf = re.search(r'csrf=([^,]+),', response.text).group(1)
            trans_id = re.search(r'transId=([^,]+),', response.text).group(1)
            policy = re.search(r'policy=([^,]+),', response.text).group(1)
            tenant = re.search(r'tenant=([^,]+),', response.text).group(1)
            cookies = "; ".join([cookie.split("; ")[0] for cookie in response.headers.get("set-cookie")])
        else:
            # Fehler bei der Anfrage
            print(f"Fehler: {response.status_code}")

        
        # Step 3: Prepare the POST request data
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-CSRF-TOKEN": csrf,
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://gruenbeckb2c.b2clogin.com",
            "Cookie": cookies,
            "User-Agent": USER_AGENT  # Geben Sie Ihren User-Agent ein
        }
        data = {
            "request_type": "RESPONSE",
            "signInName": username,
            "password": password,
        }
        
        # Step 4: Perform POST request
        response = requests.post(
            f"https://gruenbeckb2c.b2clogin.com/{tenant}/SelfAsserted?tx={trans_id}&p={policy}",
            data=urlencode(data),
            headers=headers,
        )
        if response.status_code == 200:
            # Die Anfrage war erfolgreich
            updated_cookies = "; ".join([cookie.split("; ")[0] for cookie in response.headers.get("set-cookie", [])])
            updated_cookies += f"; x-ms-cpim-csrf={csrf}"

            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Encoding": "br, gzip, deflate",
                "Connection": "keep-alive",
                "Accept-Language": "de-de",
                "Cookie": updated_cookies,
                "User-Agent": USER_AGENT  # Füge deinen User-Agent hier ein
            }

            get_response = requests.get(
                f"https://gruenbeckb2c.b2clogin.com{tenant}/api/CombinedSigninAndSignup/confirmed?csrf_token={csrf}&tx={trans_id}&p={policy}",
                headers=headers
            )

            if get_response.status_code == 200:
                # Erfolgreich
                print(f"Super")
            else:
                # Fehler bei der GET-Anforderung
                # Überprüfe, ob es sich um einen Redirect mit Statuscode 302 handelt
                if get_response.status_code == 302:
                    location_header = get_response.headers["Location"]

                    # Überprüfe, ob die "code"-Parameter in der URL vorhanden ist
                    if "code=" in location_header:
                        start = location_header.find("code=") + len("code=")
                        end = location_header.find("&", start) if "&" in location_header else len(location_header)
                        code = location_header[start:end]

                        # Konfiguration für den POST-Anforderungsaufbau
                        headers = {
                            "Host": "gruenbeckb2c.b2clogin.com",
                            "x-client-SKU": "MSAL.iOS",
                            "Accept": "application/json",
                            "x-client-OS": "14.3",
                            "x-app-name": "Grünbeck",
                            "x-client-CPU": "64",
                            "x-app-ver": "1.2.0",
                            "Accept-Language": "de-de",
                            "client-request-id": "F2929DED-2C9D-49F5-A0F4-31215427667C",
                            "x-ms-PkeyAuth": "1.0",
                            "x-client-Ver": "0.8.0",
                            "x-client-DM": "iPhone",
                            "User-Agent": "Gruenbeck/354 CFNetwork/1209 Darwin/20.2.0",
                            "return-client-request-id": "true",
                        }
                        
                        # URL für die POST-Anforderung
                        post_url = f"https://gruenbeckb2c.b2clogin.com{tenant}/oauth2/v2.0/token"

                        # Daten für die POST-Anforderung
                        post_data = {
                            "client_info": "1",
                            "scope": "https://gruenbeckb2c.onmicrosoft.com/iot/user_impersonation openid profile offline_access",
                            "code": code,
                            "grant_type": "authorization_code",
                            "code_verifier": code_verifier,
                            "redirect_uri": "msal5a83cc16-ffb1-42e9-9859-9fbf07f36df8://auth",
                            "client_id": "5a83cc16-ffb1-42e9-9859-9fbf07f36df8",
                        }

                        # Führe die POST-Anforderung aus
                        post_response = requests.post(post_url, data=post_data, headers=headers)

                        if post_response.status_code == 200:
                            # Erfolgreiche POST-Anforderung
                            response_data = post_response.json()
                            accessToken = response_data.get("access_token")
                            refreshToken = response_data.get("refresh_token")
                            hass.data[DOMAIN] = {"accessToken": accessToken, "refreshToken": refreshToken}

                            return True
                            # Führe hier die gewünschten Aktionen aus, z.B. Setze den Token, starte eine Aktualisierung, etc.
                            # ...

                        else:
                            # Fehler bei der POST-Anforderung
                            print(f"Fehler bei POST-Anforderung: {post_response.status_code}")

                else:
                    # Fehlerfall behandeln, wenn keine Weiterleitung oder ein anderer Fehler auftritt
                    print("Fehler: Weiterleitung oder anderer Fehler")

        else:
            # Fehler bei der Anfrage
            print(f"Fehler: {response.status_code}")

      

    except Exception as e:
        _LOGGER.error(f"Login error: {e}")
        return None
    
# async def getDevices():
#     # Hier implementieren Sie die Logik zum Abrufen der Geräte mit einem HTTP API-Aufruf
#     # Rückgabewert sollte eine Liste von Geräten oder None sein, wenn das Abrufen fehlschlägt
#     # Beispiel:
#     response = requests.post("https://example.com/login", data={"username": username, "password": password})
#     if response.status_code == 200:
#         return True
#     else:
#         return False

# async def parseDeviceInfos(device):
#     # Hier implementieren Sie die Logik zum Abrufen von Geräteinformationen mit einem HTTP API-Aufruf
#     # Beispiel:
#     # device_info = make_api_call_to_get_device_info(device)
#     response = requests.post("https://example.com/login", data={"username": username, "password": password})
#     if response.status_code == 200:
#         return True
#     else:
#         return False
#     # if device_info:
#     #     # Verarbeiten Sie die Geräteinformationen
#     #     pass
#     # else:
#     #     _LOGGER.error(f"Failed to get information for device {device['id']}")
