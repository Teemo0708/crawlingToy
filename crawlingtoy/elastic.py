import requests

class ElasticPost(object):
    def __init__(self, host, port, index):
        self.host = host
        self.port = port
        self.index = index

    def sendPost(self, json_data: dict):
        headers = {'Content-Type': 'application/json'}
        
        return requests.post(
            f'http://{self.host}:{self.port}/{self.index}/_doc/',
            headers=headers,
            verify=False,
            json=json_data
        ).status_code   