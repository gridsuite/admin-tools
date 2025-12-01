#
# Copyright (c) 2025, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import argparse

from tqdm import tqdm

import constant
import sys

from functions.indexes.elasticsearch import get_elasticsearch_host
from functions.indexes.elasticsearch import check_status_elasticsearch
from functions.plateform.plateform import check_server_status
from functions.plateform.plateform import get_plateform_info
from functions.indexes.studyEquipments import get_studies_index_name, get_equipments_index_name, \
    get_tombstoned_equipments_index_name, get_nb_indexed_studies, get_nb_indexed_equipments, \
    get_nb_indexed_tombstoned_equipments, reindex_study_and_equipments, recreate_study_indices
from functions.studies.studies import get_all_studies_uuid

#
# @author Antoine Bouhours <antoine.bouhours at rte-france.com>
#

parser = argparse.ArgumentParser(description='Send requests to the gridsuite services to reset equipments indexed elements', )

parser.add_argument("-n", "--dry-run", help="test mode (default) will not execute any deletion or saving request",
                    action="store_true")                                                          


args = parser.parse_args()
dry_run = args.dry_run

print("---------------------------------------------------------")
print("Equipment and studies indexed elements reset script")
if dry_run:
    print("dry-run=" + str(dry_run) + " -> will run without deleting or saving anything (test mode)")
if constant.DEV:
    print("DEV=" + str(constant.DEV) + " -> hostnames configured for a local execution (172.17.0.1:xxxx)")
print("\n")

# Check study-server
if not check_server_status(constant.STUDY_SERVER_HOSTNAME): sys.exit()
print("\n")
# Just getting an enlightening url opportunistically from here because it exists
# TODO better ?
plateformName = get_plateform_info()['redirect_uri']
elasticsearch_ip, elasticsearch_url = get_elasticsearch_host(constant.DIRECTORY_SERVER_HOSTNAME)
studies_index_name = get_studies_index_name()
equipments_index_name = get_equipments_index_name()
tombstoned_equipments_index_name = get_tombstoned_equipments_index_name()

print("\n")

print("---------------------------------------------------------")
print("This script will apply on plateform = " + plateformName )
# TODO It would be nice to show the environment prefix used for elasticsearch indexes names
print("This plateform will execute queries on elasticsearch = " + elasticsearch_url + " (" + elasticsearch_ip + ")")
print("\n")
print("===> Both elasticsearch and study-server seem OK ! The script can proceed")
print("\n")
print("Number of indexed studies before reindexation (name: " + studies_index_name + ") = " + get_nb_indexed_studies())
print("Number of indexed equipments before reindexation (name: " + equipments_index_name + ") = " + get_nb_indexed_equipments())
print("Number of indexed tombstoned_equipments before reindexation (name: " + tombstoned_equipments_index_name + ") = " + get_nb_indexed_tombstoned_equipments())
studies = get_all_studies_uuid()
print("For a total of " + str(len(studies)) + " studies")
print("---------------------------------------------------------")

if not dry_run:
    recreate_study_indices()
    print("Study elements reindexation processing...")
    for study in tqdm(studies):
        reindex_study_and_equipments(study['id'])
    print("\n")
    print("End of reindexation")
    print("Number of indexed studies after reindexation (name: " + studies_index_name + ") = " + get_nb_indexed_studies())
    print("Number of indexed equipments after reindexation (name: " + equipments_index_name + ") = " + get_nb_indexed_equipments())
    print("Number of indexed tombstoned_equipments after reindexation (name: " + tombstoned_equipments_index_name + ") = " + get_nb_indexed_tombstoned_equipments())
else:
    print("Nothing has been impacted (dry-run)")
