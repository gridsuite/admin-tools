import requests
import constant

def get_directory_element_uuid(element):
    return element["elementUuid"]

def get_element_id(element):
    return element["id"]

def delete_studies(studies_uuids, dry_run):
    if dry_run:
        for orphan in studies_uuids:
            print("DELETE " + constant.DELETE_STUDY + "/" + orphan)
    else:
        for orphan in studies_uuids:
            answer = requests.delete(constant.DELETE_STUDY + "/" + orphan)
            if answer.status_code != 200:
                print("Error: " + str(answer.content))

def delete_orphan_studies(dry_run):
    print("/// Orphan studies deletion ///")
    print("Getting existing studies from directory-server: " + constant.GET_DIRECTORY_ELEMENTS)
    directory_studies_response = requests.get(constant.GET_DIRECTORY_ELEMENTS, params={"elementType": "STUDY"})
    directory_studies_json = directory_studies_response.json()
    directory_studies_uuids_map = map(get_directory_element_uuid, directory_studies_json)
    directory_studies_uuids = list(directory_studies_uuids_map)

    print("Getting all studies from study-server: " + constant.GET_STUDIES)
    studies_response = requests.get(constant.GET_STUDIES)
    studies_response_json = studies_response.json()
    studies_uuids_map = map(get_element_id, studies_response_json)
    all_studies_uuids = list(studies_uuids_map)
    print("Done")

    # GET ORPHANS STUDIES - STUDIES IN STUDY SERVER WHICH ARE NOT KNOWN IN DIRECTORY SERVER
    print("Computing orphan studies")
    orphan_studies= []
    for study_uuid in all_studies_uuids:
        if study_uuid not in directory_studies_uuids:
            orphan_studies.append(study_uuid)
    print("Done")

    print("Deleting the following " + str(len(orphan_studies)) + " orphan studies : ")
    for orphan in orphan_studies:
        print(" - ", orphan)
    delete_studies(orphan_studies, dry_run)
    print("Done")

    print("\n\n")

