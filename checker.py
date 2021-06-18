import os
import requests
import proxygen
from itertools import cycle

current_path = os.path.dirname(os.path.realpath(__file__))
url = "https://discordapp.com/api/v6/users/@me/library"

proxies = proxygen.get_proxies()
proxy_pool = cycle(proxies)


def check(filename):
    f = open(current_path + "/" + "workingtokens.txt", "w")
    f.close()
    with open(current_path + "/" + filename) as f:
        tokens = []
        for line in f.read().splitlines():  # read rest of lines
            tokens.append(line)

    for token in tokens:
        proxy = 'http://' + next(proxy_pool)
        header = {
            "Content-Type": "application/json",
            "authorization": token
        }
        try:
            print(token)
            r = requests.get(url, headers=header, proxies={"http": proxy})
            if r.status_code == 200:
                print(u"\u001b[32;1m[+] Token Works!\u001b[0m")
                with open(current_path + "/" + "workingtokens.txt", "a") as f:
                    f.write(token + "\n")
            elif "rate limited." in r.text:
                print("[-] You are being rate limited.")
            else:
                print(u"\u001b[31m[-] Invalid Token.\u001b[0m")
        except requests.exceptions.InvalidHeader:
            print(u"\u001b[31m[-] Invalid Token.\u001b[0m")
    print("Successfully")
