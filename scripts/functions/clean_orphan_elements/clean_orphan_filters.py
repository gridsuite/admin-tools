import constant
import requests
from functions.clean_orphan_elements.clean_orphan_root_networks import get_element_id

def get_directory_element_uuid(element):
    return element["elementUuid"]

def delete_filters(filter_uuids, dry_run):
    if dry_run:
        for orphan_f in filter_uuids:
            print("DELETE " + constant.DELETE_FILTERS + "/" + orphan_f)
    else:
        for orphan_f in filter_uuids:
            requests.delete(constant.DELETE_FILTERS + "/" + orphan_f)

# DELETING ORPHAN FILTERS FROM FILTER SERVER
def delete_orphan_filters(dry_run):
    print("/// Orphan filters deletion ///")
    print("Getting existing filters from directory-server: " + constant.GET_DIRECTORY_ELEMENTS)
    directory_filters_response = requests.get(constant.GET_DIRECTORY_ELEMENTS, params={"elementType": "FILTER"})
    directory_filters_response_json = directory_filters_response.json()
    directory_filters_uuids_map = map(get_directory_element_uuid, directory_filters_response_json)
    directory_filters_uuids = list(directory_filters_uuids_map)
    print("Done")

    # GET ALL EXISTING FILTERS FROM FILTER-SERVER
    print("Getting all filters from filter-server: " + constant.GET_FILTERS)
    actions_filters_response = requests.get(constant.GET_FILTERS)
    actions_filters_json = actions_filters_response.json()
    actions_filters_uuids = map(get_element_id, actions_filters_json)
    all_filters_uuids = list(actions_filters_uuids)
    print("Done")

    # GET ORPHAN FILTERS - FILTERS FROM FILTER-SERVER WHICH ARE NOT KNOWN IN DIRECTORY SERVER
    print("Computing orphan filters")
    orphan_filters = []
    for element_uuid in all_filters_uuids:
        if element_uuid not in directory_filters_uuids:
            orphan_filters.append(element_uuid)
    print("Done")

    # DELETING ORPHANS
    print("Deleting the following " + str(len(orphan_filters)) + " orphan filters : ")
    for orphan_cl in orphan_filters:
        print(" - ", orphan_cl)
    delete_filters(orphan_filters, dry_run)
    print("Done")

    print("\n\n")
