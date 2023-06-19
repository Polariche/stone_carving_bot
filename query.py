import json
import aiohttp
import asyncio
import os

from asyncio import Future

class Query():
    loop = None

    def __init__(self, query_json_path, *args, **kwargs):
        with open(query_json_path, 'r') as f:
            query_obj = json.load(f)

            for k,v in query_obj.items():
                setattr(self, k, v)

        if self.method == "GET":
            self.fill_url(*args, **kwargs)
        elif self.method == "POST":
            self.fill_query(*args, **kwargs)

        if Query.loop is not None:
            self.result = Query.loop.create_future()
        else:
            self.result = None

    def fill_query(self, *args, **kwargs):
        pass

    def fill_url(self, *args, **kwargs):
        pass

    async def fetch(self, session):
        data = getattr(self, 'data', {})
            
        async with session.request(self.method, self.url, data=json.dumps(data)) as response:
            self.response_headers = response.headers
            json_result = await response.json()

            if self.result is not None:
                self.result.set_result(json_result)

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

class MarketItemsQuery(Query):
    def __init__(self, item_id):
        super().__init__('queries/market_items.json',  str(item_id))

    def fill_url(self, *args, **kwargs):
        self.url=os.path.join(self.url, args[0])

class GemQuery(Query):
    def __init__(self, level, gem_type):
        super().__init__('queries/auction_search_gems.json', level, gem_type)

    def fill_query(self, *args, **kwargs):
        level, gem_type = args
        self.data["ItemName"] = f"{level}레벨 {gem_type}"