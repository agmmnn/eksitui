import requests


def result(token, tip) -> list:
    body = '{"Filters":[{"channelId":1,"channelName":"spor","enabled":true},{"channelId":2,"channelName":"siyaset","enabled":true},"channelId":4,"channelName":"anket","enabled":true},{"channelId":5,"channelName":"ilixc5x9fkiler","enabled":true},{"channelId":10,channelName":"ekxc5x9fi-sxc3xb6zlxc3xbck","enabled":true},{"channelId":11,"channelName":"yetixc5x9fkin","enabled":true},"channelId":39,"channelName":"troll","enabled":true}]}'
    headers = {
        "Host": "api.eksisozluk.com",
        "Client-Secret": "eabb8841-258d-4561-89a6-66c6501dee83",
        "Content-Type": "application/json; charset=UTF-8",
        "User-Agent": "okhttp/3.12.1",
        "Authorization": "Bearer " + token,
    }
    url = f"https://api.eksisozluk.com/v2/index/{tip}/?p=1"
    if tip == "popular":
        resp = requests.request("POST", url, data=body, headers=headers).json()
    else:
        resp = requests.request("GET", url, data=body, headers=headers).json()

    if tip == "debe":
        return [[i["Title"], str(i["EntryId"])] for i in resp["Data"]["DebeItems"]]
    return [
        [f'{i["Title"]} [cyan italic]({str(i["MatchedCount"])})[/]', str(i["TopicId"])]
        for i in resp["Data"]["Topics"]
    ]
