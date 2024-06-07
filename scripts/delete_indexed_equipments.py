#
# Copyright (c) 2023, RTE (http://www.rte-france.com)
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

from functions.indexes.studyEquipments import delete_indexed_equipments
from functions.indexes.studyEquipments import get_nb_indexed_equipments
from functions.indexes.studyEquipments import get_nb_indexed_tombstoned_equipments
from functions.indexes.studyEquipments import get_equipments_index_name
from functions.indexes.studyEquipments import get_tombstoned_equipments_index_name
from functions.indexes.elasticsearch import get_eleasticsearch_host
from functions.indexes.elasticsearch import check_status_eleasticsearch
from functions.indexes.elasticsearch import expunge_deletes
from functions.studies.studies import get_all_studies_uuid
from functions.plateform.plateform import check_server_status
from functions.plateform.plateform import get_plateform_info

#
# @author Hugo Marcellin <hugo.marcelin at rte-france.com>
# @author Sylvain Bouzols <sylvain.bouzols at rte-france.com>
#

parser = argparse.ArgumentParser(description='Send requests to the gridsuite services to delete studies indexed equipments and tombstoned', )

parser.add_argument("-n", "--dry-run", help="test mode (default) will not execute any deletion request",
                    action="store_true")                                                          


args = parser.parse_args()
dry_run = args.dry_run

print("---------------------------------------------------------")
print("Studies indexed equipments and tombstoned deletion script")
if dry_run:
    print("dry-run=" + str(dry_run) + " -> will run without deleting anything (test mode)")
if constant.DEV:
    print("DEV=" + str(constant.DEV) + " -> hostnames configured for a local execution (172.17.0.1:xxxx)")
print("\n")

# Check study-server
if not check_server_status(constant.STUDY_SERVER_HOSTNAME): sys.exit()
print("\n")
# Just getting an enlightening url opportunistically from here because it exists
# TODO better ?
plateformName = get_plateform_info()['redirect_uri']
elasticsearch_host = get_eleasticsearch_host(constant.STUDY_SERVER_HOSTNAME)
# TODO don't parse here, instead have the server return structured information
elasticsearch_ip = socket.gethostbyname(elasticsearch_host.split(':')[0])
# TODO we force http but should get this protocol from the server, some servers are not exposed on http but only https for example
elasticsearch_url = constant.HTTP_PROTOCOL + elasticsearch_host
equipments_index_name = get_equipments_index_name()
tombstoned_equipments_index_name = get_tombstoned_equipments_index_name()

if not check_status_eleasticsearch(elasticsearch_url) : sys.exit()
print("\n")

print("---------------------------------------------------------")
print("This script will apply on plateform = " + plateformName )
# TODO It would be nice to show the environment prefix used for elasticsearch indexes names 
print("This plateform will execute delete queries on elasticsearch = " + elasticsearch_url + " (" + elasticsearch_ip + ")")
print("\n")
print("===> Both elasticsearch and study-server seem OK ! The script can proceed")
print("\n")
print("Number of indexed equipments (name: " + equipments_index_name + ") = " + get_nb_indexed_equipments())
print("Number of indexed tombstoned_equipments (name: " + tombstoned_equipments_index_name + ") = " + get_nb_indexed_tombstoned_equipments())
studies = get_all_studies_uuid()
print("For a total of " + str(len(studies)) + " studies")
print("And will execute on elasticsearch force merge expunge deletes to reclaim space.")
print("---------------------------------------------------------")
if not dry_run:
    print("Studies indexed equipments and tombstoned deletion processing...")
    for study in tqdm(studies):
        delete_indexed_equipments(study['id'])
    print("Waiting 30 secondes before force merge expunge_deletes...")
    time.sleep(30)    
    expunge_deletes(elasticsearch_url, equipments_index_name + "," + tombstoned_equipments_index_name)
    print("End of deletion")
else:
    print("Nothing has been impacted (dry-run)")

