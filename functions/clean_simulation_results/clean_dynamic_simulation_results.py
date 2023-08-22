import requests
import constant

def delete_dynamic_simulation_results(dry_run):
    print("/// Dynamic simulation results deletion ///")
    if dry_run: 
        resultsCount = requests.get(constant.GET_DYNAMIC_SIMULATION_RESULTS_COUNT).json()
        print("Here's the count of stored results : " + str(resultsCount))
    else :    
        requests.delete(constant.DELETE_DYNAMIC_SIMULATION_RESULTS)
        print("Done")