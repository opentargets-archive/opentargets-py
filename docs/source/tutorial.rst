.. _tutorial:

========
Tutorial
========

Quick Start
-----------

import the high level client
::

    from opentargets import OpenTargetsClient
    ot = OpenTargetsClient()

search for a target:
::

    search_result = ot.search('BRAF')
    print search_result[0]

search associations for a target:
::

    a_for_target = ot.get_associations_for_target('BRAF')
    for a in a_for_target:
        print(a['id'], a['association_score']['overall'])

search associations for a disease:
::

  a_for_disease = ot.get_associations_for_disease('cancer')

get an association by id:
::

    print(ot.get_association('ENSG00000157764-EFO_0005803')[0])

get evidence for a target:
::

    e_for_target = ot.get_evidence_for_target('BRAF')
    for evidence_json in e_for_target.to_json():
        print(evidence_json)

get evidence for a disease:
::

    e_for_disease = ot.get_evidence_for_disease('medulloblastoma')
get an evidence by id:
::

    print(ot.get_evidence('5cf863da265c32d112ff4fc3bfc25ab3')[0])

get stats about the release:
::

    print(ot.get_stats().info)

use incremental filter:
::

    >>> from opentargets import OpenTargetsClient
    >>> client = OpenTargetsClient()
    >>> response = client.filter_associations()
    >>> response
    <opentargets.conn.IterableResult object at 0x105c32d68>
    >>> print(response)
    2484000 Results found
    >>> response.filter(target='ENSG00000157764')
    >>> print(response)
    865 Results found | parameters: {'target': 'ENSG00000157764'}
    >>> response.filter(direct=True)
    >>> print(response)
    454 Results found | parameters: {'target': 'ENSG00000157764', 'direct': True}
    >>> response.filter(scorevalue_min=0.2)
    >>> print(response)
    156 Results found | parameters: {'scorevalue_min': 0.2, 'target': 'ENSG00000157764', 'direct': True}
    >>> response.filter(therapeutic_area='efo_0000701')
    >>> print(response)
    12 Results found | parameters: {'therapeutic_area': 'efo_0000701', 'scorevalue_min': 0.2, 'target': 'ENSG00000157764', 'direct': True}
    >>> for i, r in enumerate(response):
    ...     print(i, r['id'], r['association_score']['overall'], r['disease']['efo_info']['label'])
    ...
    0 ENSG00000157764-EFO_0000756 1.0 melanoma
    1 ENSG00000157764-Orphanet_1340 1.0 Cardiofaciocutaneous syndrome
    2 ENSG00000157764-Orphanet_648 1.0 Noonan syndrome
    3 ENSG00000157764-Orphanet_500 1.0 LEOPARD syndrome
    4 ENSG00000157764-EFO_0002617 1.0 metastatic melanoma
    5 ENSG00000157764-EFO_0000389 0.9975053926198617 cutaneous melanoma
    6 ENSG00000157764-EFO_0004199 0.6733333333333333 dysplastic nevus
    7 ENSG00000157764-EFO_0002894 0.6638888888888889 amelanotic skin melanoma
    8 ENSG00000157764-EFO_1000080 0.5609555555555555 Anal Melanoma
    9 ENSG00000157764-EFO_0000558 0.5602555555555556 Kaposi's sarcoma
    10 ENSG00000157764-EFO_1000249 0.5555555555555556 Extramammary Paget Disease
    11 ENSG00000157764-Orphanet_774 0.21793721666666668 Hereditary hemorrhagic telangiectasia


export a table with association score for each datasource into an excel file:
::

    >>> from opentargets import OpenTargetsClient
    >>> client = OpenTargetsClient()
    >>> response = client.get_associations_for_target('BRAF',
    ...     fields=['association_score.datasource*',
    ...             'association_score.overall',
    ...             'target.gene_info.symbol',
    ...             'disease.efo_info.*']
    ...     )
    >>> response
    865 Results found | parameters: {'target': 'ENSG00000157764', 'fields': ['association_score.datasource*', 'association_score.overall', 'target.gene_info.symbol', 'disease.efo_info.label']}
    >>> response.to_excel('BRAF_associated_diseases_by_datasource.xls')
    >>>

If you want to change the way the associations are scored using just some datatype you might try something like this:
::

    >>> from opentargets import OpenTargetsClient
    >>> from opentargets.statistics import HarmonicSumScorer
    >>> ot = OpenTargetsClient()
    >>> r = ot.get_associations_for_target('BRAF')
    >>> interesting_datatypes = ['genetic_association', 'known_drug', 'somatic_mutation']
    >>> def score_with_datatype_subset(datatypes, results):
    ...     for i in results:
    ...         datatype_scores = i['association_score']['datatypes']
    ...         filtered_scores = [datatype_scores[dt] for dt in datatypes]
    ...         custom_score = HarmonicSumScorer.harmonic_sum(filtered_scores)
    ...         if custom_score:
    ...             yield (custom_score, i['disease']['id'], dict(zip(datatypes, filtered_scores))) #return some useful data
    >>> for i in score_with_datatype_subset(interesting_datatypes, r):
    ...     print(i)
    (1.8333333333333333, 'EFO_0000701', {'genetic_association': 1.0, 'known_drug': 1.0, 'somatic_mutation': 1.0})
    (1.8333333333333333, 'EFO_0000616', {'genetic_association': 1.0, 'known_drug': 1.0, 'somatic_mutation': 1.0})
    (1.8333333333333333, 'EFO_0000311', {'genetic_association': 1.0, 'known_drug': 1.0, 'somatic_mutation': 1.0})
    (1.8333333333333333, 'EFO_0001379', {'genetic_association': 1.0, 'known_drug': 1.0, 'somatic_mutation': 1.0})
    (1.8333333333333333, 'EFO_0000313', {'genetic_association': 1.0, 'known_drug': 1.0, 'somatic_mutation': 1.0})
    (1.8333333333333333, 'EFO_0005803', {'genetic_association': 1.0, 'known_drug': 1.0, 'somatic_mutation': 1.0})
    (1.8333333333333333, 'EFO_0001642', {'genetic_association': 1.0, 'known_drug': 1.0, 'somatic_mutation': 1.0})
    (1.587037037037037, 'EFO_0000319', {'genetic_association': 1.0, 'known_drug': 1.0, 'somatic_mutation': 0.2611111111111111})
    (1.5949074074074074, 'EFO_0000508', {'genetic_association': 1.0, 'known_drug': 1.0, 'somatic_mutation': 0.2847222222222222})
    1.5, 'Orphanet_183530', {'genetic_association': 1.0, 'known_drug': 1.0, 'somatic_mutation': 0.0})
    (1.5, 'EFO_0003777', {'genetic_association': 1.0, 'known_drug': 1.0, 'somatic_mutation': 0.0})
    (1.5, 'Orphanet_98054', {'genetic_association': 1.0, 'known_drug': 1.0, 'somatic_mutation': 0.0})
    (1.5, 'Orphanet_99739', {'genetic_association': 1.0, 'known_drug': 1.0, 'somatic_mutation': 0.0})
    (1.5, 'Orphanet_217595', {'genetic_association': 1.0, 'known_drug': 1.0, 'somatic_mutation': 0.0})
    (1.5, 'Orphanet_183570', {'genetic_association': 1.0, 'known_drug': 1.0, 'somatic_mutation': 0.0})
    (1.5, 'Orphanet_98733', {'genetic_association': 1.0, 'known_drug': 1.0, 'somatic_mutation': 0.0})
    (1.6050444693876402, 'EFO_0000684', {'genetic_association': 1.0, 'known_drug': 1.0, 'somatic_mutation': 0.31513340816292035})
    (1.6050444693876402, 'EFO_0003818', {'genetic_association': 1.0, 'known_drug': 1.0, 'somatic_mutation': 0.31513340816292035})
    (1.6050444693876402, 'EFO_0003853', {'genetic_association': 1.0, 'known_drug': 1.0, 'somatic_mutation': 0.31513340816292035})
    (1.6050444693876402, 'EFO_0001071', {'genetic_association': 1.0, 'known_drug': 1.0, 'somatic_mutation': 0.31513340816292035})
    (1.5408333333333333, 'EFO_0000618', {'genetic_association': 1.0, 'known_drug': 1.0, 'somatic_mutation': 0.1225})
    (1.6803112925534462, 'EFO_0000228', {'genetic_association': 1.0, 'known_drug': 0.9357799925142999, 'somatic_mutation': 0.6372638888888889})
    (1.6013073034769463, 'EFO_0000512', {'genetic_association': 1.0, 'known_drug': 1.0, 'somatic_mutation': 0.303921910430839})



