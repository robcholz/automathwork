import argparse
import json
import os

from subject import Subject


def set_http_proxy(address, port):
    os.environ["HTTP_PROXY"] = 'http://127.0.0.1:7890'
    os.environ["HTTPS_PROXY"] = 'https://127.0.0.1:7890'


class Settings:
    def __init__(self):
        self.pandoc_path: str
        self.config_path: str
        parser = argparse.ArgumentParser(description="Water Water WWW.. commandline")
        parser.add_argument("-c", "--config", type=str, help="json configuration directory")
        args = parser.parse_args()
        self.config_path = args.config
        self.pandoc_path = os.path.join(self.config_path, 'pandoc')

        with open(os.path.join(self.config_path, 'config.json'), 'r') as file:
            self.config_data = json.load(file)
        # Access the individual values
        self.api_key = self.config_data['gpt3.5-turbo.key']
        self.proxy_address = self.config_data['proxy.address']
        self.proxy_port = self.config_data['proxy.port']

        # self.set_http_proxy(self.proxy_address,self.proxy_port)
        self.verify_default_subject_name()

    def get_pandoc_path(self):
        return self.pandoc_path

    def get_api_key(self):
        return self.api_key

    def get_default_subject_name(self) -> str:
        return self.config_data['subject.default']

    def verify_default_subject_name(self):
        name = self.get_default_subject_name()
        items = self.get_subject_list()
        flag = False
        random_name = ""
        for item in items:
            if name == item.get_name():
                flag = True
            if not flag:
                random_name = item.get_name()
        if not flag:
            self.set_default_subject(random_name)

    def get_default_subject(self):
        with open(os.path.join(self.config_path, 'subjects.json'), 'r') as file:
            data = json.load(file)
            name = self.get_default_subject_name()
            return Subject(name, data[name])

    def set_default_subject(self, name: str):
        self.config_data['subject.default'] = name
        updated_json_data = json.dumps(self.config_data, indent=2)
        with open(os.path.join(self.config_path, 'config.json'), "w") as file:
            file.write(updated_json_data)
            file.flush()

    def get_subject_list(self):
        subjects = []
        with open(os.path.join(self.config_path, 'subjects.json'), 'r') as file:
            data = json.load(file)
            for name, fields in data.items():
                subjects.append(Subject(name, fields))
        return subjects
