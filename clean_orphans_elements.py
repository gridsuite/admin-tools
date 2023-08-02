import argparse

from functions.clean_orphan_elements.clean_orphan_contingency_lists import delete_orphan_contingency_lists
from functions.clean_orphan_elements.clean_orphan_filters import delete_orphan_filters
from functions.clean_orphan_elements.clean_orphan_networks import delete_orphan_network
from script_mode import ScriptMode

parser = argparse.ArgumentParser(description='Send requests to the gridsuite services to remove orphan elements', )

parser.add_argument("--mode", help="test mode (default) will not execute any modification request",
                    choices=[ScriptMode.TEST.value, ScriptMode.EXEC.value], nargs='?', type=str, const=ScriptMode.TEST,
                    default=ScriptMode.TEST)

args = parser.parse_args()
script_mode = args.mode

if script_mode == ScriptMode.TEST:
    print("Orphans deletion script will run without deleting anything (test mode)")
else:
    print("Orphans deletion script (exec mode)")

print("\n\n")

delete_orphan_network(script_mode)

delete_orphan_contingency_lists(script_mode)

delete_orphan_filters(script_mode)
