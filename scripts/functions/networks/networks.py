#
# Copyright (c) 2025, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import requests
import constant
#
# @author Etienne Homer <etienne.homer at rte-france.com>
#

def get_all_networks_uuid():
    return requests.get(constant.GET_NETWORKS).json()

def get_variants(networkId):
    return requests.get(constant.GET_NETWORK.format(networkId = networkId)).json()

def migrate_v211_limits(networkId, variantNum):
    result = requests.put(constant.MIGRATE_V211_LIMITS.format(networkId = networkId, variantNum = variantNum))
    if result.ok :
        print("network " + networkId + "/variantNum=" + str(variantNum) + " => migration OK.")
    else :
        print("network " + networkId + "/variantNum=" + str(variantNum) + " => migration failed.")
