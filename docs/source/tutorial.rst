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
        print(a['id'], a.association_score['overall'])

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

