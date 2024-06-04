#
# Copyright (c) 2024, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import argparse
import constant
import time
import socket
import sys
from tqdm import tqdm

from functions.indexes.studyEquipments import get_equipments_index_name
from functions.indexes.studyEquipments import get_tombstoned_equipments_index_name
from functions.indexes.elasticsearch import get_eleasticsearch_host
from functions.indexes.elasticsearch import check_status_eleasticsearch
from functions.indexes.elasticsearch import expunge_deletes
from functions.studies.studies import delete_indexed_equipments
from functions.studies.studies import get_all_orphan_indexed_equipments_network_uuids
from functions.plateform.plateform import check_server_status
from functions.plateform.plateform import get_plateform_info

#
# @author Achour Berrahma <achour.berrahma at rte-france.com>
#

parser = argparse.ArgumentParser(description='Send requests to the gridsuite services to delete orphaned studies indexed equipments and tombstoned equipments.', )

parser.add_argument("-n", "--dry-run", help="test mode (default) will not execute any deletion request",
                    action="store_true")                                                          


args = parser.parse_args()
dry_run = args.dry_run

print("---------------------------------------------------------")
print("Orphaned studies indexed equipments and tombstoned deletion script")
if dry_run:
    print("dry-run=" + str(dry_run) + " -> will run without deleting anything (test mode)")
if constant.DEV:
    print("DEV=" + str(constant.DEV) + " -> hostnames configured for a local execution (localhost:xxxx)")
print("\n")

# Check study-server
if not check_server_status(constant.STUDY_SERVER_HOSTNAME): sys.exit()
print("\n")
# Just getting an enlightening url opportunistically from here because it exists
# TODO better ?
plateformName = get_plateform_info()['redirect_uri']
elasticsearch_host = get_eleasticsearch_host(constant.STUDY_SERVER_HOSTNAME)
elasticsearch_ip = socket.gethostbyname(elasticsearch_host.split(':')[0])
elasticsearch_url = constant.HTTP_PROTOCOL + elasticsearch_host
equipments_index_name = get_equipments_index_name()
tombstoned_equipments_index_name = get_tombstoned_equipments_index_name()

if not check_status_eleasticsearch(elasticsearch_url) : sys.exit()
print("\n")

print("---------------------------------------------------------")
print("This script will apply on plateform = " + plateformName )
print("This platform will execute delete queries on elasticsearch = " + elasticsearch_url + " (" + elasticsearch_ip + ")")
print("\n")
print("===> Both elasticsearch and study-server seem OK ! The script can proceed")
print("\n")
networkUuids = get_all_orphan_indexed_equipments_network_uuids()
print("Orphaned indexed equipments network uuids = " + str(networkUuids))
print("For a total of " + str(len(networkUuids)) + " studies")
print("And will execute on elasticsearch force merge expunge deletes to reclaim space.")
print("---------------------------------------------------------")
if not dry_run:
    print("Orphaned indexed equipments deletion processing...")
    for networkUuid in tqdm(networkUuids):
        delete_indexed_equipments(networkUuid)
    print("Waiting 30 seconds before forcing merge expunge_deletes...")
    time.sleep(30)
    expunge_deletes(elasticsearch_url, equipments_index_name + "," + tombstoned_equipments_index_name)
    print("End of deletion")
else:
    print("Nothing has been impacted (dry-run)")

