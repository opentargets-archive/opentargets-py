"""
This module communicate with the Open Targets REST API with a simple client, and requires not knowledge of the API.
"""
from opentargets.conn import Connection, IterableResult

import logging
logging.getLogger('opentargets').addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class OpenTargetsClient(object):
    """
    Main class to use to get data from the Open Targets
    REST API available at targetvalidation.org (or your
    private instance)

    """

    _search_endpoint = '/platform/public/search'
    _filter_associations_endpoint = '/platform/public/association/filter'
    _get_associations_endpoint = '/platform/public/association'
    _filter_evidence_endpoint = '/platform/public/evidence/filter'
    _get_evidence_endpoint = '/platform/public/evidence'
    _stats_endpoint = '/platform/public/utils/stats'
    _relation_target_endpoint = '/platform/private/relation/target'
    _relation_disease_endpoint = '/platform/private/relation/disease'

    def __init__(self,
                 **kwargs
                 ):
        """
        Init the client and start a connection

        Keyword Args:
            **kwargs: all params forwarded to ``opentargets.conn.Connection`` object
        """
        self.conn = Connection(**kwargs)

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.conn.close()

    def search(self, query,**kwargs):
        """
        Search a string and return a list of objects form the search method of the REST API.
        E.g. A returned object could be a target or a disease

        Args:
            query (str): string to search for
        Keyword Args:
            **kwargs: are passed as other parameters to the /public/search method of the REST API

        Returns:
            IterableResult: Result of the query
        """
        kwargs['q']=query
        result = IterableResult(self.conn)
        result(self._search_endpoint,**kwargs)
        return result

    def get_association(self,association_id, **kwargs):
        """
        Retrieve a specific Association object from the REST API provided its ID

        Args:
            association_id (str): Association ID
        Keyword Args:
            **kwargs: are passed as other parameters to the /public/association method of the REST API

        Returns:
             IterableResult: Result of the query
        """
        kwargs['id']= association_id
        result = IterableResult(self.conn)
        result(self._get_associations_endpoint, **kwargs)
        return result

    def filter_associations(self,**kwargs):
        """
        Retrieve a set of associations by applying a set of filters

        Keyword Args:
            **kwargs: are passed as parameters to the /public/association/filterby method of the REST API

        Returns:
            IterableResult: Result of the query
        """
        result = IterableResult(self.conn)
        result(self._filter_associations_endpoint, **kwargs)
        return result

    def get_associations_for_target(self, target, **kwargs):
        """
        Same as ``OpenTargetsClient.filter_associations`` but accept any string as `target` parameter and fires a search
        if it is not an Ensembl Gene identifier

        Args:
            target (str): an Ensembl Gene identifier or a string to search for a gene mapping
        Keyword Args:
            **kwargs: are passed as parameters to the /public/association/filterby method of the REST API
        Returns:
            IterableResult: Result of the query
        """
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
        """
        Same as ``OpenTargetsClient.filter_associations`` but accept any string as `disease` parameter and
        fires a search if it is not a valid disease identifier

        Args:
            disease (str): a disease identifier or a string to search for a disease mapping
        Keyword Args:
            **kwargs: are passed as parameters to the /public/association/filterby method of the REST API
        Returns:
            IterableResult: Result of the query
        """
        if not isinstance(disease, str):
            raise AttributeError('disease must be of type str')
        results = self.filter_associations(disease=disease)
        if not results:
            search_result = next(self.search(disease, size=1, filter='disease'))
            if not search_result:
                raise AttributeError('cannot find an disease id for disease {}'.format(disease))
            disease_id = search_result['id']
            logger.debug('{} resolved to id {}'.format(disease, disease_id))
            results = self.filter_associations(disease=disease_id, **kwargs)
        return results

    def get_evidence(self, evidence_id, **kwargs):
        """
        Retrieve a specific Evidence object from the REST API provided its ID

        Args:
            evidence_id:
        Keyword Args:
            **kwargs: are passed as other parameters to the /public/evidence method of the REST API

        Returns:
             IterableResult: Result of the query
        """
        kwargs['id']= evidence_id
        result = IterableResult(self.conn)
        result(self._get_evidence_endpoint, **kwargs)
        return result

    def filter_evidence(self,**kwargs):
        """
        Retrieve a set of evidence by applying a set of filters

        Keyword Args:
            **kwargs: are passed as parameters to the /public/evidence/filterby method of the REST API

        Returns:
            IterableResult: Result of the query
        """
        result = IterableResult(self.conn)
        result(self._filter_evidence_endpoint, **kwargs)
        return result

    def get_evidence_for_target(self, target, **kwargs):
        """
        Same as ``OpenTargetsClient.filter_evidence`` but accept any string as `target` parameter and fires a search
        if it is not an Ensembl Gene identifier

        Args:
            target (str): an Ensembl Gene identifier or a string to search for a gene mapping
        Keyword Args:
            **kwargs: are passed as parameters to the /public/evidence/filterby method of the REST API
        Returns:
            IterableResult: Result of the query
        """
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
        """
        Same as ``OpenTargetsClient.filter_evidence`` but accept any string as `disease` parameter and
        fires a search if it is not a valid disease identifier

        Args:
            disease (str): a disease identifier or a string to search for a disease mapping
        Keyword Args:
            **kwargs: are passed as parameters to the /public/evidence/filterby method of the REST API
        Returns:
            IterableResult: Result of the query
        """
        if not isinstance(disease, str):
            raise AttributeError('disease must be of type str')
        results = self.filter_evidence(disease=disease, **kwargs)
        if not results:
            search_result = next(self.search(disease, size=1, filter='disease'))
            if not search_result:
                raise AttributeError('cannot find an disease id for disease {}'.format(disease))
            disease_id = search_result['id']
            logger.debug('{} resolved to id {}'.format(disease, disease_id))
            results = self.filter_evidence(disease=disease_id)
        return results

    def get_similar_target(self, target, **kwargs):
        """
        Return targets sharing a similar patter nof association to diseases
        Accepts any string as `target` parameter and fires a search if it is not an Ensembl Gene identifier

        Args:
            target (str): an Ensembl Gene identifier or a string to search for a gene mapping
        Keyword Args:
            **kwargs: are passed as parameters to the /private/relation/target method of the REST API
        Returns:
            IterableResult: Result of the query
        """
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

        result = IterableResult(self.conn)
        result(self._relation_target_endpoint+'/'+target_id, **kwargs)
        return result

    def get_similar_disease(self, disease, **kwargs):
        """
        Return targets sharing a similar patter nof association to diseases
        Accepts any string as `disease` parameter and fires a search if nothing is retireved on a first attempt

        Args:
            disease (str): a disease identifier or a string to search for a disease mapping
        Keyword Args:
            **kwargs: are passed as parameters to the /private/relation/disease method of the REST API
        Returns:
            IterableResult: Result of the query
        """
        if not isinstance(disease, str):
            raise AttributeError('disease must be of type str')
        result = IterableResult(self.conn)
        result(self._relation_disease_endpoint+'/'+disease, **kwargs)
        if not result:
            search_result = next(self.search(disease, size=1, filter='disease'))
            if not search_result:
                raise AttributeError('cannot find an disease id for disease {}'.format(disease))
            disease_id = search_result['id']
            logger.debug('{} resolved to id {}'.format(disease, disease_id))
            result = IterableResult(self.conn)
            result(self._relation_disease_endpoint + '/' + disease_id, **kwargs)
        return result

    def get_stats(self):
        """
        Returns statistics about the data served by the REST API

        Returns:
            IterableResult: Result of the query
        """
        result = IterableResult(self.conn)
        result(self._stats_endpoint)
        return result
