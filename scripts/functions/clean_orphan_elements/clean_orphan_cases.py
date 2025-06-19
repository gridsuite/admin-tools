import requests
import constant

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
            if answer.status_code != 200:
                print("Error: " + str(answer.content))

def delete_orphan_cases(dry_run):
    print("/// Orphan cases deletion ///")
    print("Getting existing cases from directory-server: " + constant.GET_DIRECTORY_ELEMENTS)
    directory_cases_response = requests.get(constant.GET_DIRECTORY_ELEMENTS, params={"elementType": "CASE"})
    directory_cases_response_json = directory_cases_response.json()
    directory_cases_uuids_map = map(get_directory_element_uuid, directory_cases_response_json)
    directory_cases_uuids = list(directory_cases_uuids_map)

    print("Adding cases referenced by studies: " + constant.GET_SUPERVISION_STUDIES)
    studies_cases_response = requests.get(constant.GET_SUPERVISION_STUDIES)
    studies_cases_response_json = studies_cases_response.json()
    # turn studies_cases_response_json into a case uuids list :
    studies_cases_uuids = map(get_case_uuids_from_study, studies_cases_response_json)
    case_uuids_used_in_studies = [element for sub_list in list(studies_cases_uuids) for element in sub_list]
    # concatenates both referenced case uuids list and remove duplicates
    referenced_case_uuids = list(set(directory_cases_uuids + case_uuids_used_in_studies))
    print("Done")

    # GET CASES SAVED IN CASE SERVER
    print("Getting cases from case server: " + constant.GET_ALL_CASES)
    cases_response = requests.get(constant.GET_ALL_CASES)
    cases_response_json = cases_response.json()
    cases_uuids = map(get_uuid, cases_response_json)
    all_cases_uuids = list(cases_uuids)
    print("Done")

    # GET ORPHANS CASES - CASES IN CASE SERVER WHICH ARE NOT KNOWN IN STUDY SERVER NOR IN DIRECTORY SERVER
    print("Computing orphan cases")
    orphan_cases = []
    for case_uuid in all_cases_uuids:
        if case_uuid not in referenced_case_uuids:
            orphan_cases.append(case_uuid)
    print("Done")

    # DELETING ORPHANS
    print("Deleting the following " + str(len(orphan_cases)) + " orphan cases : ")
    for orphan in orphan_cases:
        print(" - ", orphan)
    delete_cases(orphan_cases, dry_run)
    print("Done")

    print("\n\n")
