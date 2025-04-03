#
# Copyright (c) 2025, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
from simplejson import dumps, JSONDecodeError


#
# @author Antoine Bouhours <antoine.bouhours at rte-france.com>
#

def prettyprint(result):
    try:
        pretty = dumps(result.json(), indent=2)
        print(pretty)
    except JSONDecodeError:
        print('Response could not be JSON serialized')
        print(result.text) # try to print text if not JSON serialized
