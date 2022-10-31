class TopicList(Widget):
    async def topic_list(self, message: Input.Changed) -> None:
        """A coroutine to handle a text changed message."""
        if message.value:
            # Look up the word in the background
            asyncio.create_task(self.lookup_word(message.value))
        else:
            # Clear the results
            self.query_one("#results", Static).update()

    async def lookup_topics(self, word: str) -> None:
        """Looks up a word."""
        body = """{"Filters":[{"channelId":1,"channelName":"spor","enabled":true},{"channelId":2,"channelName":"siyaset","enabled":true},{"channelId":4,"channelName":"anket","enabled":true},{"channelId":5,"channelName":"ilixc5x9fkiler","enabled":true},{"channelId":10,"channelName":"ekxc5x9fi-sxc3xb6zlxc3xbck","enabled":false},{"channelId":11,"channelName":"yetixc5x9fkin","enabled":false},{"channelId":39,"channelName":"troll","enabled":false}]}"""
        headers = {
            "Host": "api.eksisozluk.com",
            "Client-Secret": "eabb8841-258d-4561-89a6-66c6501dee83",
            "Content-Type": "application/json; charset=UTF-8",
            "Authorization": "Bearer J3Wu9CPbDsy5C3WUhKZKj_wYgfjWVIE9Hb0K_BbSGjjH0y3R41oVoWzTAd0LW5jXyeD34uIgWs9JE-OfUc-Ees-m478_VN9yIZf0n4pLPgMTwVNlBRRokWbpx5zvN0sae4V3raEhCh-2He0vEGOG7PK8OEgEtnR8ZEb0UDFsidtDvdeWFf4t8fYj_UJ62T0ccehEPDMt5xx5eU1RDqfHSA",
        }
        url = "https://api.eksisozluk.com/v2/index/popular/?p=1"
        async with httpx.AsyncClient() as client:
            results = (await client.post(url, data=body, headers=headers)).json()

        # if word == self.query_one(Input).value:
        #     markdown = self.make_word_markdown(results)
        #     self.query_one("#results", Static).update(Markdown(markdown))
        gundem = results["Data"]["Topics"][0]
