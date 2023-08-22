import requests
import constant

def delete_loadflow_results(dry_run):
    print("/// LoadFlow results deletion ///")
    if dry_run: 
        resultsCount = requests.get(constant.GET_LOADFLOW_RESULTS_COUNT).json()
        print("Here's the count of stored results : " + str(resultsCount))
    else :
        requests.delete(constant.DELETE_LOADFLOW_RESULTS)
        print("Done")