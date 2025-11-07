import requests
import constant

def get_directory_element_uuid(element):
    return element["elementUuid"]


def get_actions_element_uuid(element):
    return element["id"]


def delete_contingency_lists(contingency_list_uuids, dry_run):
    if dry_run:
        for orphan_cl in contingency_list_uuids:
            print("DELETE " + constant.DELETE_CONTINGENCY_LISTS + "/" + orphan_cl)
    else:
        for orphan_cl in contingency_list_uuids:
            requests.delete(constant.DELETE_CONTINGENCY_LISTS + "/" + orphan_cl)


def delete_orphan_contingency_lists(dry_run):
    # DELETING ORPHAN ACTIONS IN ACTIONS SERVER
    print("/// Orphan actions deletion ///")
    # GET EXISTING ACTIONS FROM DIRECTORY SERVER
    print("Getting contingency lists from directory-server: " + constant.GET_DIRECTORY_ELEMENTS)
    directory_contingency_lists_response = requests.get(constant.GET_DIRECTORY_ELEMENTS,
                                                            params={"elementType": "CONTINGENCY_LIST"})
    directory_contingency_lists_response_json = directory_contingency_lists_response.json()
    directory_contingency_lists_uuids = list(map(get_directory_element_uuid, directory_contingency_lists_response_json))
    print("Done")

    # GET CONTINGENCY LISTS FROM ACTIONS SERVER
    print("Getting all contingency lists from actions-server: " + constant.GET_CONTINGENCY_LISTS)
    actions_contingency_lists_response = requests.get(constant.GET_CONTINGENCY_LISTS)
    actions_contingency_lists_json = actions_contingency_lists_response.json()
    all_contingency_lists_uuid = list(map(get_actions_element_uuid, actions_contingency_lists_json))
    print("Done")

    # GET ORPHANS CONTINGENCY LISTS - CONTINGENCY LISTS IN ACTIONS SERVER WHICH ARE NOT KNOWN IN DIRECTORY SERVER
    print("Computing orphan contingency lists")
    orphan_contingency_lists = []
    for element_uuid in all_contingency_lists_uuid:
        if element_uuid not in directory_contingency_lists_uuids:
            orphan_contingency_lists.append(element_uuid)

    print("Done")

    # DELETING ORPHANS
    print("Deleting the following " + str(len(orphan_contingency_lists)) + " orphan contingency lists : ")
    for orphan_cl in orphan_contingency_lists:
        print(" - ", orphan_cl)

    delete_contingency_lists(orphan_contingency_lists, dry_run)

    print("Done")

    print("\n\n")
