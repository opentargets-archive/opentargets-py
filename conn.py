import json
import logging
from collections import namedtuple
from itertools import islice

import requests
from cachecontrol import CacheControl
from hyper.contrib import HTTP20Adapter
import time
import namedtupled
from future.utils import implements_iterator



VERSION=1.2

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

class HTTPMethods(object):
    GET='GET'
    POST='POST'
    HEAD='HEAD'
    PUT='PUT'
    DELETE='DELETE'

def result_to_json(result, **kwargs):
    '''transforms a result back to json. kwargs will be passed to json.dumps'''
    return json.dumps(result._asdict(), **kwargs)

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

    def __str__(self):
        data = str(self.data)
        return data[:100] + (data[100:] and '...')


    def _parse_usage_data(self):
        if 'X-Usage-Limit-1h' in self._headers:
            UL1H = 'X-Usage-Limit-1h'
            UL10S = 'X-Usage-Limit-10s'
            UR1H = 'X-Usage-Remaining-1h'
            UR10S = 'X-Usage-Remaining-10s'
        elif b'X-Usage-Limit-1h' in self._headers:
            UL1H = b'X-Usage-Limit-1h'
            UL10S = b'X-Usage-Limit-10s'
            UR1H = b'X-Usage-Remaining-1h'
            UR10S = b'X-Usage-Remaining-10s'
        else:
            self.usage = None
            return

        usage = dict(limit={'hour': int(self._headers[UL1H]),
                            'seconds_10': int(self._headers[UL10S]),
                            },
                     remaining = {'hour': int(self._headers[UR1H]),
                                  'seconds_10': int(self._headers[UR10S]),
                                  },
                     )
        usage['remaining']['minimum'] =min((usage['remaining']['hour'], usage['remaining']['seconds_10']))

        usage['exceeded'] = usage['remaining']['minimum'] < 0
        self.usage = self._dict_to_nested_namedtuple(usage, classname='UsageInfo')
        if self.usage.exceeded:
            self._logger.warning('Fair Usage limit exceeded')
    def __len__(self):
        try:
            return self.info.total
        except:
            return len(self.data)


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
                 use_http2=False,
                 ):
        self._logger = logging.getLogger(__name__)
        self.host = host
        self.port = port
        self.api_version = api_version
        self.auth_app_name = auth_app_name
        self.auth_secret = auth_secret
        self.token = None
        self.use_http2 = use_http2
        session= requests.Session()
        if self.use_http2:
            session.mount(host, HTTP20Adapter())
        self.session = CacheControl(session)
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

        'order params to allow efficient caching'
        if params is not None:
            if isinstance(params, dict):
                params = sorted(params.items())
            else:
                params = sorted(params)

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

    def close(self):
        self.session.close()

@implements_iterator
class IterableResult(object):
    '''
    proxy over the Connection class that allows to iterate over all the items returned from a query making multiple calls to the backend in API background
    '''
    def __init__(self, conn, method = HTTPMethods.GET):
        self.conn = conn
        self.method = method

    def __call__(self, *args, **kwargs):

        self._args = args
        self._kwargs = kwargs
        response = self._make_call()
        self.info = response.info
        self._data = response.data
        self.current = 0
        try:
            self.total = int(self.info.total)
        except:
            self.total = len(self._data)



    def _make_call(self):
        if self.method == HTTPMethods.GET:
            return self.conn.get(*self._args, **self._kwargs)
        elif self.method == HTTPMethods.POST:
            return self.conn.post(*self._args, **self._kwargs)
        else:
            raise AttributeError("HTTP method {} is not supported".format(self.method))

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.total:
            if not self._data:
                self._kwargs['from'] = self.current
            self._data = self._make_call().data
            d = self._data.pop(0)
            self.current+=1
            return d
        else:
            raise StopIteration()

    def __len__(self):
        try:
            return self.total
        except:
            return 0

    def __bool__(self):
        return self.__len__() >0

    def __nonzero__(self):
        return self.__bool__()

    def __str__(self):
        data = str(self._data)
        return data[:100] + (data[100:] and '...')

    def __getitem__(self, x):
        if type(x) is slice:
            return list(islice(self, x.start, x.stop, x.step))
        else:
            return next(islice(self, x, None), None)


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