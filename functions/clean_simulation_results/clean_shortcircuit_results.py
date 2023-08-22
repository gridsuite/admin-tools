import requests
import constant

def delete_shortcircuit_results(dry_run):
    print("/// Shortcircuit results deletion ///")
    if dry_run: 
        resultsCount = requests.get(constant.GET_SHORTCIRCUIT_RESULTS_COUNT).json()
        print("Here's the count of stored results : " + str(resultsCount))
    else :
        requests.delete(constant.DELETE_SHORTCIRCUIT_RESULTS)
        print("Done")