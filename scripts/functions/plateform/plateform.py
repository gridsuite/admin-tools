#
# Copyright (c) 2023, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import requests
import constant

from ..utils import prettyprint


#
# @author Sylvain Bouzols <sylvain.bouzols at rte-france.com>
#

def get_plateform_info():
    return requests.get(constant.GET_PLATEFORM_INFO).json()


def check_server_status(serverHostName):
    try:
        result = requests.get(constant.GET_ACTUATOR_INFO.format(serverHostName = serverHostName))

        if not result.ok :
            print("An error occured : ")
            prettyprint(result)
            return False
        status = result.json()
        print("-----------------------")
        print(serverHostName + " describe-short : " + status['git']['commit']['id']['describe-short'])
        print(serverHostName + " name : " + status['build']['name'])
        print(serverHostName + " version : " + status['build']['version'])
        return True
    except requests.exceptions.RequestException as e:
        print("Exception during " + serverHostName + " check status")
        print(e)
        return False
