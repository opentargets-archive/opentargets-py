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

    from opentargets.conn import result_to_json
    e_for_target = ot.get_evidence_for_target('BRAF')
    for e in e_for_target:
        print(result_to_json(e))

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

