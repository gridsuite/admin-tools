#
# Copyright (c) 2025, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import requests
from requests import RequestException

import constant
from pathlib import Path
import json

#
# @author Slimane Amar <slimane.amar at rte-france.com>
#

GRAFANA_DASHBOARDS_URL = constant.GRAFANA_URL + "/dashboards"
DASHBOARD_CREATE_URL = GRAFANA_DASHBOARDS_URL + "/db"


def create_dashboard(dashbord_file_path, parent_folder_uid=""):
    print("Importing dashboard : " + dashbord_file_path)
    file_content = Path(dashbord_file_path).read_text()
    final_content = '{"dashboard": %s, "overwrite": true, "inputs": [], "folderUid": "%s"}' % (file_content, parent_folder_uid)
    result = None
    try:
        result = requests.post(DASHBOARD_CREATE_URL, json=json.loads(final_content), headers=constant.GRAFANA_HEADERS, cookies=constant.GRAFANA_COOKIES)
        result.raise_for_status()
        print("Dashboard imported successfully: %s" % dashbord_file_path)
    except RequestException as e:
        raise SystemExit(e, result.content)
