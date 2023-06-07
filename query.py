import json
import aiohttp
import asyncio

class Query():
    def __init__(self, query_json_path, *args, **kwargs):
        with open(query_json_path, 'r') as f:
            query_obj = json.load(f)

            for k,v in query_obj.items():
                setattr(self, k, v)

        self.fill_query(*args, **kwargs)

    def fill_query(self, *args, **kwargs):
        pass

    async def fetch(self, session):
        data = getattr(self, 'data', {})
            
        async with session.request(self.method, self.url, data=json.dumps(data)) as response:
            self.response_headers = response.headers
            json_result = await response.json()

            return json_result

class StoneQuery(Query):
    def __init__(self, id1, id2):
        super().__init__('queries/auction_search_stones.json', id1, id2)

    def fill_query(self, *args, **kwargs):
        id1, id2 = args
        self.data["EtcOptions"][0]["SecondOption"] = id1
        self.data["EtcOptions"][1]["SecondOption"] = id2

class AuctionOptionsQuery(Query):
    def __init__(self):
        super().__init__('queries/auction_options.json')