#
# Copyright (c) 2024, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import requests
import constant

#
# @author Sylvain Bouzols <sylvain.bouzols at rte-france.com>
#

def get_all_directories_uuid():
    return requests.get(constant.GET_DIRECTORIES).json()

