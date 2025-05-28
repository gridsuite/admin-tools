import argparse

from functions.clean_orphan_elements.clean_orphan_contingency_lists import delete_orphan_contingency_lists
from functions.clean_orphan_elements.clean_orphan_filters import delete_orphan_filters
from functions.clean_orphan_elements.clean_orphan_cases import delete_orphan_cases
from functions.clean_orphan_elements.clean_orphan_networks import delete_orphan_network

parser = argparse.ArgumentParser(description='Send requests to the gridsuite services to remove orphan elements', )

parser.add_argument("--dry-run", help="test mode (default) will not execute any modification request",
                    action="store_true")

args = parser.parse_args()
dry_run = args.dry_run

if dry_run:
    print("Orphans deletion script will run without deleting anything (test mode)")
else:
    print("Orphans deletion script (exec mode)")

print("\n\n")
# TODO : effacer les studies orphelines au début, en tout cas avant delete_orphan_network, pour optimiser le nettoyage

delete_orphan_cases(dry_run)

# delete_orphan_network(dry_run)

# delete_orphan_contingency_lists(dry_run)

# delete_orphan_filters(dry_run)