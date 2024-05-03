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

def get_eleasticsearch_host():
    # TODO use credentials because some server could have
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

def expunge_deletes(elasticsearchHost, indexName):
    print("ES Force merge : " + constant.ES_FORCE_MERGE.format(elasticsearchHost = elasticsearchHost, indexName = indexName) + "?only_expunge_deletes=true")
    result = requests.post(url = constant.ES_FORCE_MERGE.format(elasticsearchHost = elasticsearchHost, indexName = indexName), params={'only_expunge_deletes': 'true'})
