import requests


def result() -> str:
    client_secret = "eabb8841-258d-4561-89a6-66c6501dee83"
    client_unique = "1a62383d-742e-4bcf-bf77-2fe1a1edcd39"
    api_secret = "68f779c5-4d39-411a-bd12-cbcc50dc83dd"
    payload = (
        "Platform=g&Version=2.0.0&Build=51&Api-Secret="
        + api_secret
        + "&Client-Secret="
        + client_secret
        + "&ClientUniqueId="
        + client_unique
    )
    headers = {
        "Host": "api.eksisozluk.com",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "184",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "okhttp/3.12.1",
        "Connection": "close",
    }
    url = "https://api.eksisozluk.com/v2/account/anonymoustoken"
    return requests.request("POST", url, headers=headers, data=payload).json()["Data"][
        "access_token"
    ]
