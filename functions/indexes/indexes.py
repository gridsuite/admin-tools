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

def delete_equipments_indexes(dry_run):
    print("/// Studies equipments indexes deletion ///")
    if dry_run: 
        resultsCount = requests.delete(constant.DELETE_STUDIES_EQUIPMENTS_INDEXES, params={"dryRun": "true"})
        print("Here's the count of stored indexes : " + str(resultsCount.json()))
    else :
        result = requests.delete(constant.DELETE_STUDIES_EQUIPMENTS_INDEXES, params={"dryRun": "false"})
        if result.ok :
            print("Here's the count of deleted equipment indexes : " + str(result.json()))
        else :
            print("An error occured : " + str(result.json()))