import requests
from dataclasses import asdict, replace
from .models import User


class ApiClient():
    def __init__(self, api_url):
        self.URL = api_url

    def api_request(self, method, path, **kwargs):
        url = self.URL + path
        resp = getattr(requests, method)(url, **kwargs)
        if resp.status_code in [200, 201]:
            return resp.json()
        elif resp.status_code == 404:
            return None
        else:
            print(resp.json())

    def get_object(self, obj_class, id, **kwargs):
        if obj_class == User:
            path = obj_class._endpoint
            response_data = self.api_request(
                'get', path, params={'messenger_id': id})
            if response_data and type(response_data) == list:
                response_data = response_data[0]
        else:
            path = obj_class._endpoint + str(id)
            response_data = self.api_request('get', path)
        if response_data:
            return obj_class(**response_data)

    def save_object(self, obj):
        path = obj._endpoint
        data = asdict(obj)
        if obj.id:
            path += str(obj.id)
            response_data = self.api_request('put', path, json=data)
        else:
            response_data = self.api_request('post', path, json=data)
        obj = replace(obj, **response_data)
        return obj
