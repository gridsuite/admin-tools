#
# Copyright (c) 2024, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import argparse
import os

from functions.grafana.alerts import create_alert_rule

#
# @author Kevin Le Saulnier <kevin.lesaulnier at rte-france.com>
# @author Slimane Amar <slimane.amar at rte-france.com>
#
GRAFANA_ALERTS_DIR = 'resources/grafana/alerts/'
GRAFANA_LOGS_ALERTS_DIR = GRAFANA_ALERTS_DIR + 'logs'
GRAFANA_METRICS_ALERTS_DIR = GRAFANA_ALERTS_DIR + 'metrics'

parser = argparse.ArgumentParser(description='Send requests to the grafana to create alert-rules into one folder - rule-groups are automatically created if not already existing')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-l", "--logs", help="create all alert rules for logs (datasource loki)", action="store_true")
group.add_argument("-m", "--metrics", help="create all alert rules for metrics (datasource prometheus)", action="store_true")
group.add_argument("-f", "--file", help="path of the alert rule to create", action='append')
parser.add_argument("-p", "--parent_folder_uid", help="uid of parent folder", required=True)
parser.add_argument("-d", "--datasource_uid", help="uid of datasource (loki or prometheus)", required=True)

args = parser.parse_args()
files = args.file
root_folder_uid = args.parent_folder_uid
datasource_uid = args.datasource_uid

print("Grafana alert rules creation")

if args.logs or args.metrics:
    for path, _, files in os.walk(GRAFANA_LOGS_ALERTS_DIR if args.logs else GRAFANA_METRICS_ALERTS_DIR):
        for file in files:
            print("")
            create_alert_rule(os.path.join(path, file), root_folder_uid, datasource_uid, overwrite=True)
else:
    for file in files:
        create_alert_rule(file, root_folder_uid, datasource_uid)
