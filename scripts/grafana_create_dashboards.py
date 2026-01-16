#
# Copyright (c) 2025, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import argparse
import os

from click import UUID
from tqdm import tqdm

from functions.grafana.dashboards import create_dashboard
from functions.grafana.folders import reset_folder, create_folder

#
# @author Slimane Amar <slimane.amar at rte-france.com>
#
GRAFANA_DASHBOARDS_DIR = 'resources/grafana/dashboards'

parser = argparse.ArgumentParser(description='Send requests to the grafana to create or update dashboards into one folder')
group = parser.add_mutually_exclusive_group()
group.add_argument("-a", "--all", help="create all dashboards", action="store_true")
group.add_argument("-f", "--file", help="path of the dashboard to create", action='append')
parser.add_argument("-p", "--parent_folder_uid", help="uid of parent folder", required=True)

args = parser.parse_args()
files = args.file
root_folder_uid = args.parent_folder_uid

print("Grafana dashboards creation")

if args.all:
    reset_folder(root_folder_uid)
    folders_uids = { GRAFANA_DASHBOARDS_DIR : root_folder_uid }
    parent_folder_uid = None
    for path, subdirs, files in os.walk(GRAFANA_DASHBOARDS_DIR):
        parent_folder_uid = folders_uids.get(path)
        for subdir in subdirs:
            folders_uids[os.path.join(path, subdir)] = create_folder(subdir, parent_folder_uid, recreate=True)
        for file in files:
            create_dashboard(os.path.join(path, file), parent_folder_uid)
else:
    for file in files:
        create_dashboard(file, root_folder_uid)
