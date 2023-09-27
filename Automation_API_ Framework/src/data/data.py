import json
import os


class Data:
    def __init__(self, file: str = 'dev'):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'{file}.json')) as json_file:
            for k, v in json.load(json_file).items():
                self.__setattr__(k, v)


data = Data()

