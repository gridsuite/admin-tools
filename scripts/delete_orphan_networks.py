#
# Copyright (c) 2026, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import argparse

import requests

import constant
from functions.clean_orphan_elements.clean_orphan_networks import get_network_uuids_from_studies

parser = argparse.ArgumentParser(description="Delete the networks which are not used by any root network")
parser.add_argument("-n", "--dry-run", help="only list the orphan networks, without deleting them", action="store_true")
parser.add_argument("-l", "--limit", help="maximum number of orphan networks to delete", type=int)
args = parser.parse_args()

studies_response = requests.get(constant.GET_SUPERVISION_STUDIES)
studies_response.raise_for_status()
used_network_uuids = set(get_network_uuids_from_studies(studies_response.json()))

networks_response = requests.get(constant.GET_NETWORKS)
networks_response.raise_for_status()

orphan_networks = []
for network in networks_response.json():
    if network["uuid"] not in used_network_uuids:
        orphan_networks.append(network)

print("Found " + str(len(orphan_networks)) + " orphan networks")

if args.limit is not None and args.limit < len(orphan_networks):
    print("Limit applied: processing " + str(args.limit) + " out of " + str(len(orphan_networks)) + " orphan networks")
    orphan_networks = orphan_networks[:args.limit]

for network in orphan_networks:
    print(network["uuid"] + " " + network["id"])
    if not args.dry_run:
        response = requests.delete(constant.DELETE_NETWORKS + "/" + network["uuid"])
        response.raise_for_status()
