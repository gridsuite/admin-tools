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

def get_all_orphan_indexed_equipments_network_uuids():
    return requests.get(constant.GET_ALL_ORPHAN_INDEXED_EQUIPMENTS_NETWORK_UUIDS).json()

def delete_indexed_equipments(networkUuid):
    try:
        result = requests.delete(url = constant.DELETE_STUDY_INDEXED_EQUIPMENTS_BY_NETWORK_UUID.format(networkUuid = networkUuid))

        # Check if the response status code indicates success
        if result.status_code == 200:
            print(f"Successfully deleted indexed equipments for network UUID: {networkUuid}")
            return True
        else:
            print(f"Failed to delete indexed equipments for network UUID: {networkUuid}. "
                  f"Response status code: {result.status_code} - Response content: {result.content}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Exception occurred while deleting indexed equipments for network UUID: {networkUuid}. Exception: {e}")
        return False

def invalidate_nodes_builds(studyUuid):
    return requests.delete(constant.DELETE_STUDY_NODES_BUILDS.format(studyUuid = studyUuid))

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
    
