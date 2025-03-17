#
# Copyright (c) 2024, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import argparse
import constant
import sys

from functions.indexes.cases import recreate_elements_index
from functions.indexes.cases import reindex_elements
from functions.indexes.cases import get_nb_indexed_elements
from functions.indexes.cases import get_elements_index_name
from functions.indexes.elasticsearch import get_elasticsearch_host
from functions.indexes.elasticsearch import check_status_elasticsearch
from functions.plateform.plateform import check_server_status
from functions.plateform.plateform import get_plateform_info

#
# @author Jamal KHEYYAD <jamal.kheyyad at rte-international.com>
#

parser = argparse.ArgumentParser(description='Send requests to the gridsuite services to reset indexed cases', )

parser.add_argument("-n", "--dry-run", help="test mode (default) will not execute any deletion or saving request",
                    action="store_true")                                                          


args = parser.parse_args()
dry_run = args.dry_run

print("---------------------------------------------------------")
print("indexed cases reset script")
if dry_run:
    print("dry-run=" + str(dry_run) + " -> will run without deleting or saving anything (test mode)")
if constant.DEV:
    print("DEV=" + str(constant.DEV) + " -> hostnames configured for a local execution (172.17.0.1:xxxx)")
print("\n")

# Check case-server
if not check_server_status(constant.CASE_SERVER_HOSTNAME): sys.exit()
print("\n")
# Just getting an enlightening url opportunistically from here because it exists
# TODO better ?
plateformName = get_plateform_info()['redirect_uri']
elasticsearch_ip, elasticsearch_url = get_elasticsearch_host(constant.CASE_SERVER_HOSTNAME)
elements_index_name = get_elements_index_name()

if not check_status_elasticsearch(elasticsearch_url) : sys.exit()
print("\n")

print("---------------------------------------------------------")
print("This script will apply on plateform = " + plateformName )
# TODO It would be nice to show the environment prefix used for elasticsearch indexes names 
print("This plateform will execute queries on elasticsearch = " + elasticsearch_url + " (" + elasticsearch_ip + ")")
print("\n")
print("===> Both elasticsearch and case-server seem OK ! The script can proceed")
print("\n")
print("Number of indexed cases elements before reindexation (name: " + elements_index_name + ") = " + get_nb_indexed_elements())
print("---------------------------------------------------------")
if not dry_run:
    recreate_elements_index()
    print("Cases elements reindexation processing...")
    reindex_elements()
    print("End of reindexation")
    print("Number of indexed cases elements after reindexation (name: " + elements_index_name + ") = " + get_nb_indexed_elements())
else:
    print("Nothing has been impacted (dry-run)")

