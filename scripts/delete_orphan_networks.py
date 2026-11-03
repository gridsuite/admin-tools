#
# Copyright (c) 2026, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import argparse

import psycopg2
import requests

import constant

FIND_ORPHAN_NETWORKS_QUERY = """
SELECT n.uuid, n.id, n.name, n.casedate
FROM iidm.network n
WHERE n.variantnum = 0
  AND NOT EXISTS (SELECT 1 FROM study.root_network r WHERE r.network_uuid = n.uuid)
"""

parser = argparse.ArgumentParser(description="Delete the networks which are not used by any root network")
parser.add_argument("-n", "--dry-run", help="only list the orphan networks, without deleting them", action="store_true")
args = parser.parse_args()

connection = psycopg2.connect("")
cursor = connection.cursor()
cursor.execute(FIND_ORPHAN_NETWORKS_QUERY)
orphan_networks = cursor.fetchall()
connection.close()

print("Found " + str(len(orphan_networks)) + " orphan networks")

for network in orphan_networks:
    network_uuid = network[0]
    print(network)
    if not args.dry_run:
        response = requests.delete(constant.DELETE_NETWORKS + "/" + network_uuid)
        response.raise_for_status()
