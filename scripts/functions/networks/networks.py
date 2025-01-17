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

def get_variants(network_id):
    return requests.get(constant.GET_NETWORK.format(networkId = network_id)).json()

def migrate_v211_limits(network_id, variant_num):
        response = requests.put(constant.MIGRATE_V211_LIMITS.format(networkId = network_id, variantNum = variant_num))
        response.raise_for_status()
