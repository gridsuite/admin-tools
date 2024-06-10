#
# Copyright (c) 2024, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import argparse

from functions.delete_stashed_elements.delete_stashed_elements import delete_stashed_elements
#
# @author Kevin Le Saulnier <kevin.lesaulnier at rte-france.com>
#

parser = argparse.ArgumentParser(description='Send requests to the gridsuite services to delete stashed elements', )

parser.add_argument("-n", "--dry-run", help="test mode (default) will not execute any modification request",
                    action="store_true")
                                                         

args = parser.parse_args()
dry_run = args.dry_run


if dry_run:
    print("Stashed elements deletion script will run without deleting anything (test mode)")
else:
    print("Stashed elements deletion script (exec mode)")
print("\n")

delete_stashed_elements(dry_run);
