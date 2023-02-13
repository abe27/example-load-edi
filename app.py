# from nanoid import generate
from datetime import datetime, timedelta
import time
import urllib
import os
import sys
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import urllib3
## Load .env file
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


## Initialize variables
API_PROD=False
if str(os.getenv("API_PROD")).lower() == "true":
    API_PROD=True
API_HOST=os.getenv("API_HOST")
API_USERNAME = os.getenv("API_USERNAME")
API_PASSWORD = os.getenv("API_PASSWORD")
LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")
SOURCE_DIR = os.getenv("SOURCE_DIR","data/download")

### Line Notify API Function
def line_notification(msg):
    try:
        url = "https://notify-api.line.me/api/notify"
        payload = f"message={msg}"
        headers = {
            "Authorization": f"Bearer {LINE_NOTIFY_TOKEN}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = requests.request("POST",
                                    url,
                                    headers=headers,
                                    data=payload.encode("utf-8"))
        print(f"line status => {response}")
        return True
    except Exception as ex:
        print(ex)
        pass

    return False

def main():
    ## Step 1 login
    password = urllib.parse.quote(API_PASSWORD)
    payload = f'operation=LOGON&remote={API_USERNAME}&password={password}'
    urllib3.disable_warnings()
    session = requests.request("POST",API_HOST,headers={    'Content-Type': 'application/x-www-form-urlencoded', },verify=False,data=payload,timeout=3)
    txt = None
    docs = BeautifulSoup(session.text, "html.parser")
    for i in docs.find_all("hr"):
        txt = (i.previous).replace("\n", "")

    is_status = True
    if txt.find("751") >= 0:
        is_status = False
    ## Step 2 Download And Save TXT file
    if is_status:
        etd = "20230212"
        if API_PROD:
            etd = str((datetime.now() - timedelta(days=1)).strftime("%Y%m%d"))

        if session.status_code == 200:
            payload = f"operation=DIRECTORY&fromdate={etd}&Submit=Receive"
            r = requests.request(
                "POST",
                API_HOST,
                data=payload,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                verify=False,
                timeout=3,
                cookies=session.cookies,
            )
            # print(type(r))
            soup = BeautifulSoup(r.text, "html.parser")
            for tr in soup.find_all("tr"):
                found = False
                i = 0
                docs = []
                for td in tr.find_all("td"):
                    txt = (td.text).rstrip().lstrip()
                    docs.append(txt)
                    if td.find("a") != None:
                        found = True

                # False =debug,True=prod.
                if found is API_PROD:
                    if len(docs) >= 9:
                        edi_type = "RECEIVE"
                        if str(docs[3])[:len("OES.VCBI")] == "OES.VCBI":
                            edi_type = "ORDERPLAN"

                        l = {
                            "mailbox": docs[0],
                            "batch_id": docs[1],
                            "batch_file": docs[3],
                            "uploaded_at": datetime.strptime(f"{docs[4]} {docs[5]}", "%b %d, %Y %I:%M %p"),
                            "mailto": docs[8]
                        }
                        url_downloaded = f"{API_HOST}?operation=DOWNLOAD&mailbox_id={API_USERNAME}&batch_num={docs[1]}&data_format={docs[7]}&batch_id={docs[3]}"
                        # makedir folder edi is exits
                        dirs_dist = f'{SOURCE_DIR}/{edi_type}/{(l["uploaded_at"]).strftime("%Y%m%d")}'
                        os.makedirs(dirs_dist, exist_ok=True)
                        # download file
                        request = requests.get(
                            url_downloaded,
                            stream=True,
                            verify=False,
                            cookies=session.cookies,
                            allow_redirects=True,
                        )
                        txt = BeautifulSoup(
                            request.content, "lxml")

                        file_name = f'{dirs_dist}/{l["batch_id"]}.{docs[3]}'
                        # Check if file exists
                        if os.path.exists(file_name):
                            ## Remove when file exists
                            os.remove(file_name)

                        ## Append TXT to TXT file
                        f = open(file_name,mode="a",encoding="ascii",newline="\r\n")
                        for p in txt:
                            f.write(p.text)
                        f.close()
    ## Step 3 LogOut
    time.sleep(5)
    response = requests.request("GET",f"{API_HOST}?operation=LOGOFF",verify=False,timeout=3,cookies=session.cookies)
    print(response.status_code)
    session.close()

if __name__ == "__main__":
    main()
    sys.exit(0)