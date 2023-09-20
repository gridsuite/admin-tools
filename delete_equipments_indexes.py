#
# Copyright (c) 2023, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import argparse
import constant
from functions.indexes import indexes 

#
# @author Hugo Marcellin <hugo.marcelin at rte-france.com>
#

parser = argparse.ArgumentParser(description='Send requests to the gridsuite services to delete studies equipments indexes', )

parser.add_argument("-n", "--dry-run", help="test mode (default) will not execute any deletion request",
                    action="store_true")                                                          

if dry_run:
    print("Studies equipments indexes deletion script will run without deleting anything (test mode)")
else:
    print("Studies equipments indexes deletion script (exec mode)")
print("\n")

delete_computation_results(dry_run, constant.LOADFLOW)    
