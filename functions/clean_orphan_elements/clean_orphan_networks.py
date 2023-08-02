import requests

import constant
from script_mode import ScriptMode


def get_network_uuid_from_study(study):
    return study["networkUuid"]


def get_network_uuid_from_network(network):
    return network["uuid"]


def delete_networks(network_uuids, script_mode):
    if script_mode == ScriptMode.TEST:
        for orphan_n in network_uuids:
            print("DELETE " + constant.DELETE_NETWORKS + "/" + orphan_n)
    else:
        for orphan_n in network_uuids:
            requests.delete(constant.DELETE_NETWORKS + "/" + orphan_n)


def delete_orphan_network(script_mode):
    # DELETING ORPHAN NETWORKS IN NETWORK STORE SERVER
    print("/// Orphan networks deletion ///")
    # GET EXISTING NETWORKS AMONG EXISTING STUDIES
    print("Getting existing networks from existing studies")
    get_studies_response = requests.get(constant.GET_STUDIES)

    get_studies_response_json = get_studies_response.json()
    get_studies_response_json_network_uuid = map(get_network_uuid_from_study, get_studies_response_json)
    existing_networks_uuid = list(get_studies_response_json_network_uuid)

    print("Done")
    # GET NETWORKS SAVED IN NETWORK STORE SERVER
    print("Getting networks from network store server")
    get_networks_response = requests.get(constant.GET_NETWORKS)

    get_networks_response_json = get_networks_response.json()
    get_networks_response_json_uuid = map(get_network_uuid_from_network, get_networks_response_json)
    all_networks_uuid = list(get_networks_response_json_uuid)

    print("Done")
    # GET ORPHANS NETWORKS - NETWORKS IN NETWORK STORE SERVER WHICH ARE NOT KNOWN IN STUDY SERVER
    print("Computing orphan networks")
    orphan_networks = []
    for network_uuid in all_networks_uuid:
        if network_uuid not in existing_networks_uuid:
            orphan_networks.append(network_uuid)

    print("Done")
    # DELETING OPRHANS
    print("Deleting the following orphan networks : ")
    for orphan_n in orphan_networks:
        print(" - ", orphan_n)

    delete_networks(orphan_networks, script_mode)

    print("Done")

    print("\n\n")
