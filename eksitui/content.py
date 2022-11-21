import requests

# https://api.eksisozluk.com/v2/topic/7006370
# https://api.eksisozluk.com/v2/topic/7006370?p=4
# https://api.eksisozluk.com/v2/topic/7427856/popular?p=1
# https://api.eksisozluk.com/v2/topic/7427856/today?day=2022-11-05&p=1


def result(token, id, tip) -> list:
    headers = {
        "Host": "api.eksisozluk.com",
        "Client-Secret": "eabb8841-258d-4561-89a6-66c6501dee83",
        "Content-Type": "application/json; charset=UTF-8",
        "User-Agent": "okhttp/3.12.1",
        "Authorization": "Bearer " + token,
    }
    url = (
        f"https://api.eksisozluk.com/v2/{tip}/"
        + str(id)
        + ("/popular?p=1" if tip != "entry" else "")
    )
    resp = requests.request("GET", url, headers=headers).json()

    return resp["Data"]
