import requests


def result(token, topicid) -> list:
    headers = {
        "Host": "api.eksisozluk.com",
        "Client-Secret": "eabb8841-258d-4561-89a6-66c6501dee83",
        "Content-Type": "application/json; charset=UTF-8",
        "User-Agent": "okhttp/3.12.1",
        "Authorization": "Bearer " + token,
    }
    url = "https://api.eksisozluk.com/v2/topic/" + str(topicid)
    resp = requests.request("GET", url, headers=headers).json()

    return resp["Data"]


# print(
#     result(
#         "J3Wu9CPbDsy5C3WUhKZKj_wYgfjWVIE9Hb0K_BbSGjjH0y3R41oVoWzTAd0LW5jXyeD34uIgWs9JE-OfUc-Ees-m478_VN9yIZf0n4pLPgMTwVNlBRRokWbpx5zvN0sae4V3raEhCh-2He0vEGOG7PK8OEgEtnR8ZEb0UDFsidtDvdeWFf4t8fYj_UJ62T0ccehEPDMt5xx5eU1RDqfHSA",
#         7250896,
#     )
# )
