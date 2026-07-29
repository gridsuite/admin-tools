import argparse

from functions.clean_orphan_elements.clean_orphan_contingency_lists import delete_orphan_contingency_lists
from functions.clean_orphan_elements.clean_orphan_filters import delete_orphan_filters
from functions.clean_orphan_elements.clean_orphan_cases import delete_orphan_cases
from functions.clean_orphan_elements.clean_orphan_studies import delete_orphan_studies
from functions.clean_orphan_elements.clean_orphan_networks import delete_orphan_networks
from functions.clean_orphan_elements.clean_orphan_root_networks import delete_orphan_root_networks

parser = argparse.ArgumentParser(description='Send requests to the gridsuite services to remove orphan elements', )

parser.add_argument("--dry-run", help="test mode : will not execute any deletion request",
                    action="store_true")

args = parser.parse_args()
dry_run = args.dry_run

if dry_run:
    print("Orphans deletion script will run without deleting anything (dry run mode)")
else:
    print("Orphans deletion script")

print("\n\n")

delete_orphan_cases(dry_run)

delete_orphan_studies(dry_run)

delete_orphan_root_networks(dry_run)

delete_orphan_networks(dry_run)

delete_orphan_contingency_lists(dry_run)

delete_orphan_filters(dry_run)
