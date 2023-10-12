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

def get_all_studies_uuid():
    return requests.get(constant.GET_STUDIES).json()

def check_status_study_server():
    try:
        result = requests.get(constant.GET_ACTUATOR_INFO)

        if not result.ok :
            # TODO this might not be a json format
            print("An error occured : " + str(result.json()))
            return False
        status = result.json()
        print("-----------------------")
        print("study-server describe-short : " + status['git']['commit']['id']['describe-short'])
        print("study-server name : " + status['build']['name'])
        print("study-server version : " + status['build']['version'])
        return True
    except requests.exceptions.RequestException as e:
        print("Exception during study-server check status")
        print(e)
        return False
    
