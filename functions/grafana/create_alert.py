
#
# Copyright (c) 2024, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import requests
import constant
from pathlib import Path
import json

#
# @author Kevin Le Saulnier <kevin.lesaulnier at rte-france.com>
#

FOLDER_UID_PLACEHOLDER = "{{FOLDER_UID}}"
DATASOURCE_UID_PLACEHOLDER = "{{DATASOURCE_UID}}"

def create_alert_rule(alert_rule_json_path, parent_folder_uid, datasource_uid, rule_group_interval):
    print("Importing alert-rule " + alert_rule_json_path)
    file_content = Path(alert_rule_json_path).read_text()

    file_content = file_content.replace(FOLDER_UID_PLACEHOLDER, parent_folder_uid)
    file_content = file_content.replace(DATASOURCE_UID_PLACEHOLDER, datasource_uid)

    file_content_json = json.loads(file_content)

    try:
        result = requests.post(constant.GRAFANA_ALERT_RULES, json = file_content_json, headers={'X-Disable-Provenance': 'true'})
        # grafana errors are details in request content
        result_content = result.content
        result.raise_for_status()
        print("Alert-rule imported successfuly")
    except Exception as e:
        raise SystemExit(e, result_content)


    if rule_group_interval:
        try:
            print("Updating rule-group linked to " + alert_rule_json_path + "...")
            rule_group_id = file_content_json["ruleGroup"]
            json_body = {"interval": int(rule_group_interval)}
            result = requests.put(constant.GRAFANA_RULE_GROUPS.format(folderUid = parent_folder_uid, ruleGroupId = rule_group_id), json=json_body, headers={'X-Disable-Provenance': 'true'})
            # grafana errors are details in request content
            result_content = result.content
            result.raise_for_status()
            print("Rule group updated successfuly")
        except Exception as e:
            raise SystemExit(e, result_content)
    