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

from functions.networks.networks import get_all_networks_uuid
from functions.networks.networks import get_variants
from functions.networks.networks import migrate_v211_limits
from functions.plateform.plateform import get_plateform_info
from functions.plateform.plateform import check_server_status

#
# @author Etienne Homer <etienne.homer at rte-france.com>
#

parser = argparse.ArgumentParser(description='Send requests to the gridsuite services to migrate V2.11 limits', )

parser.add_argument("-n", "--dry-run", help="test mode (default) will not execute any deletion request",
                    action="store_true")


args = parser.parse_args()
dry_run = args.dry_run

print("---------------------------------------------------------")
print("V2.11 limits migration script")
if dry_run:
    print("dry-run=" + str(dry_run) + " -> will run without modifying anything (test mode)")
if constant.DEV:
    print("DEV=" + str(constant.DEV) + " -> hostnames configured for a local execution (172.17.0.1:xxxx)")
print("\n")

# Check network-store-server
if not check_server_status(constant.NETWORK_STORE_SERVER_HOSTNAME): sys.exit()
print("\n")
# Just getting an enlightening url opportunistically from here because it exists
plateformName = get_plateform_info()['redirect_uri']

print("\n")

print("---------------------------------------------------------")
print("This script will apply on plateform = " + plateformName )
print("\n")
print("===> network-store-server seems OK ! The script can proceed")
print("\n")
networks = get_all_networks_uuid()
print("For a total of " + str(len(networks)) + " networks")
print("---------------------------------------------------------")

print("V2.11 limits migration (dry-run=" + str(dry_run) + ") in processing...")
failCount = 0
successCount = 0
for network in tqdm(networks):
    variants = get_variants(network['uuid'])
    for variant in variants:
        if not dry_run:
            try:
                migrate_v211_limits(network['uuid'], variant['num'])
                successCount += 1
            except Exception as e:
                failCount += 1
                # print only str(e) instead of the full traceback because we call this method from a simple for loop script
                tqdm.write("network " + network['uuid'] + ", variantNum " + str(variant['num']) + " => migration failed: "+ str(e))
                if isinstance(e, requests.exceptions.RequestException) and e.response is not None:
                    tqdm.write(f"Response body: {e.response.text}".replace('\r\n','').replace('\n',''))
                tqdm.write("") # emtpy newline between errors for legibility
print("End of V2.11.0 limits migration")
print("Variant migration sucesses  : " + str(successCount))
print("Variant migration failures  : " + str(failCount))
