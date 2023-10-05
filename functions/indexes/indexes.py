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
#

def delete_indexed_equipments(dry_run):
    print("/// Studies indexed equipments and tombstoned deletion ///")
    if dry_run: 
        resultsCount = requests.delete(constant.DELETE_STUDIES_INDEXED_EQUIPMENTS, params={"dryRun": "true"})
        print("Here's the count of stored indexed equipments and tombstoned : " + str(resultsCount.json()))
    else :
        result = requests.delete(constant.DELETE_STUDIES_INDEXED_EQUIPMENTS, params={"dryRun": "false"})
        if result.ok :
            print("Here's the count of deleted indexed equipments and tombstoned : " + str(result.json()))
        else :
            print("An error occured : " + str(result.json()))
