import requests
import constant
from script_mode import ScriptMode


def get_directory_element_uuid(element):
    return element["elementUuid"]


def get_actions_element_uuid(element):
    return element["id"]


def delete_contingency_lists(contingency_list_uuids, script_mode):
    if script_mode == ScriptMode.TEST:
        for orphan_cl in contingency_list_uuids:
            print("DELETE " + constant.DELETE_CONTINGENCY_LISTS + "/" + orphan_cl)
    else:
        for orphan_cl in contingency_list_uuids:
            requests.delete(constant.DELETE_CONTINGENCY_LISTS + "/" + orphan_cl)


def delete_orphan_contingency_lists(script_mode):
    # DELETING ORPHAN ACTIONS IN ACTIONS SERVER
    print("/// Orphan actions deletion ///")
    # GET EXISTING ACTIONS FROM DIRECTORY SERVER
    print("Getting existing contingency lists from directory-server")
    get_directory_contingency_lists_response = requests.get(constant.GET_DIRECTORY_ELEMENTS,
                                                            params={"elementType": "CONTINGENCY_LIST"})
    get_directory_contingency_lists_response_json = get_directory_contingency_lists_response.json()
    get_directory_contingency_lists_response_json_uuid = map(get_directory_element_uuid,
                                                             get_directory_contingency_lists_response_json)
    existing_contingency_lists_uuid = list(get_directory_contingency_lists_response_json_uuid)

    print("Done")

    # GET CONTINGENCY LISTS FROM ACTIONS SERVER
    print("Getting all contingency lists from actions-server")
    get_actions_contingency_lists_response = requests.get(constant.GET_CONTINGENCY_LISTS)
    get_actions_contingency_lists_json = get_actions_contingency_lists_response.json()
    get_actions_contingency_lists_uuid = map(get_actions_element_uuid, get_actions_contingency_lists_json)
    all_contingency_lists_uuid = list(get_actions_contingency_lists_uuid)

    print("Done")

    # GET ORPHANS CONTINGENCY LISTS - CONTINGENCY LISTS IN ACTIONS SERVER WHICH ARE NOT KNOWN IN DIRECTORY SERVER
    print("Computing orphan contingency lists")
    orphan_contingency_lists = []
    for element_uuid in all_contingency_lists_uuid:
        if element_uuid not in existing_contingency_lists_uuid:
            orphan_contingency_lists.append(element_uuid)

    print("Done")

    # DELETING OPRHANS
    print("Deleting the following orphan contingency lists : ")
    for orphan_cl in orphan_contingency_lists:
        print(" - ", orphan_cl)

    delete_contingency_lists(orphan_contingency_lists, script_mode)

    print("Done")

    print("\n\n")
