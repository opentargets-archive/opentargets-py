import json
import logging
from collections import namedtuple
import requests
from  httpcache import CachingHTTPAdapter
import time
import namedtupled


VERSION=1.2

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

class Response(object):
    ''' Handler for responses from the api'''

    def __init__(self, response, content_type = 'json'):
        self._logger =logging.getLogger(__name__)
        if content_type == 'json':
            parsed_response = response.json()
            if isinstance(parsed_response, dict):
                self.data = [self._dict_to_namedtuple(e) for e in parsed_response['data']]
                del parsed_response['data']
                if 'from' in parsed_response:
                    parsed_response['from_'] = parsed_response['from']
                    del parsed_response['from']
                self.info = self._dict_to_namedtuple(parsed_response, classname='ResultInfo')

            else:
                self.data = parsed_response
            self._headers = response.headers
            self._parse_usage_data()

        else:
            raise AttributeError("content-type not supported")

    @staticmethod
    def _dict_to_namedtuple(d, classname ='Result', rename = True):
        return namedtuple(classname, d.keys(),rename=rename)(*d.values())

    @staticmethod
    def _dict_to_nested_namedtuple(d, classname ='Result', ):
        return namedtupled.map(d,classname)


    def _parse_usage_data(self):
        usage = dict(limit={'hour': int(self._headers['X-Usage-Limit-1h']),
                            'seconds_10': int(self._headers['X-Usage-Limit-10s']),
                            },
                     remaining = {'hour': int(self._headers['X-Usage-Remaining-1h']),
                                  'seconds_10': int(self._headers['X-Usage-Remaining-10s']),
                                  },
                     )
        usage['remaining']['minimum'] =min((usage['remaining']['hour'], usage['remaining']['seconds_10']))

        usage['exceeded'] = usage['remaining']['minimum'] < 0
        self.usage = self._dict_to_nested_namedtuple(usage, classname='UsageInfo')
        if self.usage.exceeded:
            self._logger.warning('Fair Usage limit exceeded')


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
        self._logger = logging.getLogger(__name__)
        self.host = host
        self.port = port
        self.api_version = api_version
        self.auth_app_name = auth_app_name
        self.auth_secret = auth_secret
        self.token = None
        self.session= requests.Session()
        self.session.mount('http://', CachingHTTPAdapter())
        self.session.mount('https://', CachingHTTPAdapter())
        self._test_version()



    def _build_url(self, endpoint):
        return '{}:{}/api/{}{}'.format(self.host,
                                       self.port,
                                       self.api_version,
                                       endpoint,)

    def get(self, endpoint, params=None):
        return Response(self._make_request(endpoint,
                              params=params,
                              method='GET'))

    def post(self, endpoint, data=None):
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
        return self._make_token_request(expire).data['token']

    def _make_request(self,
                      endpoint,
                      params = None,
                      data = None,
                      method = "GET",
                      token = None,
                      headers = {},
                      rate_limit_fail = False,
                      **kwargs):

        def call():
            return self.session.request(method,
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
                    retry_after = float(response.headers['Retry-After'])/1000.
                    self._logger.warning('Usage allowance hit. Retrying in {} seconds'.format(retry_after))
                    time.sleep(retry_after)
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

    def _test_version(self):
        remote_version = self.get('/public/utils/version').data
        if remote_version != VERSION:
            self._logger.warning('The remote server is running the API with version {}, but the client expected {}. They may not be compatible.'.format(remote_version, VERSION))


if __name__=='__main__':
    conn= Connection(host='https://mirror.targetvalidation.org')

    print(conn._build_url('/public/search'))
    '''test cache'''
    for i in range(5):
        start_time = time.time()
        conn.get('/public/search', {'q':'braf'})
        print(time.time()-start_time, 'seconds')
    '''test response'''
    r=conn.get('/public/search', {'q':'braf'})
    print(r.usage.remaining.minimum)
    print(r.info)
    print(r.usage)
    for i,d in enumerate(r.data):
        print(i,d.id, d.type, d.data['approved_symbol'])