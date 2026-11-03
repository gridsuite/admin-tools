#
# Copyright (c) 2026, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import argparse
import re
from datetime import datetime, timedelta, timezone
from uuid import UUID

import requests
import constant

parser = argparse.ArgumentParser(description="Delete old elements from a directory")
parser.add_argument("directory_uuid", type=UUID, help="UUID of the directory to clean")
parser.add_argument("--older-than-hours", type=int, required=True,
                    help="delete elements created more than this many hours ago")
parser.add_argument("-n", "--dry-run", help="test mode: will not execute any deletion request",
                    action="store_true")
args = parser.parse_args()
if args.older_than_hours <= 0:
    parser.error("--older-than-hours must be a positive integer")
dry_run = args.dry_run

if dry_run:
    print("The script will run without deleting anything (dry run mode)")
if constant.DEV:
    print(f"DEV={constant.DEV} -> hostnames configured for a local execution (172.17.0.1:xxxx)")

headers = {"userId": "cleanup-directory-elements", "roles": "ADMIN_EXPLORE"}
cutoff = datetime.now(timezone.utc) - timedelta(hours=args.older_than_hours)

directory_id = args.directory_uuid
print(f"Getting elements from directory {directory_id} on explore-server")
elements_response = requests.get(
    constant.GET_EXPLORE_DIRECTORY_ELEMENTS.format(directoryUuid=directory_id),
    headers=headers, timeout=60)
elements_response.raise_for_status()
elements = elements_response.json()
expired_ids = []
for element in elements:
    if element["type"] == "DIRECTORY":
        continue
    # Python 3.8 cannot parse Java Instant's nanosecond precision.
    timestamp = re.sub(r"(\.\d{6})\d+", r"\1", element["creationDate"])
    created = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    if created < cutoff:
        expired_ids.append(str(UUID(element["elementUuid"])))

for start in range(0, len(expired_ids), 50):
    ids = expired_ids[start:start + 50]
    if dry_run:
        print(f"Would request deletion of elements: {','.join(ids)}")
    else:
        response = requests.delete(
            constant.DELETE_EXPLORE_ELEMENTS.format(directoryUuid=directory_id),
            params={"ids": ids}, headers=headers, timeout=60)
        response.raise_for_status()
        print(f"Requested deletion of elements: {','.join(ids)}")
if dry_run:
    print(f"Dry run: {len(expired_ids)} elements older than {args.older_than_hours}h would be deleted")
else:
    print(f"Requested deletion of {len(expired_ids)} elements older than {args.older_than_hours}h")
