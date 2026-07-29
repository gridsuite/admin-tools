import requests
import constant

def get_network_infos_from_study(study):
    return study["rootNetworkInfos"]

# turn studies_response_json into a network uuids list
def get_root_network_uuids_from_studies(studies):
    root_network_infos = map(get_network_infos_from_study, studies)
    root_network_infos_list = [element for sub_list in root_network_infos for element in sub_list]
    root_network_uuids = []
    for root_network_info in root_network_infos_list:
        root_network_uuids.append(get_element_id(root_network_info))
    return root_network_uuids

def get_element_id(element):
    return element["id"]

def delete_root_networks(root_network_uuids, dry_run):
    if dry_run:
        for orphan in root_network_uuids:
            print("DELETE " + constant.DELETE_ROOT_NETWORKS + "/" + orphan)
    else:
        for orphan in root_network_uuids:
            requests.delete(constant.DELETE_ROOT_NETWORKS + "/" + orphan)

def delete_orphan_root_networks(dry_run):
    print("/// Orphan root networks deletion ///")

    print("Getting all root networks from study-server: " + constant.GET_ROOT_NETWORKS)
    root_networks_response_from_study_server = requests.get(constant.GET_ROOT_NETWORKS)
    root_networks_response_from_study_server_json = root_networks_response_from_study_server.json()
    all_root_networks_uuids = list(root_networks_response_from_study_server_json)
    print("Done")

    print("Getting the root networks referenced by studies: " + constant.GET_SUPERVISION_STUDIES)
    studies_response = requests.get(constant.GET_SUPERVISION_STUDIES)
    studies_response_json = studies_response.json()
    root_network_uuids_used_in_studies = get_root_network_uuids_from_studies(studies_response_json)
    print("Done")

    # GET ORPHANS ROOT NETWORKS - ROOT NETWORKS IN STUDY SERVER WHICH ARE NOT REFERENCED BY ANY STUDY
    print("Computing orphan root networks")
    orphan_root_networks = []
    for root_network_uuid in all_root_networks_uuids:
        if root_network_uuid not in root_network_uuids_used_in_studies:
            orphan_root_networks.append(root_network_uuid)
    print("Done")

    # DELETING ORPHANS
    print("Deleting the following " + str(len(orphan_root_networks)) + " orphan root networks : ")
    for orphan_n in orphan_root_networks:
        print(" - ", orphan_n)
    delete_root_networks(orphan_root_networks, dry_run)
    print("Done")

    print("\n\n")
