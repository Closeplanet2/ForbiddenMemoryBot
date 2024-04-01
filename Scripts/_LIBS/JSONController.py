from Scripts._LIBS.RequestController import RequestController
import json
import os
import requests

class JSONController:
    def dump_webpage_to_json(self, dir_path, file_name, webpage_url, external_key=None):
        external_webpage = RequestController().pull_website(webpage_url=webpage_url)
        json_webpage = json.loads(external_webpage.text)
        if not external_key is None:
            json_webpage = json.loads(external_webpage.text)[external_key]
        self.dump_dict_to_json(dir_path, file_name, json_webpage)

    def dump_dict_to_json(self, dict, file, overwrite):
        if dict is None: return
        if os.path.exists(file) and overwrite: os.remove(file)
        with open(file, 'w') as fp:
            json.dump(dict, fp)

    def return_dict_from_json(self, file, overwrite):
        if not os.path.exists(file):
            self.dump_dict_to_json(dict={}, file=file, overwrite=overwrite)
            return {}
        with open(file, "r") as json_file:
            return json.load(json_file)

    def return_page_as_json(self, website_url):
        request = requests.get(website_url, headers={'Accept': 'application/json'})
        return request.json()