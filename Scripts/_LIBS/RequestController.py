import requests

class RequestController:
    def download_image(self, image_url, save_path, verify=True):
        pull_image = requests.get(image_url, verify=verify)
        with open(save_path, 'wb') as handler:
            handler.write(pull_image.content)

    def pull_website(self, webpage_url):
        return requests.get(webpage_url)