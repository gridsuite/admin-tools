#
# Copyright (c) 2023, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import requests
import constant

#
# @author Sylvain Bouzols <sylvain.bouzols at rte-france.com>
#

def get_plateform_info():
    return requests.get(constant.GET_PLATEFORM_INFO).json()
