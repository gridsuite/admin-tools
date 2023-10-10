#
# Copyright (c) 2023, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import argparse
import constant
import socket
from tqdm import tqdm

from functions.indexes.indexes import delete_indexed_equipments 
from functions.indexes.indexes import get_nb_indexed_equipments 
from functions.indexes.indexes import get_nb_indexed_tombstoned_equipments 
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
print("\n")

studies = get_all_studies_uuid()

print("---------------------------------------------------------")
print("This script will apply on Host = " + socket.gethostname())
print("nb indexed equipments = " + get_nb_indexed_equipments())
print("nb indexed tombstoned_equipments = " + get_nb_indexed_tombstoned_equipments())
print("for a total of = " + str(len(studies)) + " studies")
print("---------------------------------------------------------")
if not dry_run:
    print("Studies indexed equipments and tombstoned deletion processing...")
    for study in tqdm(studies):
        delete_indexed_equipments(study['id'])
    print("End of deletion")
else:
    print("nothing has been impacted (dry-run)")
   
