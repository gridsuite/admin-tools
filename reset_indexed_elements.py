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

from functions.indexes.directoryElements import delete_indexed_elements
from functions.indexes.directoryElements import reindex_elements
from functions.indexes.directoryElements import get_nb_indexed_elements
from functions.indexes.directoryElements import get_elements_index_name
from functions.indexes.elasticsearch import get_eleasticsearch_host
from functions.indexes.elasticsearch import check_status_eleasticsearch
from functions.indexes.elasticsearch import expunge_deletes
from functions.directoryElements.directoryElements import get_all_directories_uuid
from functions.plateform.plateform import check_server_status
from functions.plateform.plateform import get_plateform_info

#
# @author Sylvain Bouzols <sylvain.bouzols at rte-france.com>
#

parser = argparse.ArgumentParser(description='Send requests to the gridsuite services to reset directory indexed elements', )

parser.add_argument("-n", "--dry-run", help="test mode (default) will not execute any deletion or saving request",
                    action="store_true")                                                          


args = parser.parse_args()
dry_run = args.dry_run

print("---------------------------------------------------------")
print("Directory indexed elements reset script")
if dry_run:
    print("dry-run=" + str(dry_run) + " -> will run without deleting or saving anything (test mode)")
if constant.DEV:
    print("DEV=" + str(constant.DEV) + " -> hostnames configured for a local execution (localhost:xxxx)")
print("\n")

# Check directory-server
if not check_server_status(constant.DIRECTORY_SERVER_HOSTNAME): sys.exit()
print("\n")
# Just getting an enlightening url opportunistically from here because it exists
# TODO better ?
plateformName = get_plateform_info()['redirect_uri']
elasticsearch_host = get_eleasticsearch_host()
# TODO don't parse here, instead have the server return structured information
elasticsearch_ip = socket.gethostbyname(elasticsearch_host.split(':')[0])
# TODO we force http but should get this protocol from the server, some servers are not exposed on http but only https for example
elasticsearch_url = constant.HTTP_PROTOCOL + elasticsearch_host
elements_index_name = get_elements_index_name()

if not check_status_eleasticsearch(elasticsearch_url) : sys.exit()
print("\n")

print("---------------------------------------------------------")
print("This script will apply on plateform = " + plateformName )
# TODO It would be nice to show the environment prefix used for elasticsearch indexes names 
print("This plateform will execute queries on elasticsearch = " + elasticsearch_url + " (" + elasticsearch_ip + ")")
print("\n")
print("===> Both elasticsearch and directory-server seem OK ! The script can proceed")
print("\n")
print("Number of indexed directory elements (name: " + elements_index_name + ") = " + get_nb_indexed_elements())
directories = get_all_directories_uuid()
print("For a total of " + str(len(directories)) + " directories")
print("And will execute on elasticsearch force merge expunge deletes to reclaim space.")
print("---------------------------------------------------------")
if not dry_run:
    print("Directory indexed elements deletion processing...")
    for directory in tqdm(directories):
        delete_indexed_elements(directory['elementUuid'])
    print("Waiting 30 secondes before force merge expunge_deletes...")
    time.sleep(30)    
    expunge_deletes(elasticsearch_url, elements_index_name)
    print("End of deletion")
    print("Directory indexed elements reindexation processing...")
    for directory in tqdm(directories):
        reindex_elements(directory['elementUuid'])
    print("End of reindexation")
else:
    print("Nothing has been impacted (dry-run)")

