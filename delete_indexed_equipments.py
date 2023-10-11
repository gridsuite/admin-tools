#
# Copyright (c) 2023, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import argparse
import constant
import socket
import time
from tqdm import tqdm

from functions.indexes.indexes import delete_indexed_equipments
from functions.indexes.indexes import get_nb_indexed_equipments
from functions.indexes.indexes import get_nb_indexed_tombstoned_equipments
from functions.indexes.indexes import get_equipments_index_name
from functions.indexes.indexes import get_tombstoned_equipments_index_name
from functions.indexes.indexes import expunge_deletes
from functions.studies.studies import get_all_studies_uuid

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
    print("DEV=" + str(constant.DEV) + " -> hostnames configured for a local execution (localhost:xxxx)")
print("\n")

studies = get_all_studies_uuid()

print("---------------------------------------------------------")
hostname = socket.gethostname()
host_ip = socket.gethostbyname(hostname)
equipments_index_name = get_equipments_index_name()
tombstoned_equipments_index_name = get_tombstoned_equipments_index_name()
print("This script will apply on Host = " + hostname + "(" + host_ip + ")")
print("Number of indexed equipments (name: " + equipments_index_name + ") = " + get_nb_indexed_equipments())
print("Number of indexed tombstoned_equipments (name: " + tombstoned_equipments_index_name + ") = " + get_nb_indexed_tombstoned_equipments())
print("For a total of = " + str(len(studies)) + " studies")
print("---------------------------------------------------------")
if not dry_run:
    print("Studies indexed equipments and tombstoned deletion processing...")
    for study in tqdm(studies):
        delete_indexed_equipments(study['id'])
    print("Waiting 30 secondes before force merger expunge_deletes...")
    time.sleep(30)    
    expunge_deletes(equipments_index_name + "," + tombstoned_equipments_index_name)
    print("End of deletion")
else:
    print("Nothing has been impacted (dry-run)")

