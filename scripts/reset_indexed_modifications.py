#
# Copyright (c) 2025, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import argparse
import constant
import sys
from tqdm import tqdm

from functions.indexes.modifications import get_modifications_index_name
from functions.indexes.modifications import get_nb_indexed_modifications
from functions.indexes.modifications import get_nb_modifications_to_index
from functions.indexes.modifications import recreate_modifications_index
from functions.indexes.modifications import get_modifications_network_uuids
from functions.indexes.modifications import reindex_modifications
from functions.indexes.elasticsearch import get_elasticsearch_host
from functions.indexes.elasticsearch import check_status_elasticsearch
from functions.plateform.plateform import check_server_status
from functions.plateform.plateform import get_plateform_info

#
# @author Kevin Le Saulnier <kevin.lesaulnier at rte-france.com>
#

parser = argparse.ArgumentParser(description='Send requests to the gridsuite services to reset indexed modifications', )

parser.add_argument("-n", "--dry-run", help="test mode (default) will not execute any deletion or saving request",
                    action="store_true")                                                          


args = parser.parse_args()
dry_run = args.dry_run

print("---------------------------------------------------------")
print("Indexed modifications reset script")
if dry_run:
    print("dry-run=" + str(dry_run) + " -> will run without deleting or saving anything (test mode)")
if constant.DEV:
    print("DEV=" + str(constant.DEV) + " -> hostnames configured for a local execution (172.17.0.1:xxxx)")
print("\n")

# Check directory-server
if not check_server_status(constant.MODIFICATION_SERVER_HOSTNAME): sys.exit()
print("\n")
# Just getting an enlightening url opportunistically from here because it exists
# TODO better ?
plateformName = get_plateform_info()['redirect_uri']
elasticsearch_ip, elasticsearch_url = get_elasticsearch_host(constant.MODIFICATION_SERVER_HOSTNAME)
modifications_index_name = get_modifications_index_name()
network_uuids = get_modifications_network_uuids()

if not check_status_elasticsearch(elasticsearch_url) : sys.exit()
print("\n")

print("---------------------------------------------------------")
print("This script will apply on plateform = " + plateformName )
# TODO It would be nice to show the environment prefix used for elasticsearch indexes names 
print("This plateform will execute queries on elasticsearch = " + elasticsearch_url + " (" + elasticsearch_ip + ")")
print("\n")
print("===> Both elasticsearch and network-modification-server seem OK ! The script can proceed")
print("\n")
print("Number of indexed modifications before reindexation (name: " + modifications_index_name + ") = " + get_nb_indexed_modifications())
print("Number of modifications to index = " + get_nb_modifications_to_index())
print("Number of network uuids with indexed modifications : " + str(len(network_uuids)))
print("---------------------------------------------------------")
if not dry_run:
    recreate_modifications_index()
    print("Modifications reindexation processing...")
    for network_uuid in tqdm(network_uuids):
        reindex_modifications(network_uuid)
    print("End of reindexation")
    print("Number of indexed modifications after reindexation (name: " + modifications_index_name + ") = " + get_nb_indexed_modifications())
else:
    print("Nothing has been impacted (dry-run)")

