import requests


def result(token) -> list:
    body = '{"Filters":[{"channelId":1,"channelName":"spor","enabled":true},{"channelId":2,"channelName":"siyaset","enabled":true},"channelId":4,"channelName":"anket","enabled":true},{"channelId":5,"channelName":"ilixc5x9fkiler","enabled":true},{"channelId":10,channelName":"ekxc5x9fi-sxc3xb6zlxc3xbck","enabled":false},{"channelId":11,"channelName":"yetixc5x9fkin","enabled":false},"channelId":39,"channelName":"troll","enabled":false}]}'
    headers = {
        "Host": "api.eksisozluk.com",
        "Client-Secret": "eabb8841-258d-4561-89a6-66c6501dee83",
        "Content-Type": "application/json; charset=UTF-8",
        "User-Agent": "okhttp/3.12.1",
        "Authorization": "Bearer " + token,
    }
    url = "https://api.eksisozluk.com/v2/index/popular/?p=1"
    resp = requests.request("POST", url, data=body, headers=headers).json()

    return [
        [f'{i["Title"]} [i]({str(i["MatchedCount"])})[/i]', str(i["TopicId"])]
        for i in resp["Data"]["Topics"]
    ]
