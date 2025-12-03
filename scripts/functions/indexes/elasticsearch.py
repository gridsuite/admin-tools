#
# Copyright (c) 2024, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
import os
import requests
import constant
import socket

from requests.auth import HTTPBasicAuth
from ..utils import prettyprint


#
# @author Sylvain Bouzols <sylvain.bouzols at rte-france.com>
#

def get_elasticsearch_host(serverHostName):
    # TODO use credentials because some server could have
    # we override host value in DEV otherwise services return 'elasticsearch:9200' as hostname
    try:
        if constant.DEV :
            return constant.DEV_ELASTICSEARCH_IP, constant.DEV_ELASTICSEARCH_URL 
        else:
            if constant.DEV:
                elasticsearch_host = requests.get(constant.GET_ELASTICSEARCH_HOST.format(serverHostName = serverHostName), auth=__get_authentification()).text
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


def __get_authentification():
    login = os.environ['ELASTICSEARCH_LOGIN']
    password = os.environ['ELASTICSEARCH_PASSWORD']
    return HTTPBasicAuth(login, password)


def check_status_elasticsearch(url):
    try:
        if constant.DEV:
            result = requests.get(url + '/', auth=__get_authentification())
        else:
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
        if constant.DEV:
            result = requests.request(method, url, auth=__get_authentification())
        else:
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
    if constant.DEV:
        requests.post(url = constant.ES_FORCE_MERGE.format(elasticsearchHost = elasticsearchHost, indexName = indexName), params={'only_expunge_deletes': 'true'}, auth=__get_authentification())
    else:
        requests.post(url=constant.ES_FORCE_MERGE.format(elasticsearchHost=elasticsearchHost, indexName=indexName), params={'only_expunge_deletes': 'true'})
