#
# Copyright (c) 2024, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import requests
import constant

#
# @author Kevin Le Saulnier <kevin.lesaulnier at rte-france.com>
#

def create_folder(folder_name):
    folder_data = {"title": folder_name}
    try:
        result = requests.post(constant.GRAFANA_FOLDER, json = folder_data)
        result_content = result.content
        # grafana errors are details in request content
        result.raise_for_status()

        print("Folder successfuly created : ")
        print(result_content)
    except Exception as e:
        raise SystemExit(e, result_content)
