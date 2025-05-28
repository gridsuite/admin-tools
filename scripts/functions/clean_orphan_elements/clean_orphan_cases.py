import requests
from scripts import constant

def get_directory_element_uuid(element):
    return element["elementUuid"]

def get_case_uuids_from_study(study):
    return study["caseUuids"]

def get_uuid(obj):
    return obj["uuid"]

def delete_cases(case_uuids, dry_run):
    if dry_run:
        for orphan in case_uuids:
            print("DELETE " + constant.DELETE_CASES + "/" + orphan)
    else:
        for orphan in case_uuids:
            answer = requests.delete(constant.DELETE_CASES + "/" + orphan)
            if (answer.status_code != 200):
                print("Error: " + str(answer.content))

def delete_orphan_cases(dry_run):
    # DELETING ORPHAN CASES (where ??)
    print("/// Orphan cases deletion ///")
    print("Getting existing cases from directory-server")
    get_directory_cases_response = requests.get(constant.GET_DIRECTORY_ELEMENTS, params={"elementType": "CASE"})
    get_directory_cases_response_json = get_directory_cases_response.json()
    get_directory_cases_response_json_uuid = map(get_directory_element_uuid, get_directory_cases_response_json)
    directory_cases_uuids = list(get_directory_cases_response_json_uuid)

    print("Adds cases referenced by studies: " + constant.GET_SUPERVISION_STUDIES)
    get_studies_response = requests.get(constant.GET_SUPERVISION_STUDIES)
    get_studies_response_json = get_studies_response.json()
    # turn get_studies_response_json into a case uuids list :
    get_studies_response_json_cases_uuids = map(get_case_uuids_from_study, get_studies_response_json)
    case_uuids_used_in_studies = [element for sub_list in list(get_studies_response_json_cases_uuids) for element in sub_list]
    # concatenates both referenced case uuids list and remove duplicates
    referenced_case_uuids = list(set(directory_cases_uuids + case_uuids_used_in_studies))
    print("Done")

    # GET CASES SAVED IN CASE SERVER
    print("Getting cases from case server : " + constant.GET_CASES)
    get_cases_response = requests.get(constant.GET_CASES)
    get_cases_response_json = get_cases_response.json()
    get_cases_response_json_uuid = map(get_uuid, get_cases_response_json)
    all_cases_uuids = list(get_cases_response_json_uuid)
    print("Done")

    # GET ORPHANS CASES - NETWORKS IN CASE SERVER WHICH ARE NOT KNOWN IN STUDY SERVER NOR IN DIRECTORY SERVER
    print("Computing orphan cases")
    orphan_cases = []
    for case_uuid in all_cases_uuids:
        if case_uuid not in referenced_case_uuids:
            orphan_cases.append(case_uuid)
    print("Done")

    # DELETING ORPHANS
    print("Deleting the following orphan cases : ")
    for orphan in orphan_cases:
        print(" - ", orphan)
    delete_cases(orphan_cases, dry_run)

    print("Done")

    print("\n\n")
