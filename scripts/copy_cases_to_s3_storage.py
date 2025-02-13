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

from functions.plateform.plateform import get_plateform_info
from functions.plateform.plateform import check_server_status
from functions.cases.cases import get_all_cases, get_case, copy_to_s3_storage

#
# @author Etienne Homer <etienne.homer at rte-france.com>
#

parser = argparse.ArgumentParser(description='Send requests to the gridsuite services to copy cases to the s3 storage', )

parser.add_argument("-n", "--dry-run", help="test mode (default) will not execute any deletion request",
                    action="store_true")


args = parser.parse_args()
dry_run = args.dry_run

print("---------------------------------------------------------")
print("Copy cases to the s3 storage script")
if dry_run:
    print("dry-run=" + str(dry_run) + " -> will run without modifying anything (test mode)")
if constant.DEV:
    print("DEV=" + str(constant.DEV) + " -> hostnames configured for a local execution (172.17.0.1:xxxx)")
print("\n")

# Check case-server
if not check_server_status(constant.CASE_SERVER_HOSTNAME): sys.exit()
print("\n")
# Just getting an enlightening url opportunistically from here because it exists
plateformName = get_plateform_info()['redirect_uri']

print("\n")

print("---------------------------------------------------------")
print("This script will apply on plateform = " + plateformName )
print("\n")
print("===> case-server seems OK ! The script can proceed")
print("\n")
cases = get_all_cases()
print("For a total of " + str(len(cases)) + " cases")
print("---------------------------------------------------------")

print("Cases copy (dry-run=" + str(dry_run) + ") in processing...")
fails_count = 0
cases_migrated_count = 0
already_migrated_count = 0
for caseInfos in tqdm(cases):
    try:
        case = get_case(caseInfos['uuid'])
        copy_to_s3_storage(caseInfos['uuid'], caseInfos['name'], case);
        cases_migrated_count += 1
    except Exception as e:
        if isinstance(e, requests.exceptions.RequestException) and e.response is not None and e.response.status_code == 409:
            already_migrated_count += 1
        else:
            fails_count += 1
            # print only str(e) instead of the full traceback because we call this method from a simple for loop script
            tqdm.write(
                "Case " + caseInfos['uuid'] + " => copy failed: " + str(e))
            if isinstance(e, requests.exceptions.RequestException) and e.response is not None:
                tqdm.write("Response body: " + repr(e.response.text))  # repr for cheap escaping
            tqdm.write("")  # emtpy newline between errors for legibility
print("End of cases copy to s3 storage")
print("Case copy sucesses  : " + str(cases_migrated_count))
print("Cases already migrated  : " + str(already_migrated_count))
print("Case copy failures  : " + str(fails_count))
