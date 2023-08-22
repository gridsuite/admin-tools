import requests
import constant

def delete_voltage_init_results(dry_run):
    print("/// Voltage init results deletion ///")
    if dry_run: 
        resultsCount = requests.get(constant.GET_VOLTAGE_INIT_RESULTS_COUNT).json()
        print("Here's the count of stored results : " + str(resultsCount))
    else :
        requests.delete(constant.DELETE_VOLTAGE_INIT_RESULTS)
        print("Done")