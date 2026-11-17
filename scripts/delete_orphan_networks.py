#
# Copyright (c) 2026, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import argparse
import sys
import time

import requests
from tqdm import tqdm

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

if not orphan_networks:
    print("No orphan network to process.")
    sys.exit(0)

print("Selected orphan networks:")
for network in orphan_networks:
    print("  - " + network["uuid"] + " | " + network["id"])

if args.dry_run:
    print("\nDry run mode: no network will be deleted.")
else:
    print("\nDeleting orphan networks...")
    success_count = 0
    failure_count = 0
    total_elapsed = 0.0
    for network in tqdm(orphan_networks):
        network_uuid = network["uuid"]
        start = time.time()
        try:
            response = requests.delete(constant.DELETE_NETWORKS + "/" + network_uuid)
            response.raise_for_status()
            success_count += 1
        except Exception as e:
            failure_count += 1
            tqdm.write(f"  FAILED - {network_uuid} (error: {str(e)})")
            if isinstance(e, requests.exceptions.RequestException) and e.response is not None:
                tqdm.write("Response body: " + repr(e.response.text))
            tqdm.write("")
        finally:
            elapsed = time.time() - start
            total_elapsed += elapsed
            tqdm.write(f"  {network_uuid} - {elapsed:.2f}s")

    print(f"\nDone. {success_count} succeeded, {failure_count} failed. Total deletion time: {total_elapsed:.2f}s (avg {total_elapsed / len(orphan_networks):.2f}s/network)")
