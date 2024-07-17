#
# Copyright (c) 2024, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import argparse
import constant
import sys

from functions.indexes.elasticsearch import get_elasticsearch_host
from functions.indexes.elasticsearch import check_status_elasticsearch
from functions.indexes.elasticsearch import request_elasticsearch
from functions.plateform.plateform import get_plateform_info

#
# @author Sylvain Bouzols <sylvain.bouzols at rte-france.com>
#

# Elastic REST API
# i.e. https://www.elastic.co/guide/en/elasticsearch/reference/current/rest-apis.html

parser = argparse.ArgumentParser(description='Send requests (REST APIs) to the ES server', )
     
parser.add_argument("-m", "--method", help="HTTP method to use for the request (e.g., GET, POST)", required=True)
parser.add_argument("-u", "--url", help="request url to execute on ES server", required=True)
                                                  
args = parser.parse_args()
request_method = args.method
request_url = args.url

print("---------------------------------------------------------")
print("ES request script")

print("\n")
# Just getting an enlightening url opportunistically from here because it exists
# TODO better ?
plateformName = get_plateform_info()['redirect_uri']
elasticsearch_ip, elasticsearch_url = get_elasticsearch_host(constant.DIRECTORY_SERVER_HOSTNAME)

if not check_status_elasticsearch(elasticsearch_url) : sys.exit()
print("\n")

print("---------------------------------------------------------")
print("This script will apply on plateform = " + plateformName )
# TODO It would be nice to show the environment prefix used for elasticsearch indexes names 
print("This plateform will execute queries on elasticsearch = " + elasticsearch_url + " (" + elasticsearch_ip + ")")
print("\n")
print("===> Elasticsearch seems OK ! The script can proceed")
print("\n")
print("---------------------------------------------------------")
print("Elasticsearch request processing...")
request_elasticsearch(request_method, elasticsearch_url + request_url)
print("End of request")
