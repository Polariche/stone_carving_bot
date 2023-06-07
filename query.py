import json
import aiohttp
import asyncio

class Query():
    def __init__(self, query_json_path, **query_kwargs):
        with open(query_json_path, 'r') as f:
            query_obj = json.load(f)

            for k,v in query_obj.items():
                setattr(self, k, v)

        self.fill_query(**query_kwargs)

    def fill_query(self, **query_kwargs):
        pass

    async def fetch(self, session):
        if self.method == "GET":
            f = session.get
        elif self.method == "POST":
            f = session.post 

        data = getattr(self, 'data', {})
            
        async with f(self.url, data=json.dumps(data)) as response:
            self.response_headers = response.headers
            json_result = await response.json()

            return json_result

class StoneQuery(Query):
    def __init__(self, **query_kwargs):
        super().__init__('queries/auction_search_stones.json', **query_kwargs)

    def fill_query(self, **query_kwargs):
        engraves = query_kwargs["engraves"]
        self.data["EtcOptions"][0]["SecondOption"] = engraves[0]
        self.data["EtcOptions"][1]["SecondOption"] = engraves[1]

class AuctionOptionsQuery(Query):
    def __init__(self):
        super().__init__('queries/auction_options.json')


with open("tokens/smilegate.token", "r") as f:
    key = f.readlines()[0]

async def client():
    headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json',
                    'authorization': f'bearer {key}'
                }

    async with aiohttp.ClientSession(headers=headers) as session:
        query = StoneQuery(engraves=[118, 299])
        query_result = await query.fetch(session)
        print(query_result)
        print(query.response_headers)

loop = asyncio.get_event_loop()
loop.run_until_complete(client())





