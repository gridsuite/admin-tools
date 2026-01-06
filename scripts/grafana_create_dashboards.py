#
# Copyright (c) 2025, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import argparse
import os

from tqdm import tqdm

from constant import GRAFANA_DASHBOARDS_DIR
from functions.grafana.dashboards import create_dashbord
from functions.grafana.folders import reset_folder, create_folder

#
# @author Slimane Amar <slimane.amar at rte-france.com>
#

parser = argparse.ArgumentParser(description='Send requests to the grafana to create or update dashboards into one folder')
group = parser.add_mutually_exclusive_group()
group.add_argument("-a", "--all", help="create all dashboards", action="store_true")
group.add_argument("-f", "--file", help="path of the dashboard to create", action='append')
parser.add_argument("-p", "--parent_folder_uuid", help="uuid of parent folder", required=True)

args = parser.parse_args()
files = args.file
root_folder_uuid = args.parent_folder_uuid

print("Grafana dashboards creation")

if args.all:
    reset_folder(root_folder_uuid)
    parent_folder_uuid = None
    for path, _, files in os.walk(GRAFANA_DASHBOARDS_DIR):
        parent_folder_uuid = root_folder_uuid if parent_folder_uuid is None else create_folder(os.path.basename(path), parent_folder_uuid)
        for file in tqdm(files):
            create_dashbord(os.path.join(path, file), parent_folder_uuid)
else:
    for file in tqdm(files):
        create_dashbord(file, root_folder_uuid)
