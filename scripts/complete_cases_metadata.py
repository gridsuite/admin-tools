#
# Copyright (c) 2025, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import requests
import argparse
import constant
import sys
from tqdm import tqdm

from functions.plateform.plateform import check_server_status
from functions.plateform.plateform import get_plateform_info
from scripts.functions.cases.cases import get_cases_with_empty_metadata
from scripts.functions.cases.cases import complete_cases_metadata

parser = argparse.ArgumentParser(description='Send requests to the gridsuite services to update cases metadata by filling missing information')
parser.add_argument("-n", "--dry-run", help="test mode (default) will not execute any update request", action='store_true')

args = parser.parse_args()
dry_run = args.dry_run

print("---------------------------------------------------------")
print("Cases metadata migration script")
if dry_run:
    print("dry-run=" + str(dry_run) + " -> will run without modifying anything (test mode)")

# Check powsybl-case-server
if not check_server_status(constant.CASE_SERVER_HOSTNAME): sys.exit()
print("\n")

# Just getting an enlightening url opportunistically from here because it exists
plateformName = get_plateform_info()['redirect_uri']
print("\n")

print("---------------------------------------------------------")
print("This script will apply on plateform = " + plateformName )
print("\n")
print("===> powsybl-case-server seems OK ! The script can proceed")
print("\n")
casesUuids = get_cases_with_empty_metadata()
print("table content : ")
print(str(casesUuids))
print("For a total of " + str(len(casesUuids)) + " casesUuids ")
print("---------------------------------------------------------")

print("cases metadata update migration (dry-run=" + str(dry_run) + ") in processing...")
failCount = 0
successCount = 0

for caseUuid in tqdm(casesUuids):
    if not dry_run:
        try:
            complete_cases_metadata(caseUuid)
            successCount += 1
        except Exception as e:
            failCount += 1
            # print only str(e) instead of the full traceback because we call this method from a simple for loop script
            tqdm.write("case " +  caseUuid +  " => migration failed: "+ str(e))
            if isinstance(e, requests.exceptions.RequestException) and e.response is not None:
                tqdm.write("Response body: " + repr(e.response.text)) # repr for cheap escaping
            tqdm.write("") # emtpy newline between errors for legibility
print("End of case metadata update migration")
print("cases migration sucesses  : " + str(successCount))
print("cases migration failures  : " + str(failCount))
