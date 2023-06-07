import json
import requests

class Query():
    def __init__(self, url, get_or_post, query_json_path, **query_kwargs):
        self.url = url
        self.get_or_post = get_or_post

        self.query_json_path = query_json_path

        self.query_kwargs = query_kwargs

        self.response_f = {
                'post' : requests.post,
                'get' : requests.get
        }

    def headers(self, key):
        return {
                    'accept': 'application/json',
                    'Content-Type': 'application/json',
                    'authorization': f'bearer {key}'
                }

    def get_query_template(self):
        with open(self.query_json_path, 'r') as f:
            query = json.load(f)

        return query

    def fill_query(self):
        return self.get_query_template()

    def get_response(self, key):
        request_kwargs = {}
        request_kwargs['headers'] = self.headers(key)

        try:
            request_kwargs['data'] = json.dumps(self.fill_query())
        except:
            pass

        response = self.response_f[self.get_or_post](self.url, **request_kwargs)
        return response


class StoneQuery(Query):
    def __init__(self, **query_kwargs):
        super().__init__('https://developer-lostark.game.onstove.com/auctions/items', 
                            'post', 
                            'json/stone_query.json', 
                            **query_kwargs)

    def fill_query(self):
        query = self.get_query_template()

        engraves = self.query_kwargs["engraves"]
        query["EtcOptions"][0]["SecondOption"] = engraves[0]
        query["EtcOptions"][1]["SecondOption"] = engraves[1]

        return query


class AuctionOptionsQuery(Query):
    def __init__(self, **query_kwargs):
        super().__init__('https://developer-lostark.game.onstove.com/auctions/options', 
                            'get', 
                            '', 
                            **query_kwargs)


with open("./smilegate.token", "r") as f:
    key = f.readlines()[0]

print(json.loads(StoneQuery(engraves=[118, 299]).get_response(key).text)['Items'][0])




