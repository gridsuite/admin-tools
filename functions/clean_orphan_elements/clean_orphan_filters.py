import constant
import requests


def get_directory_element_uuid(element):
    return element["elementUuid"]


def delete_filters(filter_uuids, dry_run):
    if dry_run:
        for orphan_f in filter_uuids:
            print("DELETE " + constant.DELETE_FILTERS + "/" + orphan_f)
    else:
        for orphan_f in filter_uuids:
            requests.delete(constant.DELETE_FILTERS + "/" + orphan_f)


def get_element_id(element):
    return element["id"]


def delete_orphan_filters(dry_run):
    # DELETING ORPHAN FILTERS IN FILTER SERVER
    print("/// Orphan filters deletion ///")
    # GET EXISTING FILTERS FROM DIRECTORY SERVER
    print("Getting existing filters from directory-server")
    get_directory_filters_response = requests.get(constant.GET_DIRECTORY_ELEMENTS, params={"elementType": "FILTER"})
    get_directory_filters_response_json = get_directory_filters_response.json()
    get_directory_filters_response_json_uuid = map(get_directory_element_uuid, get_directory_filters_response_json)
    existing_filters_uuid = list(get_directory_filters_response_json_uuid)

    print("Done")

    # GET CONTINGENCY LISTS FROM ACTIONS SERVER
    print("Getting all filters from filter-server")
    get_actions_filters_response = requests.get(constant.GET_FILTERS)
    get_actions_filters_json = get_actions_filters_response.json()
    get_actions_filters_uuid = map(get_element_id, get_actions_filters_json)
    all_filters_uuid = list(get_actions_filters_uuid)

    print("Done")

    # GET ORPHANS CONTINGENCY LISTS - CONTINGENCY LISTS IN ACTIONS SERVER WHICH ARE NOT KNOWN IN DIRECTORY SERVER
    print("Computing orphan filters")
    orphan_filters = []
    for element_uuid in all_filters_uuid:
        if element_uuid not in existing_filters_uuid:
            orphan_filters.append(element_uuid)

    print("Done")

    # DELETING OPRHANS
    print("Deleting the following orphan filters : ")
    for orphan_cl in orphan_filters:
        print(" - ", orphan_cl)

    delete_filters(orphan_filters, dry_run)

    print("Done")

    print("\n\n")
