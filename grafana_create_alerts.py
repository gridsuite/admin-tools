#
# Copyright (c) 2024, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import argparse

from functions.grafana.create_alert import create_alert_rule

#
# @author Kevin Le Saulnier <kevin.lesaulnier at rte-france.com>
#
parser = argparse.ArgumentParser(description='Send requests to the grafana to create alert-rules into one folder - rule-groups are automatically created if not already existing')
parser.add_argument("-f", "--file", help="path of the alert rule to create", required=True, action='append')
parser.add_argument("-p", "--parent_folder_uuid", help="uuid of parent folder", required=True)
parser.add_argument("-d", "--datasource_uuid", help="uuid of datasource", required=True)
parser.add_argument("-i", "--interval", help="(seconds) - after successfuly creating the alert-rule, its rule-group interval (newly created or not) will be updated with this value. Newly created rule-group will have an interval set to Grafana default value (60s) if left empty")

args = parser.parse_args()
files = args.file
parent_folder_uuid = args.parent_folder_uuid
datasource_uuid = args.datasource_uuid
rule_group_interval = args.interval

print("Grafana alert rule creation script")

for file in files:
    create_alert_rule(file, parent_folder_uuid, datasource_uuid, rule_group_interval)