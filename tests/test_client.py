import json
import logging
import unittest

from opentargets import Connection
from opentargets import OpenTargetsClient
from opentargets.statistics import HarmonicSumScorer

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class OpenTargetClientTest(unittest.TestCase):
    _AUTO_GET_TOKEN = 'auto'

    def setUp(self):

        self.client = OpenTargetsClient()
        self.http2_client = OpenTargetsClient(use_http2=True)
        self.auth_client = OpenTargetsClient(auth_app_name='test',
                                             auth_secret='test', )

    def tearDown(self):
        self.client.close()

    def testSearchTargetCorrectResult(self):
        target_symbol = 'BRAF'
        response = self.client.search(target_symbol)
        self.assertGreater(len(response), 0)
        result = next(response)
        self.assertEqual(result['type'], 'search-object-target')
        self.assertEqual(result['id'], 'ENSG00000157764')
        self.assertEqual(result['data']['approved_symbol'], target_symbol)

    def testSearchTargetFetchAllResults(self):
        target_symbol = 'BRAF'
        response = self.client.search(target_symbol)
        total_results = len(response)
        self.assertGreater(total_results, 0)
        c = 0
        for i in response:
            c += 1
        self.assertEqual(total_results, c)

    def testSearchTargetFetchAllResultsAuth(self):
        target_symbol = 'BRAF'
        response = self.auth_client.search(target_symbol)
        total_results = len(response)
        self.assertGreater(total_results, 0)
        c = 0
        for i in response:
            c += 1
        self.assertEqual(total_results, c)

    def testSearchTargetCorrectResultHTTP2(self):
        target_symbol = 'BRAF'
        response = self.http2_client.search(target_symbol)
        self.assertGreater(len(response), 0)
        result = next(response)
        self.assertEqual(result['type'], 'search-object-target')
        self.assertEqual(result['id'], 'ENSG00000157764')
        self.assertEqual(result['data']['approved_symbol'], target_symbol)

    def testSearchTargetFetchAllResultsHTTP2(self):
        target_symbol = 'BRAF'
        response = self.http2_client.search(target_symbol)
        total_results = len(response)
        self.assertGreater(total_results, 0)
        c = 0
        for i in response:
            c += 1
        self.assertEqual(total_results, c)

    def testSearchDiseaseCorrectResult(self):
        disease_label = 'cancer'
        response = self.client.search(disease_label)
        self.assertGreater(len(response), 0)
        result = next(response)
        self.assertEqual(result['type'], 'search-object-disease')
        self.assertEqual(result['id'], 'EFO_0000311')

    # #this takes a lot to run
    # def testSearchDiseaseFetchAllResults(self):
    #     disease_label = 'cancer'
    #     response = self.client.search(disease_label, size = 100)
    #     total_results = len(response)
    #     self.assertGreater(total_results,0)
    #     c=0
    #     for i in response:
    #         c+=1
    #     self.assertEqual(total_results, c)
    #     print(total_results, c)

    def testGetAssociation(self):
        association_id = "ENSG00000157764-EFO_0005803"
        response = self.client.get_association(association_id)
        self.assertEquals(len(response), 1)
        self.assertEquals(association_id, response[0]['id'])

    def testFilterAssociations(self):
        response = self.client.filter_associations()
        self.assertGreater(len(response), 0)
        total = response.info.total
        print(response)
        response.filter(target='ENSG00000157764')
        self.assertLess(len(response), total)
        print(response)
        total = response.info.total
        response.filter(direct=True)
        self.assertLess(len(response), total)
        print(response)
        total = response.info.total
        response.filter(scorevalue_min=0.2)
        self.assertLess(len(response), total)
        print(response)
        total = response.info.total
        response.filter(therapeutic_area='efo_0000701')
        self.assertLess(len(response), total)
        print(response)
        results = []
        for i, r in enumerate(response):
            print(i, r['id'], r['association_score']['overall'], r['disease']['efo_info']['label'])
            results.append(r)
        response_multi = self.client.filter_associations(target='ENSG00000157764', direct=True, scorevalue_min=0.2,
                                                         therapeutic_area='efo_0000701')
        self.assertEqual(len(response_multi), response.info.total)
        for i, r in enumerate(response_multi):
            self.assertEqual(results[i]['id'], r['id'])
        response_chained = self.client.filter_associations().filter(target='ENSG00000157764').filter(
            direct=True).filter(therapeutic_area='efo_0000701').filter(scorevalue_min=0.2)
        self.assertEqual(len(response_chained), response.info.total)
        for i, r in enumerate(response_chained):
            self.assertEqual(results[i]['id'], r['id'])

    def testGetAssociationsForTarget(self):
        target_symbol = 'BRAF'
        response = self.client.get_associations_for_target(target_symbol)
        self.assertGreater(len(response), 0)
        result = next(response)
        self.assertEqual(result['target']['gene_info']['symbol'], target_symbol)

    def testGetAssociationsForDisease(self):
        disease_label = 'cancer'
        response = self.client.get_associations_for_disease(disease_label)
        self.assertGreater(len(response), 0)
        result = next(response)
        self.assertEqual(result['disease']['efo_info']['label'], disease_label)

    def testGetEvidence(self):
        evidence_id = "5cf863da265c32d112ff4fc3bfc25ab3"
        response = self.client.get_evidence(evidence_id)
        self.assertEquals(len(response), 1)
        self.assertEquals(evidence_id, response[0]['id'])

    def testFilterEvidence(self):
        response = self.client.filter_evidence()
        self.assertGreater(len(response), 0)

    def testGetEvidenceForTarget(self):
        target_symbol = 'BRAF'
        response = self.client.get_evidence_for_target(target_symbol)
        self.assertGreater(len(response), 0)
        result = next(response)
        self.assertEqual(result['target']['gene_info']['symbol'], target_symbol)

    def testGetEvidenceForDisease(self):
        disease_label = 'medulloblastoma'
        response = self.client.get_evidence_for_disease(disease_label)
        self.assertGreater(len(response), 0)
        result = next(response)
        self.assertEqual(result['disease']['efo_info']['label'], disease_label)

    def testSerialiseToJson(self):
        target_symbol = 'BRAF'
        '''test iterable version'''
        response = self.client.get_associations_for_target(target_symbol)
        items = len(response)
        self.assertGreater(len(response), 0)
        json_output = response.to_json()
        parsed_json = [json.loads(i) for i in json_output]
        self.assertEqual(items, len(parsed_json))
        '''test non iterable version'''
        response = self.client.get_associations_for_target(target_symbol)
        items = len(response)
        self.assertGreater(len(response), 0)
        json_output = response.to_json(iterable=False)
        parsed_json = json.loads(json_output)
        self.assertEqual(items, len(parsed_json))

    def testResultToPandasDataFrame(self):
        target_symbol = 'BRAF'
        response = self.client.get_associations_for_target(target_symbol)
        items = len(response)
        self.assertGreater(len(response), 0)
        dataframe = response.to_dataframe()
        self.assertEqual(len(dataframe), items)

    def testResultToPandasCSV(self):
        target_symbol = 'BRAF'
        response = self.client.get_associations_for_target(target_symbol,
                                                           fields=['association_score.*',
                                                                   'target.gene_info.symbol',
                                                                   'disease.efo_info.*']
                                                           )
        items = len(response)
        self.assertGreater(len(response), 0)
        csv = response.to_csv()
        open('test.csv', 'wb').write(csv.encode('utf-8'))
        self.assertEqual(len(csv.split('\n')), items + 2)

    def testResultToPandasExcel(self):
        target_symbol = 'BRAF'
        response = self.client.get_associations_for_target(target_symbol,
                                                           fields=['association_score.*',
                                                                   'target.gene_info.symbol',
                                                                   'disease.efo_info.*']
                                                           )
        self.assertGreater(len(response), 0)
        response.to_excel('test.xls')

    def testSerialiseToNamedtuple(self):
        target_symbol = 'BRAF'
        response = self.client.get_associations_for_target(target_symbol)
        items = len(response)
        self.assertGreater(len(response), 0)
        nt_output = list(response.to_namedtuple())
        for i, result in enumerate(nt_output):
            self.assertIsNotNone(result.target.id)
        self.assertEqual(items, i + 1)

    def testGetStats(self):
        response = self.client.get_stats()
        self.assertEquals(len(response), 0)

    def testAutodetectPost(self):
        self.assertFalse(Connection._auto_detect_post({'target': ['ENSG00000157764']}))
        self.assertTrue(Connection._auto_detect_post({'target': ['ENSG00000157764',
                                                                 'ENSG00000171862',
                                                                 'ENSG00000136997',
                                                                 'ENSG00000012048',
                                                                 'ENSG00000139618',
                                                                 ]}))

    def testGetToPost(self):
        response = self.client.conn.get('/public/association/filter', params={'target': ['ENSG00000157764',
                                                                                         'ENSG00000171862',
                                                                                         'ENSG00000136997',
                                                                                         'ENSG00000012048',
                                                                                         'ENSG00000139618',
                                                                                         ]})
        self.assertGreater(len(response), 0)

    def testCustomScore(self):
        def score_with_datatype_subset(datatypes, results):
            for r in results:
                datatype_scores = r['association_score']['datatypes']
                filtered_scores = [datatype_scores[dt] for dt in datatypes]
                custom_score = HarmonicSumScorer.harmonic_sum(filtered_scores)
                if custom_score:
                    yield (round(custom_score, 3), r['disease']['id'], dict(zip(datatypes, filtered_scores)))

        target_symbol = 'BRAF'
        response = self.client.get_associations_for_target(target_symbol)
        self.assertGreater(len(response), 0)
        for i, filtered_data in enumerate(score_with_datatype_subset(['genetic_association',
                                                                      'known_drug',
                                                                      'somatic_mutation'],
                                                                     response)):
            self.assertGreater(filtered_data[0], 0.)

        self.assertLess(i, len(response))

    def testGetAvailableEndpoints(self):
        endpoints = self.client.conn.get_api_endpoints()
        self.assertTrue('/public/search' in endpoints)

    def testGetEndpointDocs(self):
        docs = self.client.conn.api_endpoint_docs('/public/search')
        self.assertGreater(len(docs['get']['parameters']),0)

    def testPing(self):
        response = self.client.conn.ping()
        if isinstance(response, bool):
            self.assertTrue(response)
        else:
            self.assertIsNotNone(response)