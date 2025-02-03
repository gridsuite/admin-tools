#
# Copyright (c) 2025, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import requests
import constant
#
# @author Etienne HOMER <etienne.homer at rte-france.com>
#

def get_all_cases():
    return requests.get(constant.GET_ALL_CASES).json()

def get_case(caseUuid):
    return requests.get(constant.GET_CASE.format(caseUuid = caseUuid)).content

def copy_to_s3_storage(caseUuid, caseName, case):
    files = {'file': (caseName, case)}
    return requests.post(constant.COPY_CASE, files=files, params={'caseUuid': str(caseUuid)}).json()
