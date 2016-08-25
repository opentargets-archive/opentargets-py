import logging

from conn import Connection, IterableResult

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

class OpenTargetClient(object):
    '''
    main class to use to get data from the Open Targets REST API available at targetvalidation.org, or your private instance
    '''

    _search_endpoint = '/public/search'


    def __init__(self,
                 **kwargs
                 ):
        self.conn = Connection(**kwargs)

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        # self.conn.close()
        pass

    def search(self, query,**kwargs):
        kwargs['q']=query
        result = IterableResult(self.conn)
        result(self._search_endpoint,params=kwargs)
        return result