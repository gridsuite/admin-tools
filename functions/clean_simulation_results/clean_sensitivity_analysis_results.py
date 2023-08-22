import requests
import constant

def delete_sensitivity_analysis_results(dry_run):
    print("/// Sensitivity analysis results deletion ///")
    if dry_run: 
        resultsCount = requests.get(constant.GET_SENSITIVITY_ANALYSIS_RESULTS_COUNT).json()
        print("Here's the count of stored results : " + str(resultsCount))
    else :
        requests.delete(constant.DELETE_SENSITIVITY_ANALYSIS_RESULTS)
        print("Done")