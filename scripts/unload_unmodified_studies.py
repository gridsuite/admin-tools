#
# Copyright (c) 2026, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import sys
import time
import requests
import constant
from functions.studies.studies import get_loaded_studies_uuids, unload_study
from tqdm import tqdm

#
# Invalidates built nodes and delete initial variant network for all studies that have not been modified since a given duration
# and whose at least one root network is still loaded.
#
# Usage:
#   python unload_unmodified_studies.py <duration> [--dry-run] [--limit <n>] [--delay <seconds>]
#
# Arguments:
#   duration              ISO 8601 duration (e.g. P365D for 1 year, P30D for 30 days, PT24H for 24 hours)
#   --dry-run             Optional flag to only list affected studies without performing any invalidation
#   --limit <n>           Optional maximum number of studies to process
#   --delay <seconds>     Optional delay in seconds between each study invalidation request (e.g. 1, 2, 60, 120)
#
# Example:
#   python unload_unmodified_studies.py P365D --dry-run
#   python unload_unmodified_studies.py P365D --limit 10 --dry-run
#   python unload_unmodified_studies.py P365D --limit 10 --delay 2
#

#
# @author Hugo Marcellin <hugo.marcellin_externe at rte-france.com>
#

if len(sys.argv) < 2:
    print("Usage: python unload_unmodified_studies.py <duration> [--dry-run] [--limit <n>] [--delay <seconds>]")
    print("Example: python unload_unmodified_studies.py P365D --limit 10 --delay 1.5 --dry-run")
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

delay_arg = None
if "--delay" in sys.argv:
    delay_index = sys.argv.index("--delay")
    if delay_index + 1 >= len(sys.argv):
        print("Error: --delay requires a numeric value.")
        sys.exit(1)
    try:
        delay_arg = float(sys.argv[delay_index + 1])
        if delay_arg < 0:
            raise ValueError
    except ValueError:
        print("Error: --delay must be a non-negative number.")
        sys.exit(1)


def get_unmodified_studies(duration):
    response = requests.get(constant.GET_UNMODIFIED_DIRECTORY_ELEMENTS, params={"elementType": "STUDY", "duration": duration})
    response.raise_for_status()
    return response.json()

def filter_loaded_studies(studies):
    loaded_uuids = set(get_loaded_studies_uuids([study['elementUuid'] for study in studies]))
    return [study for study in studies if study['elementUuid'] in loaded_uuids]

def unload_unmodified_studies(duration, dry_run=False, limit=None, delay=None):
    if constant.DEV:
        print(f"\nDEV={str(constant.DEV)} -> hostnames configured for a local execution (172.17.0.1:xxxx)")

    print(f"Fetching studies not modified since {duration}...")
    studies = get_unmodified_studies(duration)

    if not studies:
        print("No unmodified studies found.")
        return

    print(f"Found {len(studies)} unmodified study/studies.")

    studies = filter_loaded_studies(studies)
    print(f"Among them, {len(studies)} are still loaded and are candidates for invalidation.")

    if not studies:
        return

    if limit is not None and limit < len(studies):
        print(f"Limit applied: processing {limit} out of {len(studies)} studies.")
        studies = studies[:limit]

    print("Selected studies:")
    for study in studies:
        print(f"  - {study['elementUuid']} | {study['elementName']} | last modified: {study['lastModificationDate']}")

    if dry_run:
        print("\nDry run mode: no study will be unloaded.")
        return

    if delay is not None:
        print(f"\nDelay between requests: {delay}s")

    print("\nnUnloading studies...")
    success_count = 0
    failure_count = 0
    total_elapsed = 0.0
    for study in tqdm(studies):
        try:
            study_uuid = study["elementUuid"]
            start = time.time()
            result = unload_study(study_uuid)
            result.raise_for_status()
            success_count += 1
        except Exception as e:
            failure_count += 1
            tqdm.write(f"  FAILED - {study_uuid} (error: {str(e)})")
            if isinstance(e, requests.exceptions.RequestException) and e.response is not None:
                tqdm.write("Response body: " + repr(e.response.text)) # repr for cheap escaping
            tqdm.write("") # empty newline between errors for legibility
        finally:
            elapsed = time.time() - start
            total_elapsed += elapsed
            tqdm.write(f"  {study_uuid} - {elapsed:.2f}s")
            if delay is not None:
                time.sleep(delay)

    delay_note = " (excludes --delay pauses)" if delay is not None else ""
    print(f"\nDone. {success_count} succeeded, {failure_count} failed. Total unload time: {total_elapsed:.2f}s (avg {total_elapsed / len(studies):.2f}s/study){delay_note}")

unload_unmodified_studies(duration_arg, dry_run=dry_run_arg, limit=limit_arg, delay=delay_arg)
