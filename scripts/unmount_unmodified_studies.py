#
# Copyright (c) 2026, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import sys
import requests
import constant
from functions.studies.studies import unmount_study

#
# Invalidates built nodes and delete initial variant network for all studies that have not been modified since a given duration.
#
# Usage:
#   python unmount_unmodified_studies.py <duration> [--dry-run] [--limit <n>]
#
# Arguments:
#   duration              ISO 8601 duration (e.g. P365D for 1 year, P30D for 30 days, PT24H for 24 hours)
#   --dry-run             Optional flag to only list affected studies without performing any invalidation
#   --limit <n>      Optional maximum number of studies to process
#
# Example:
#   python unmount_unmodified_studies.py P365D --dry-run
#   python unmount_unmodified_studies.py P365D --limit 10 --dry-run
#

#
# @author Hugo Marcellin <hugo.marcellin_externe at rte-france.com>
#

def get_unmodified_studies(duration):
    response = requests.get(constant.GET_UNMODIFIED_DIRECTORY_ELEMENTS, params={"elementType": "STUDY", "duration": duration})
    response.raise_for_status()
    return response.json()

def unmount_unmodified_studies(duration, dry_run=False, limit=None):
    print(f"Fetching studies not modified since {duration}...")
    studies = get_unmodified_studies(duration)

    if not studies:
        print("No unmodified studies found.")
        return

    print(f"Found {len(studies)} unmodified study/studies.")

    if limit is not None and limit < len(studies):
        print(f"Limit applied: processing {limit} out of {len(studies)} studies.")
        studies = studies[:limit]

    print("Selected studies:")
    for study in studies:
        print(f"  - {study['elementUuid']} | {study['elementName']} | last modified: {study['lastModificationDate']}")

    if dry_run:
        print("\nDry run mode: no study will be unmounted.")
        return

    if constant.DEV:
        print(f"\nDEV={str(constant.DEV)} -> hostnames configured for a local execution (172.17.0.1:xxxx)")

    print("\nUnmounting studies...")
    success_count = 0
    failure_count = 0
    for study in studies:
        study_uuid = study["elementUuid"]
        result = unmount_study(study_uuid)
        if result.status_code == 200:
            print(f"  OK - {study_uuid}")
            success_count += 1
        else:
            print(f"  FAILED - {study_uuid} (status: {result.status_code})")
            failure_count += 1

    print(f"\nDone. {success_count} succeeded, {failure_count} failed.")


if len(sys.argv) < 1:
    print("Usage: python unmount_unmodified_studies.py <duration> [--dry-run] [--limit <n>]")
    print("Example: python unmount_unmodified_studies.py P365D --limit 10 --dry-run")
    sys.exit(1)

duration_arg = sys.argv[1]
dry_run_arg = "--dry-run" in sys.argv

limit_arg = None
if "--limit" in sys.argv:
    limit_index = sys.argv.index("--limit")
    if limit_index + 1 >= len(sys.argv):
        print("Error: --limit requires a numeric value.")
        sys.exit(1)
    try:
        limit_arg = int(sys.argv[limit_index + 1])
        if limit_arg <= 0:
            raise ValueError
    except ValueError:
        print("Error: --limit must be a positive integer.")
        sys.exit(1)

unmount_unmodified_studies(duration_arg, dry_run=dry_run_arg, limit=limit_arg)
