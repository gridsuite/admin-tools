#
# Copyright (c) 2023, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import requests
import constant

#
# @author Hugo Marcellin <hugo.marcelin at rte-france.com>
# @author Sylvain Bouzols <sylvain.bouzols at rte-france.com>
#

def get_nb_indexed_equipments():
    return requests.get(constant.GET_STUDIES_INDEXED_EQUIPMENTS_COUNT).text

def get_nb_indexed_tombstoned_equipments():
    return requests.get(constant.GET_STUDIES_INDEXED_TOMBSTONED_EQUIPMENTS_COUNT).text

def get_equipments_index_name():
    try:
        return requests.get(constant.GET_STUDIES_INDEXED_EQUIPMENTS_INDEX_NAME).text
    except requests.exceptions.RequestException as e:
        print(e)
        return ""

def get_tombstoned_equipments_index_name():
    try:
        return requests.get(constant.GET_STUDIES_INDEXED_TOMBSTONED_EQUIPMENTS_INDEX_NAME).text
    except requests.exceptions.RequestException as e:
        print(e)
        return ""

def get_eleasticsearch_host():
    # TODO we force http but should get this protocol from the server, some servers are not exposed on http but only https for exemple
    # TODO use credentials because some server could have
    # TODO get elasticsearch_ip from the server for debug because only the server has the DNS to return the IP
    # we override host value in DEV otherwise study-server return 'elasticsearch:9200' as hostname
    try:
        return "localhost:9200" if constant.DEV else requests.get(constant.GET_ELASTICSEARCH_HOST).text
    except requests.exceptions.RequestException as e:
        print(e)
        return ""

def check_status_eleasticsearch(url):
    try:
        result = requests.get(url + '/')
        if not result.ok :
            # TODO this might not be a json format
            print("An error occured : " + str(result.json()))
            return False
        status = result.json()
        print("-----------------------")
        print("elasticsearch name :" + status['name'])
        print("elasticsearch cluster_name :" + status['cluster_name'])
        print("elasticsearch version :" + status['version']['number'])
        return True
    except requests.exceptions.RequestException as e:
        print("Exception during elasticsearch check status")
        print(e)
        return False


def delete_indexed_equipments(studyUuid):    
    result = requests.delete(url = constant.DELETE_STUDY_INDEXED_EQUIPMENTS.format(studyUuid = studyUuid))
    if not result.ok :
        print("An error occured : " + str(result.json()))

def expunge_deletes(elasticsearchHost, indexName):
    print("ES Force merge : " + constant.ES_FORCE_MERGE.format(elasticsearchHost = elasticsearchHost, indexName = indexName) + "?only_expunge_deletes=true")
    result = requests.post(url = constant.ES_FORCE_MERGE.format(elasticsearchHost = elasticsearchHost, indexName = indexName), params={'only_expunge_deletes': 'true'})
