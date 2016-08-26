"""
This module communicate with the Open Targets REST API with a simple client, and requires not knowledge of the API.
"""


import logging

from opentargets.conn import Connection, IterableResult

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class OpenTargetsClient(object):
    '''
    main class to use to get data from the Open Targets REST API available at targetvalidation.org, or your private instance

    '''

    _search_endpoint = '/public/search'
    _filter_associations_endpoint = '/public/association/filter'
    _get_associations_endpoint = '/public/association'
    _filter_evidence_endpoint = '/public/evidence/filter'
    _get_evidence_endpoint = '/public/evidence'
    _stats_endpoint = '/public/utils/stats'


    def __init__(self,
                 **kwargs
                 ):
        '''

        :param kwargs: all params forwarded to :class:`opentargets.conn.Connection` object

        '''
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

    def get_association(self,association_id, **kwargs):
        kwargs['id']= association_id
        result = IterableResult(self.conn)
        result(self._get_associations_endpoint, params=kwargs)
        return result

    def filter_associations(self,**kwargs):
        result = IterableResult(self.conn)
        result(self._filter_associations_endpoint, params=kwargs)
        return result

    def get_associations_for_target(self, target, **kwargs):
        if not isinstance(target, str):
            raise AttributeError('target must be of type str')
        if not target.startswith('ENSG'):
            search_result = next(self.search(target, size=1, filter='target'))
            if not search_result:
                raise AttributeError('cannot find an ensembl gene id for target {}'.format(target))
            target_id = search_result['id']
            logger.debug('{} resolved to id {}'.format(target, target_id))
        else:
            target_id = target
        return self.filter_associations(target=target_id,**kwargs)

    def get_associations_for_disease(self, disease, **kwargs):
        if not isinstance(disease, str):
            raise AttributeError('disease must be of type str')
        results = self.filter_associations(disease=disease)
        if not results:
            search_result = next(self.search(disease, size=1, filter='disease'))
            if not search_result:
                raise AttributeError('cannot find an disease id for disease {}'.format(disease))
            disease_id = search_result['id']
            logger.debug('{} resolved to id {}'.format(disease, disease_id))
            results = self.filter_associations(disease=disease_id)
        return results

    def get_evidence(self, evidence_id, **kwargs):
        kwargs['id']= evidence_id
        result = IterableResult(self.conn)
        result(self._get_evidence_endpoint, params=kwargs)
        return result

    def filter_evidence(self,**kwargs):
        result = IterableResult(self.conn)
        result(self._filter_evidence_endpoint, params=kwargs)
        return result

    def get_evidence_for_target(self, target, **kwargs):
        if not isinstance(target, str):
            raise AttributeError('target must be of type str')
        if not target.startswith('ENSG'):
            search_result = next(self.search(target, size=1, filter='target'))
            if not search_result:
                raise AttributeError('cannot find an ensembl gene id for target {}'.format(target))
            target_id = search_result['id']
            logger.debug('{} resolved to id {}'.format(target, target_id))
        else:
            target_id = target
        return self.filter_evidence(target=target_id,**kwargs)

    def get_evidence_for_disease(self, disease, **kwargs):
        if not isinstance(disease, str):
            raise AttributeError('disease must be of type str')
        results = self.filter_evidence(disease=disease)
        if not results:
            search_result = next(self.search(disease, size=1, filter='disease'))
            if not search_result:
                raise AttributeError('cannot find an disease id for disease {}'.format(disease))
            disease_id = search_result['id']
            logger.debug('{} resolved to id {}'.format(disease, disease_id))
            results = self.filter_evidence(disease=disease_id)
        return results

    def get_stats(self):
        result = IterableResult(self.conn)
        result(self._stats_endpoint)
        return result


