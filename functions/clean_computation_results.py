import requests
import constant

def delete_computation_results(dry_run, computationType):
    print("/// " + computationType + " results deletion ///")
    if dry_run: 
        resultsCount = requests.delete(constant.DELETE_COMPUTATION_RESULTS, params={'type': computationType, "dryRun": "true"})
        print("Here's the count of stored results : " + str(resultsCount.json()))
    else :
        result = requests.delete(constant.DELETE_COMPUTATION_RESULTS, params={'type': computationType, "dryRun": "false"})
        if result.ok :
            print("Here's the count of deleted results : " + str(result.json()))
        else :
            print("An error occured : " + str(result.json()))