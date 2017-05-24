"""
This module abstracts the connection to the Open Targets REST API to simplify its usage.
Can be used directly but requires some knowledge of the API.
"""
import gzip
import json
import logging
from collections import namedtuple
from itertools import islice
from json import JSONEncoder
import collections
import requests
from cachecontrol import CacheControl
from hyper.contrib import HTTP20Adapter
from h2.utilities import CONNECTION_HEADERS as INVALID_HTTP2_HEADERS
import time
from future.utils import implements_iterator
import yaml
from requests.packages.urllib3.exceptions import MaxRetryError
from opentargets import __version__

try:
    import pandas
    pandas_available = True
except ImportError:
    pandas_available = False

try:
    import xlwt
    xlwt_available = True
except ImportError:
    xlwt_available = False

try:
    from tqdm import tqdm
    tqdm_available = True
except ImportError:
    tqdm_available = False

API_MAJOR_VERSION='2.'

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

def flatten(d, parent_key='', separator='.'):
    """
    Takes a nested dictionary as input and generate a flat one with keys separated by the separator

    Args:
        d (dict): dictionary
        parent_key (str): a prefix for all flattened keys
        separator (str): separator between nested keys

    Returns:
        dict: a flattened dictionary
    """
    flat_fields = []
    for k, v in d.items():
        flat_key = parent_key + separator + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            flat_fields.extend(flatten(v, flat_key, separator=separator).items())
        else:
            flat_fields.append((flat_key, v))
    return dict(flat_fields)

def compress_list_values(d, sep='|'):
    """
    Args:
        d (dict): dictionary
        sep (str): separator char used to join list element

    Returns:
        dict: dictionary with compressed lists
    """
    for k, v in d.items():
        if not isinstance(v, (str, int, float)):
            if isinstance(v, collections.Sequence):
                safe_values = []
                for i in v:
                    if isinstance(i, (str, int, float)):
                        safe_values.append(str(i))
                    else:
                        safe_values.append(json.dumps(i))
                d[k]=sep.join(safe_values)
    return d


def dict_to_namedtuple(d, named_tuple_class_name='Result', rename=True):
    """
    Converts a dictionary to a namedtuple
    Args:
        d (dict): dictionary
        named_tuple_class_name: Name of the namedtuple class
        rename (bool): rename unsafe fields. Defaults to True

    Returns:
        namedtuple: the converted namedtuple
    """
    return namedtuple(named_tuple_class_name, d.keys(), rename=rename)(*d.values())


def dict_to_nested_namedtuple(d, named_tuple_class_name='Result' ):
    """
        Recursively converts a dictionary to a namedtuple
        Args:
            d (dict): dictionary
            named_tuple_class_name: Name of the namedtuple class

        Returns:
            namedtuple: the converted namedtuple
        """
    for key, value in d.items():
        if isinstance(value, dict):
            d[key] = dict_to_nested_namedtuple(value, named_tuple_class_name = named_tuple_class_name)
    return namedtuple(named_tuple_class_name, d.keys())(**d)


class HTTPMethods(object):
    GET='get'
    POST='post'


class Response(object):
    """
    Handler for responses coming from the api
    """

    def __init__(self, response):
        """

        Args:
            response: a response coming from a requests call
            content_type (str): content type of the response
        """
        self._logger =logging.getLogger(__name__)
        try:
            parsed_response = response.json()
            if isinstance(parsed_response, dict):
                if 'data' in parsed_response:
                    self.data = parsed_response['data']
                    del parsed_response['data']
                else:
                    self.data = []
                if 'from' in parsed_response:
                    parsed_response['from_'] = parsed_response['from']
                    del parsed_response['from']
                self.info = dict_to_namedtuple(parsed_response, named_tuple_class_name='ResultInfo')

            else:
                self.data = parsed_response
                self.info = {}


        except ValueError:
            self.data = response.text
            self.info = {}

        self._headers = response.headers
        self._parse_usage_data()

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
        self.usage = dict_to_nested_namedtuple(usage, named_tuple_class_name='UsageInfo')
        if self.usage.exceeded:
            self._logger.warning('Fair Usage limit exceeded')
    def __len__(self):
        try:
            return self.info.total
        except:
            return len(self.data)


class Connection(object):
    """
    Handler for connection and calls to the Open Targets Validation Platform REST API
    """

    _AUTO_GET_TOKEN = 'auto'

    def __init__(self,
                 host='https://www.targetvalidation.org',
                 port=443,
                 api_version='latest',
                 auth_app_name = None,
                 auth_secret = None,
                 use_http2=False,
                 ):
        """
        Args:
            host (str): host serving the API
            port (int): port to use for connection to the API
            api_version (str): api version to point to, default to 'latest'
            auth_app_name (str): app_name if using authentication
            auth_secret (str): secret if using authentication
            use_http2 (bool): use http2 client
        """
        self._logger = logging.getLogger(__name__)
        self.host = host
        self.port = str(port)
        self.api_version = api_version
        self.auth_app_name = auth_app_name
        self.auth_secret = auth_secret
        if self.auth_app_name and self.auth_secret:
            self.use_auth = True
        else:
            self.use_auth = False
        self.token = None
        self.use_http2 = use_http2
        session= requests.Session()
        if self.use_http2:
            session.mount(host, HTTP20Adapter())
        self.session = CacheControl(session)
        self._get_remote_api_specs()



    def _build_url(self, endpoint):
        return '{}:{}/api/{}{}'.format(self.host,
                                       self.port,
                                       self.api_version,
                                       endpoint,)
    @staticmethod
    def _auto_detect_post(params):
        """
        Determine if a post request should be made instead of a get depending on the size of the parameters
        in the request.

        Args:
            params (dict): params to pass in the request

        Returns:
            Boolean: True if post is needed
        """
        if params:
            for k,v in params.items():
                if isinstance(v, (list, tuple)):
                    if len(v)>3:
                        return True
        return False

    def get(self, endpoint, params=None):
        """
        makes a GET request
        Args:
            endpoint (str): REST API endpoint to call
            params (dict): request payload

        Returns:
            Response: request response
        """
        if self._auto_detect_post(params):
            self._logger.debug('switching to POST due to big size of params')
            return self.post(endpoint, data=params)
        return Response(self._make_request(endpoint,
                              params=params,
                              method='GET'))

    def post(self, endpoint, data=None):
        """
        makes a POST request
        Args:
            endpoint (str): REST API endpoint to call
            data (dict): request payload

        Returns:
            Response: request response
        """
        return Response(self._make_request(endpoint,
                               data=data,
                               method='POST'))


    def _make_token_request(self, expire = 60):
        """
        Asks for a token to the API
        Args:
            expire (int): expiration time for the token

        Returns:
            response for the get token request
        """
        return self._make_request('/public/auth/request_token',
                                  params={'app_name':self.auth_app_name,
                                        'secret':self.auth_secret,
                                        'expiry': expire},
                                  headers={'Cache-Control':'no-cache',}
                                  )

    def get_token(self, expire = 60):
        """
        Asks for a token to the API
        Args:
            expire (int): expiration time for the token

        Returns:
            str: the token served by the API
        """
        response = self._make_token_request(expire)
        return response.json()['token']

    def _make_request(self,
                      endpoint,
                      params = None,
                      data = None,
                      method = HTTPMethods.GET,
                      headers = {},
                      rate_limit_fail = False,
                      **kwargs):
        """
        Makes a request to the REST API
        Args:
            endpoint (str): endpoint of the REST API
            params (dict): payload for GET request
            data (dict): payload for POST request
            method (HTTPMethods): request method, either HTTPMethods.GET or HTTPMethods.POST. Defaults to HTTPMethods.GET
            headers (dict): HTTP headers for the request
            rate_limit_fail (bool): If True raise exception when usage limit is exceeded. If False wait and
                retry the request. Defaults to False.
        Keyword Args:
            **kwargs: forwarded to requests

        Returns:
            a response from requests
        """

        def call():
            headers['User-agent']='Open Targets Python Client/%s'%str(__version__)
            if self.use_http2 and set(headers.keys())&INVALID_HTTP2_HEADERS:
                for h in INVALID_HTTP2_HEADERS:
                    if h in headers:
                        del headers[h]
            return self.session.request(method,
                                    self._build_url(endpoint),
                                    params = params,
                                    json = data,
                                    headers = headers,
                                    **kwargs)

        'order params to allow efficient caching'
        if params is not None:
            if isinstance(params, dict):
                params = sorted(params.items())
            else:
                params = sorted(params)

        if self.use_auth and not 'request_token' in endpoint:
            if self.token is None:
                self._update_token()
            if self.token is not None:
                headers['Auth-Token']=self.token

        response = None
        default_retry_after = 5
        if not rate_limit_fail:
            status_code = 429
            while status_code in [429,419]:
                try:
                    response = call()
                    status_code = response.status_code
                    if status_code == 429:
                        retry_after=default_retry_after
                        if 'Retry-After' in response.headers:
                            retry_after = float(response.headers['Retry-After'])
                        self._logger.warning('Maximum usage limit hit. Retrying in {} seconds'.format(retry_after))
                        time.sleep(retry_after)
                    elif status_code == 419:
                        self._update_token(force = True)
                        headers['Auth-Token'] = self.token
                        time.sleep(0.5)
                except MaxRetryError as e:
                    self._logger.exception(e.args[0].reason)
                    self._logger.warning('Problem connecting to the remote API. Retrying in {} seconds'.format(default_retry_after))
                    time.sleep(default_retry_after)
                except OSError as e:
                    self._logger.exception(str(e))
                    self._logger.warning('Problem connecting to the remote API. Retrying in {} seconds'.format(default_retry_after))
                    time.sleep(default_retry_after)


        else:
            response = call()

        response.raise_for_status()
        return response

    def _update_token(self, force = False):
        """
        Update token when expired
        """
        if self.token and not force:
            token_valid_response = self._make_request('/public/auth/validate_token',
                                                       headers={'Auth-Token':self.token})
            if token_valid_response.status_code == 200:
                return
            elif token_valid_response.status_code == 419:
                pass
            else:
                token_valid_response.raise_for_status()

        self.token = self.get_token()

    def _get_remote_api_specs(self):
        """
        Fetch and parse REST API documentation
        """
        r= self.session.get(self.host+':'+self.port+'/api/docs/swagger.yaml')
        r.raise_for_status()
        self.swagger_yaml = r.text
        self.api_specs = yaml.load(self.swagger_yaml)
        self.endpoint_validation_data={}
        for p, data in self.api_specs['paths'].items():
            p=p.split('{')[0]
            if p[-1]== '/':
                p=p[:-1]
            self.endpoint_validation_data[p] = {}
            for method, method_data in data.items():
                if 'parameters' in method_data:
                    params = {}
                    for par in method_data['parameters']:
                        par_type = par.get('type', 'string')
                        params[par['name']]=par_type
                    self.endpoint_validation_data[p][method] = params

        remote_version = self.get('/public/utils/version').data
        if remote_version.startswith(API_MAJOR_VERSION):
            self._logger.warning('The remote server is running the API with version {}, but the client expected this major version {}. They may not be compatible.'.format(remote_version, API_MAJOR_VERSION))

    def validate_parameter(self, endpoint, filter_type, value, method=HTTPMethods.GET):
        """
        Validate payload to send to the REST API based on info fetched from the API documentation

        Args:
            endpoint (str): endpoint of the REST API
            filter_type (str): the parameter sent for the request
            value: the value sent for the request
            method (HTTPMethods): request method, either HTTPMethods.GET or HTTPMethods.POST. Defaults to HTTPMethods.GET
        Raises
            AttributeError: if validation is not passed

        """
        endpoint_data = self.endpoint_validation_data[endpoint][method]
        if filter_type in endpoint_data:
            if endpoint_data[filter_type] == 'string' and isinstance(value, str):
                return
            elif endpoint_data[filter_type] == 'boolean' and isinstance(value, bool):
                return
            elif endpoint_data[filter_type] == 'number' and isinstance(value, (int, float)):
                return

        raise AttributeError('{}={} is not a valid parameter for endpoint {}'.format(filter_type, value, endpoint))

    def api_endpoint_docs(self, endpoint):
        """
        Returns the documentation available for a given REST API endpoint

        Args:
            endpoint (str): endpoint of the REST API

        Returns:
            dict: documentation for the endpoint parsed from YAML docs
        """
        return self.api_specs['paths'][endpoint]

    def get_api_endpoints(self):
        """
        Get a list of available endpoints

        Returns:
            list: available endpoints
        """
        return self.api_specs['paths'].keys()

    def close(self):
        """
        Close connection to the REST API
        """
        self.session.close()

    def ping(self):
        """
        Pings the API as a live check
        Returns:
            bool: True if pinging the raw response as a ``str`` if the API has a non standard name
        """
        response = self.get('/public/utils/ping')
        if response.data=='pong':
            return True
        elif response.data:
            return response.data
        return False

@implements_iterator
class IterableResult(object):
    '''
    Proxy over the Connection class that allows to iterate over all the items returned from a quer.
    It will automatically handle making multiple calls for pagination if needed.
    '''
    def __init__(self, conn, method = HTTPMethods.GET):
        """
        Requires a Connection
        Args:
            conn (Connection): a Connection instance
            method (HTTPMethods): HTTP method to use for the calls
        """
        self.conn = conn
        self.method = method

    def __call__(self, *args, **kwargs):
        """
        Allows to set parameters for calls to the REST API
        Args:
            *args: stored internally
        Keyword Args:
            **kwargs: stored internally

        Returns:
            IterableResult: returns itself
        """
        self._args = args
        self._kwargs = kwargs
        response = self._make_call()
        self.info = response.info
        self._data = response.data
        self.current = 0
        try:
            self.total = int(self.info.total)
            if 'size' in self.info._fields and  'size' not in self._kwargs:
                self._kwargs['size']=1000
        except:
            self.total = len(self._data)
        return self

    def filter(self, **kwargs):
        """
        Applies a set of filters to the current query
        Keyword Args
            **kwargs: passed to the REST API
        Returns:
            IterableResult: an IterableResult with applied filters
        """
        if kwargs:
            for filter_type, filter_value in kwargs.items():
                self._validate_filter(filter_type, filter_value)
                self._kwargs[filter_type] = filter_value
            self.__call__(*self._args, **self._kwargs)
        return self


    def _make_call(self):
        """
        makes calls to the REST API
        Returns:
            Response: response for a call
        Raises:
            AttributeError: if HTTP method is not supported
        """
        if self.method == HTTPMethods.GET:
            return self.conn.get(*self._args, params=self._kwargs)
        elif self.method == HTTPMethods.POST:
            return self.conn.post(*self._args, data=self._kwargs)
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
        try:
            return_str = '{} Results found'.format(self.info.total)
            if  self._kwargs:
                return_str+=' | parameters: {}'.format(self._kwargs)
            return return_str
        except:
            data = str(self._data)
            return data[:100] + (data[100:] and '...')

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, x):
        if type(x) is slice:
            return list(islice(self, x.start, x.stop, x.step))
        else:
            return next(islice(self, x, None), None)

    def _validate_filter(self,filter_type, value):
        """
        validate the provided filter versus the REST API documentation
        Args:
            filter_type (str): filter for the REST API call
            value: the value passed

       Raises
            AttributeError: if validation is not passed

        """
        self.conn.validate_parameter(self._args[0], filter_type, value)

    def to_json(self,iterable=True, **kwargs):
        """

        Args:
            iterable: If True will yield a json string for each result and convert them dinamically as they are
                fetched from the api. If False gets all the results and returns a singl json string.
        Keyword Args:
            **kwargs: forwarded to json.dumps

        Returns:
            an iterator of json strings or a single json string
        """
        if iterable:
            return (json.dumps(i) for i in self)
        return IterableResultSimpleJSONEncoder(**kwargs).encode(self)


    def to_dataframe(self, compress_lists = False,**kwargs):
        """
        Create a Pandas dataframe from a flattened version of the response.

        Args:
            compress_lists: if a value is a list, serialise it to a string with '|' as separator
        Keyword Args:
            **kwargs: forwarded to pandas.DataFrame.from_dict

        Returns:
            pandas.DataFrame: A DataFrame with all the data coming from the query in the REST API
        Notes:
            Requires Pandas to be installed.
        Raises:
            ImportError: if Pandas is not available

        """
        if pandas_available:
            data = [flatten(i) for i in self]
            if compress_lists:
                data = [compress_list_values(i) for i in data]

            return pandas.DataFrame.from_dict(data,  **kwargs)
        else:
            raise ImportError('Pandas library is not installed but is required to create a dataframe')

    def to_csv(self, **kwargs):
        """
        Create a csv file from a flattened version of the response.

        Keyword Args:
            **kwargs: forwarded to pandas.DataFrame.to_csv
        Returns:
            output of pandas.DataFrame.to_csv
        Notes:
            Requires Pandas to be installed.
        Raises:
            ImportError: if Pandas is not available

        """
        return self.to_dataframe(compress_lists=True).to_csv(**kwargs)


    def to_excel(self, excel_writer, **kwargs):
        """
        Create a excel (xls) file from a flattened version of the response.

        Keyword Args:
            **kwargs: forwarded to pandas.DataFrame.to_excel
        Returns:
            output of pandas.DataFrame.to_excel
        Notes:
            Requires Pandas and xlwt to be installed.
        Raises:
            ImportError: if Pandas or xlwt are not available

        """
        if xlwt_available:
            self.to_dataframe(compress_lists=True).to_excel(excel_writer, **kwargs)
        else:
            raise ImportError('xlwt library is not installed but is required to create an excel file')

    def to_namedtuple(self):
        """
        Converts dictionary in the data to namedtuple. Useful for interactive data exploration on IPython
            and similar tools
        Returns:
            iterator: an iterator of namedtupled
        """
        return (dict_to_nested_namedtuple(i, named_tuple_class_name='Data') for i in self)

    def to_file(self, filename, compress=True, progress_bar = False):
        if compress:
            fh = gzip.open(filename, 'wb')
        else:
            fh = open(filename, 'wb')
        if tqdm_available and progress_bar:
            progress = tqdm(desc='Saving entries to file %s'%filename,
                       total=len(self),
                       unit_scale=True)
        for datapoint in self:
            line = json.dumps(datapoint)+'\n'
            fh.write(line.encode('utf-8'))
            if tqdm_available and progress_bar:
                progress.update()
        fh.close()


class IterableResultSimpleJSONEncoder(JSONEncoder):
    def default(self, o):
        '''extends JsonEncoder to support IterableResult'''
        if isinstance(o, IterableResult):
            return list(o)
