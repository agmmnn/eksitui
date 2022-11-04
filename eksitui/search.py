import requests


def result(token, term) -> list:
    headers = {
        "Host": "api.eksisozluk.com",
        "Client-Secret": "eabb8841-258d-4561-89a6-66c6501dee83",
        "Content-Type": "application/json; charset=UTF-8",
        "User-Agent": "okhttp/3.12.1",
        "Authorization": "Bearer " + token,
    }
    url = f"https://api.eksisozluk.com/v2/topic/query/?term={term}"
    resp = requests.request("GET", url, headers=headers).json()
    return resp["Data"]["QueryData"]["TopicId"]
