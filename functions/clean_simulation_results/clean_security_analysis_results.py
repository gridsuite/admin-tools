import requests
import constant

def delete_security_analysis_results(dry_run):
    print("/// Security analysis results deletion ///")
    if dry_run: 
        resultsCount = requests.get(constant.GET_SECURITY_ANALYSIS_RESULTS_COUNT).json()
        print("Here's the count of stored results : " + str(resultsCount))
    else :
        requests.delete(constant.DELETE_SECURITY_ANALYSIS_RESULTS)
        print("Done")
