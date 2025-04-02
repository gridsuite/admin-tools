#
# Copyright (c) 2024, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import requests
import constant
import socket
from simplejson import JSONDecodeError
from simplejson import dumps

#
# @author Sylvain Bouzols <sylvain.bouzols at rte-france.com>
#

def prettyprint(result):
    try:
        # TODO this might not be a json format
        pretty = dumps(result.json(), indent=2)
        print(pretty)
    except JSONDecodeError:
        print('Response could not be JSON serialized')
        print(result.text) # try to print text if not JSON serialized

def get_elasticsearch_host(serverHostName):
    # TODO use credentials because some server could have
    # we override host value in DEV otherwise services return 'elasticsearch:9200' as hostname
    try:
        if constant.DEV :
            return constant.DEV_ELASTICSEARCH_IP, constant.DEV_ELASTICSEARCH_URL 
        else:
            elasticsearch_host = requests.get(constant.GET_ELASTICSEARCH_HOST.format(serverHostName = serverHostName)).text
            # TODO don't parse here, instead have the server return structured information
            elasticsearch_ip = socket.gethostbyname(elasticsearch_host.split(':')[0])
            # TODO we force http but should get this protocol from the server, some servers are not exposed on http but only https for example
            elasticsearch_url = constant.HTTP_PROTOCOL + elasticsearch_host
            return elasticsearch_ip, elasticsearch_url
    except requests.exceptions.RequestException as e:
        print(e)
        return ""

def check_status_elasticsearch(url):
    try:
        result = requests.get(url + '/')
        if not result.ok :
            print("An error occured : ")
            prettyprint(result)
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

def request_elasticsearch(method, url):
    try:
        print(method + " " + url)
        result = requests.request(method, url)
        if not result.ok :
            print("An error occured : ")
            prettyprint(result)
            return False
        print("-----------------------")
        prettyprint(result)
        return True
    except requests.exceptions.RequestException as e:
        print("Exception during elasticsearch request")
        print(e)
        return False

def expunge_deletes(elasticsearchHost, indexName):
    print("ES Force merge : " + constant.ES_FORCE_MERGE.format(elasticsearchHost = elasticsearchHost, indexName = indexName) + "?only_expunge_deletes=true")
    result = requests.post(url = constant.ES_FORCE_MERGE.format(elasticsearchHost = elasticsearchHost, indexName = indexName), params={'only_expunge_deletes': 'true'})
