import json
import os
import requests

class JSONController:
    def dump_dict_to_json(self, dict, file, overwrite):
        if dict is None: return
        if os.path.exists(file) and overwrite: os.remove(file)
        with open(file, 'w') as fp:
            json.dump(dict, fp)

    def return_dict_from_json(self, file):
        if not os.path.exists(file): return None
        with open(file, "r") as json_file:
            return json.load(json_file)

    def return_page_as_json(self, website_url):
        request = requests.get(website_url, headers={'Accept': 'application/json'})
        return request.json()