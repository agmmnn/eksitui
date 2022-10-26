import requests
from datetime import date

# https://api.eksisozluk.com/v2/entry/1
# https://api.eksisozluk.com/v2/topic/7006370
# https://api.eksisozluk.com/v2/topic/7006370?p=4
# https://api.eksisozluk.com/v2/topic/6886221/popular?p=1
# https://api.eksisozluk.com/v2/topic/6886221/today?day=2022-11-05&p=1
def result(token: str, topic_tip: str, id, categ: str = "", page: int = 1) -> dict:
    params_dict = {"day": str(date.today()), "p": page}
    headers = {
        "Host": "api.eksisozluk.com",
        "Client-Secret": "eabb8841-258d-4561-89a6-66c6501dee83",
        "Content-Type": "application/json; charset=UTF-8",
        "User-Agent": "okhttp/3.12.1",
        "Authorization": "Bearer " + token,
    }
    url = (
        f"https://api.eksisozluk.com/v2/{topic_tip}/"
        + str(id)
        + ("/" + categ if topic_tip == "topic" and categ else "")
    )
    resp = requests.request(
        "GET",
        url,
        headers=headers,
        params=params_dict if topic_tip == "topic" else "",
    )
    print(resp.url)
    return resp.json()["Data"]
