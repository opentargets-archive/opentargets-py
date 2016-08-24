import json
import logging
from collections import namedtuple

import requests
import time
from cachetools import cached, LRUCache


class Response(object):
    ''' Handler for responses from the api'''

    def __init__(self, response, content_type = 'json'):
        if content_type == 'json':
            parsed_response = response.json()
            self.data = [self._json_object_hook(e) for e in parsed_response['data']]
            del parsed_response['data']
            if 'from' in parsed_response:
                parsed_response['from_']= parsed_response['from']
            del parsed_response['from']
            self.info = self._json_object_hook(parsed_response, classname = 'ResultInfo')
        else:
            raise AttributeError("content-type not supported")

    @staticmethod
    def _json_object_hook(d, classname = 'Result'):
        return namedtuple(classname, d.keys(),rename=True)(*d.values())

    @staticmethod
    def json2obj(data):
        return json.loads(data, object_hook=Response._json_object_hook)

class Connection(object):
    '''
    Handles connections to the Open Targets REST API
    '''

    _AUTO_GET_TOKEN = 'auto'

    def __init__(self,
                 host='https://www.targetvalidation.org',
                 port=443,
                 api_version='latest',
                 auth_app_name = None,
                 auth_secret = None,
                 ):
        self.host = host
        self.port = port
        self.api_version = api_version
        self.auth_app_name = auth_app_name
        self.auth_secret = auth_secret
        self.token = None
        self._cache = LRUCache(maxsize=100)



    def _build_url(self, endpoint):
        return '{}:{}/api/{}{}'.format(self.host,
                                       self.port,
                                       self.api_version,
                                       endpoint,)

    def get(self, endpoint, params):
        return Response(self._make_request(endpoint,
                              params=params,
                              method='GET'))

    def post(self, endpoint, data):
        return Response(self._make_request(endpoint,
                               data=data,
                               method='POST'))


    def _make_token_request(self, expire = 10*60):
        return self._make_request('/public/auth/request_token',
                                  data={'app_name':self.auth_app_name,
                                        'secret':self.auth_secret,
                                        'expiry': expire},
                                  )

    def get_token(self, expire = 10*60):
        return json.loads(self._make_token_request(expire).data.decode('utf-8'))['token']

    def _make_request(self,
                      endpoint,
                      params = {},
                      data = {},
                      method = "GET",
                      token = None,
                      headers = {},
                      rate_limit_fail = False,
                      **kwargs):

        def call():
            return requests.request(method,
                                    self._build_url(endpoint),
                                    params = params,
                                    data = data,
                                    headers = headers,
                                    **kwargs)

        if token is not None and token == self._AUTO_GET_TOKEN:
            self._update_token()
            token = self.token
        if token is not None:
            headers['Auth-Token']=token

        response = None
        if not rate_limit_fail:
            status_code = 429
            while status_code == 429:
                response = call()
                status_code = response.status_code
                if status_code == 429:
                    print("TODO: get the right time from the header")
                    time.sleep(1)
        else:
            response = call()

        response.raise_for_status()
        return response

    def _update_token(self):
        if self.token:
            token_valid_response = self._make_request('/public/auth/validate_token',
                                                       headers={'Auth-Token':self.token})
            if token_valid_response.status_code == 200:
                return
            if token_valid_response.status_code == 419:
                pass
        self.token = self.get_token()




if __name__=='__main__':
    conn= Connection()
    print(conn._build_url('/public/search'))
    r=conn.get('/public/search', {'q':'braf'})
    print r.info
    for i,d in enumerate(r.data):
        print (i,d.id, d.type, d.data['approved_symbol'])