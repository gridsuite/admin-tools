import argparse
import requests
import constant

def get_directory_element_uuid(element):
    return element["elementUuid"]

parser = argparse.ArgumentParser(description='Remove the obsolete elements refering to criteria contingency lists', )

parser.add_argument("--dry-run", help="test mode : will not execute any deletion request",
                    action="store_true")

args = parser.parse_args()
dry_run = args.dry_run

if dry_run:
    print("the script will run without deleting anything (dry run mode)")
else:
    print("Deletion of obsolete elements refering to criteria contingency lists")

print("\n\n")

# GET ALL CONTINGENCY LISTS FROM DIRECTORY SERVER
print("Getting contingency lists from directory-server: " + constant.GET_DIRECTORY_ELEMENTS)
directory_contingency_lists_response = requests.get(constant.GET_DIRECTORY_ELEMENTS,
                                                        params={"elementType": "CONTINGENCY_LIST"})
directory_contingency_lists_response_json = directory_contingency_lists_response.json()
directory_contingency_lists_uuids = list(map(get_directory_element_uuid, directory_contingency_lists_response_json))
print("Done")

# GET ALL CONTINGENCY LISTS FROM ACTIONS SERVER
print("Getting all contingency lists from actions-server: " + constant.GET_CONTINGENCY_LISTS)
contingency_lists_metadata = requests.get(constant.GET_CONTINGENCY_LISTS_METADATA,
                                                            params={"ids": directory_contingency_lists_uuids}
                                          ).json()
print("Done")

# EXTRACT THE CONTINGENCY LIST THAT ARE 'CRITERIA BASED' ACCORDING TO METADATA
print("Extract contingency lists to be deleted")
contingency_lists_to_be_deleted = []
for metadata in contingency_lists_metadata:
    if metadata["type"] == 'FORM':
        contingency_lists_to_be_deleted.append(metadata["id"])

# DELETING CRITERIA CONTINGENCY LISTS ELEMENTS
print("Deleting the following " + str(len(contingency_lists_to_be_deleted)) + " criteria contingency lists : ")
for uuid_to_be_deleted in contingency_lists_to_be_deleted:
    print(" - ", uuid_to_be_deleted)

if dry_run:
    for uuid_to_be_deleted in contingency_lists_to_be_deleted:
        print("DELETE " + constant.GET_DIRECTORY_ELEMENTS + "/" + uuid_to_be_deleted)
else:
    requests.delete(constant.GET_DIRECTORY_ELEMENTS, params={"ids": contingency_lists_to_be_deleted})
print("Done")
