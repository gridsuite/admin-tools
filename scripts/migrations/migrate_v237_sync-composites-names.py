import argparse
import requests
import constant

parser = argparse.ArgumentParser(description='Takes the name of the composites elements in directory server and apply it to them in netmod-server', )

print("Getting composites lists from directory-server: " + constant.GET_DIRECTORY_ELEMENTS)
directory_composites_response = requests.get(
    constant.GET_DIRECTORY_ELEMENTS,
    params={"elementType": "MODIFICATION"},
    timeout=30)
if 200 == directory_composites_response.status_code:
    print("Success")
else:
    print("Failed : {directory_composites_response.status_code} - {directory_composites_response.reason}")
    directory_composites_response.raise_for_status()

directory_composites_response_json = directory_composites_response.json()

# updates their name (with their current name) -> it will now sync them with their name in netmod-server
directory_composites_pairs = [(element["elementUuid"], element["elementName"]) for element in directory_composites_response_json]
print("Updates the following " + str(len(directory_composites_pairs)) + " composites names in modification-server : ")
for uuid, name in directory_composites_pairs:
    print(" - ", uuid, '-> ' + name)
    response = requests.put(
        url = constant.PUT_COMPOSITES.format(uuid = uuid),
        json={},
        params={"name": name},
        timeout=30)
    if 200 == response.status_code:
        print("Success")
    else:
        print("Failed : {response.status_code} - {response.reason}")
