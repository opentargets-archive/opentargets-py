import logging
import unittest

from opentargets import OpenTargetClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class OpenTargetClientTest(unittest.TestCase):
    _AUTO_GET_TOKEN='auto'

    def setUp(self):

        self.client = OpenTargetClient()
        self.http2_client = OpenTargetClient(use_http2=True)

    def tearDown(self):
        self.client.close()


    def testSearchGeneCorrectResult(self):
        gene_symbol = 'BRAF'
        response = self.client.search(gene_symbol)
        self.assertGreater(len(response),0)
        result = next(response)
        self.assertEqual(result.type, 'search-object-target')
        self.assertEqual(result.id, 'ENSG00000157764')
        self.assertEqual(result.data['approved_symbol'], gene_symbol)

    def testSearchGeneFetchAllResults(self):
        gene_symbol = 'BRAF'
        response = self.client.search(gene_symbol)
        total_results = len(response)
        self.assertGreater(total_results,0)
        c=0
        for i in response:
            c+=1
        self.assertEqual(total_results, c)
        print(total_results, c)

    def testSearchGeneCorrectResultHTTP2(self):
        gene_symbol = 'BRAF'
        response = self.http2_client.search(gene_symbol)
        self.assertGreater(len(response), 0)
        result = next(response)
        self.assertEqual(result.type, 'search-object-target')
        self.assertEqual(result.id, 'ENSG00000157764')
        self.assertEqual(result.data['approved_symbol'], gene_symbol)

    def testSearchGeneFetchAllResultsHTTP2(self):
        gene_symbol = 'BRAF'
        response = self.http2_client.search(gene_symbol)
        total_results = len(response)
        self.assertGreater(total_results, 0)
        c = 0
        for i in response:
            c += 1
        self.assertEqual(total_results, c)
        print(total_results, c)

    def testSearchDiseaseCorrectResult(self):
        disease_label = 'cancer'
        response = self.client.search(disease_label)
        self.assertGreater(len(response),0)
        result = next(response)
        self.assertEqual(result.type, 'search-object-disease')
        self.assertEqual(result.id, 'EFO_0000311')


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