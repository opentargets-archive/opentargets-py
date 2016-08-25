import logging
import unittest

from opentargets import OpenTargetsClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class OpenTargetClientTest(unittest.TestCase):
    _AUTO_GET_TOKEN='auto'

    def setUp(self):

        self.client = OpenTargetsClient()
        self.http2_client = OpenTargetsClient(use_http2=True)

    def tearDown(self):
        self.client.close()


    def testSearchTargetCorrectResult(self):
        target_symbol = 'BRAF'
        response = self.client.search(target_symbol)
        self.assertGreater(len(response),0)
        result = next(response)
        self.assertEqual(result.type, 'search-object-target')
        self.assertEqual(result.id, 'ENSG00000157764')
        self.assertEqual(result.data['approved_symbol'], target_symbol)

    def testSearchTargetFetchAllResults(self):
        target_symbol = 'BRAF'
        response = self.client.search(target_symbol)
        total_results = len(response)
        self.assertGreater(total_results,0)
        c=0
        for i in response:
            c+=1
        self.assertEqual(total_results, c)

    def testSearchTargetCorrectResultHTTP2(self):
        target_symbol = 'BRAF'
        response = self.http2_client.search(target_symbol)
        self.assertGreater(len(response), 0)
        result = next(response)
        self.assertEqual(result.type, 'search-object-target')
        self.assertEqual(result.id, 'ENSG00000157764')
        self.assertEqual(result.data['approved_symbol'], target_symbol)

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

    def testFilterAssociations(self):
        response = self.client.filter_associations()
        self.assertGreater(len(response), 0)
        print(response, len(response))

        result = next(response)
        print(result)

    def testGetAssociationsForTarget(self):
        target_symbol = 'BRAF'
        response = self.client.get_associations_for_target(target_symbol)
        self.assertGreater(len(response), 0)
        result = next(response)
        self.assertEqual(result.target['gene_info']['symbol'], target_symbol)

    def testGetAssociationsForDisease(self):
        disease_label = 'cancer'
        response = self.client.get_associations_for_disease(disease_label)
        self.assertGreater(len(response), 0)
        result = next(response)
        self.assertEqual(result.disease['efo_info']['label'], disease_label)

    def testFilterEvidence(self):
        response = self.client.filter_evidence()
        self.assertGreater(len(response), 0)
        result = next(response)

    def testGetEvidenceForTarget(self):
        target_symbol = 'BRAF'
        response = self.client.get_evidence_for_target(target_symbol)
        self.assertGreater(len(response), 0)
        result = next(response)
        self.assertEqual(result.target['gene_info']['symbol'], target_symbol)

    def testGetEvidenceForDisease(self):
        disease_label = 'medulloblastoma'
        response = self.client.get_evidence_for_disease(disease_label)
        self.assertGreater(len(response), 0)
        result = next(response)
        self.assertEqual(result.disease['efo_info']['label'], disease_label)