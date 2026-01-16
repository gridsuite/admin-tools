#
# Copyright (c) 2024, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public

import json
from pathlib import Path

import requests
from requests import RequestException

import constant

#
# @author Kevin Le Saulnier <kevin.lesaulnier at rte-france.com>
# @author Slimane Amar <slimane.amar at rte-france.com>
#
GRAFANA_API_VERSION = "/v1"
GRAFANA_PROVISIONING_URL = constant.GRAFANA_URL + GRAFANA_API_VERSION + "/provisioning"
GRAFANA_ALERT_RULES_URL = GRAFANA_PROVISIONING_URL + "/alert-rules"
GRAFANA_ALERT_RULE_URL = GRAFANA_ALERT_RULES_URL + "/{alertRuleUuid}"
GRAFANA_RULE_GROUPS_URL = GRAFANA_PROVISIONING_URL + "/folder/{folderUid}/rule-groups/{ruleGroupId}"

FOLDER_UID_PLACEHOLDER = "{{FOLDER_UID}}"
DATASOURCE_UID_PLACEHOLDER = "{{DATASOURCE_UID}}"

EVALUATION_GROUP_INTERVALS_IN_SECONDS = {'alert_eval_group_10s': 10, 'alert_eval_group_30s': 30, 'alert_eval_group_1m': 60, 'alert_eval_group_5m': 300}


def create_alert_rule(alert_rule_json_path, parent_folder_uid, datasource_uid, overwrite=False):
    print("Importing alert rule " + alert_rule_json_path)
    file_content = Path(alert_rule_json_path).read_text()
    file_content = file_content.replace(FOLDER_UID_PLACEHOLDER, parent_folder_uid)
    file_content = file_content.replace(DATASOURCE_UID_PLACEHOLDER, datasource_uid)
    alert_rule_json = json.loads(file_content)
    if overwrite:
        delete_alert_rule(alert_rule_json['uid'])
    __create_alert_rule(parent_folder_uid, alert_rule_json_path, alert_rule_json)

def __create_alert_rule(parent_folder_uid, alert_rule_json_path, alert_rule_json):
    print("Importing alert rule " + alert_rule_json_path)
    result = None
    try:
        rule_group_id = alert_rule_json["ruleGroup"]
        rule_group_interval = __get_evaluation_group_interval(rule_group_id)
        result = requests.post(GRAFANA_ALERT_RULES_URL, json=alert_rule_json,
                               headers=constant.GRAFANA_HEADERS, cookies=constant.GRAFANA_COOKIES)
        result.raise_for_status()
        print("Alert rule imported successfully: %s" % alert_rule_json_path)
        __update_interval_alert_group(parent_folder_uid, rule_group_id, rule_group_interval)
    except RequestException as e:
        raise SystemExit(e, result.content)

def __get_evaluation_group_interval(get_rule_group_id):
    rule_group_interval = EVALUATION_GROUP_INTERVALS_IN_SECONDS.get(get_rule_group_id)
    if rule_group_interval is None:
        error_message = "Unknown rule group name : %s" % get_rule_group_id + "\nRule group valid names : %s" % list(EVALUATION_GROUP_INTERVALS_IN_SECONDS)
        raise SystemExit(error_message)
    return rule_group_interval


def __update_interval_alert_group(parent_folder_uid, rule_group_id, rule_group_interval):
    result = None
    try:
        print("Updating '%s' rule group interval with value : %s" % (rule_group_id, rule_group_interval))
        json_body = {"interval": int(rule_group_interval)}
        result = requests.put(GRAFANA_RULE_GROUPS_URL.format(folderUid=parent_folder_uid, ruleGroupId=rule_group_id),
                              json=json_body,
                              headers=constant.GRAFANA_HEADERS, cookies=constant.GRAFANA_COOKIES)
        result.raise_for_status()
        print("Rule group interval updated successfully : %s" % rule_group_id)
    except RequestException as e:
        raise SystemExit(e, result.content)

def delete_alert_rule(alert_rule_uuid):
    result = None
    try:
        result = requests.get(GRAFANA_ALERT_RULE_URL.format(alertRuleUuid=alert_rule_uuid), headers=constant.GRAFANA_HEADERS, cookies=constant.GRAFANA_COOKIES)
        if result.status_code == requests.codes.not_found:
            return
        result.raise_for_status()
        result = requests.delete(GRAFANA_ALERT_RULE_URL.format(alertRuleUuid=alert_rule_uuid), headers=constant.GRAFANA_HEADERS, cookies=constant.GRAFANA_COOKIES)
        result.raise_for_status()
        print("Alert rule successfully deleted : %s" % alert_rule_uuid)
    except RequestException as e:
        raise SystemExit(e, result.content)