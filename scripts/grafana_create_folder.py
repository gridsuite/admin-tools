#
# Copyright (c) 2024, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import argparse

from functions.grafana.create_folder import create_folder

#
# @author Kevin Le Saulnier <kevin.lesaulnier at rte-france.com>
#
parser = argparse.ArgumentParser(description='Send requests to the grafana to create folder', )
parser.add_argument("foldername", help="name of the folder to create")

args = parser.parse_args()
folder_name_to_create = args.foldername

print("Grafana folder creation script")

create_folder(folder_name_to_create)
