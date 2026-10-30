#
# Copyright (c) 2026, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import argparse
import constant
import sys
from tqdm import tqdm

from functions.plateform.plateform import check_server_status
from functions.plateform.plateform import get_plateform_info
from functions.studies.studies import get_all_studies_uuid, recreate_network_modifications_sharing_links

#
# @author Sylvain Bouzols <sylvain.bouzols at rte-france.com>
#

parser = argparse.ArgumentParser(description='Send requests to the gridsuite services to recreate network modifications sharing links', )

parser.add_argument("-n", "--dry-run", help="test mode (default) will not execute any deletion or saving request",
                    action="store_true")

args = parser.parse_args()
dry_run = args.dry_run

print("---------------------------------------------------------")
print("Network modifications sharing links recreation script")
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

print("\n")

print("---------------------------------------------------------")
print("This script will apply on plateform = " + plateformName )
print("\n")
print("===> study-server seems OK ! The script can proceed")
print("\n")
studies = get_all_studies_uuid()
print("For a total of " + str(len(studies)) + " studies")
print("---------------------------------------------------------")
if not dry_run:
    print("Network modifications sharing links recreation processing...")
    for study in tqdm(studies):
        recreate_network_modifications_sharing_links(study['id'])
    print("End of recreation")
else:
    print("Nothing has been impacted (dry-run)")

