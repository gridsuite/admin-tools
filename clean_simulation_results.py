import argparse
import constant
import requests

def delete_simulation_results(dry_run, name, endpoint, dry_run_endpoint):
    print("/// " + name + " results deletion ///")
    if dry_run: 
        resultsCount = requests.get(dry_run_endpoint).json()
        print("Here's the count of stored results : " + str(resultsCount))
    else :
        result = requests.delete(endpoint)
        if result.ok :
            print("Done")
        else :
            print("An error occured : " + str(result.status_code))

parser = argparse.ArgumentParser(description='Send requests to the gridsuite services to delete simulation results', )

parser.add_argument("--dry-run", help="test mode (default) will not execute any modification request",
                    action="store_true")
parser.add_argument("-lf", "--loadflow", help="delete all loadflow results",
                    action="store_true")
parser.add_argument("-ds", "--dynamicsimulation", help="delete all dynamic simulation results",
                    action="store_true")
parser.add_argument("-su", "--security", help="delete all security analysis results",
                    action="store_true")
parser.add_argument("-ss", "--sensitivity", help="delete all sensitivity analysis results",
                    action="store_true")
parser.add_argument("-sc", "--shortcircuit", help="delete all shortcircuit results",
                    action="store_true")
parser.add_argument("-vi", "--voltageinit", help="delete all voltage init results",
                    action="store_true")                                                            

args = parser.parse_args()
dry_run = args.dry_run

loadflow = args.loadflow
dynamicsimulation = args.dynamicsimulation
security = args.security
sensitivity = args.sensitivity
shortcircuit = args.shortcircuit
voltageinit = args.voltageinit

runAll = not(loadflow or dynamicsimulation or security or sensitivity or shortcircuit or voltageinit) 

if dry_run:
    print("Simulation results deletion script will run without deleting anything (test mode)")
else:
    print("Simulation results deletion script (exec mode)")
print("\n")

if loadflow or runAll:
    delete_simulation_results(dry_run, "LoadFlow", constant.DELETE_STUDY_LOADFLOW_RESULTS, constant.GET_LOADFLOW_RESULTS_COUNT)    
if dynamicsimulation or runAll:
    delete_simulation_results(dry_run, "Dynamic simulation", constant.DELETE_STUDY_DYNAMIC_SIMULATION_RESULTS, constant.GET_DYNAMIC_SIMULATION_RESULTS_COUNT)
if security or runAll:
    delete_simulation_results(dry_run, "Security analysis", constant.DELETE_STUDY_SECURITY_ANALYSIS_RESULTS, constant.GET_SECURITY_ANALYSIS_RESULTS_COUNT)
if sensitivity or runAll:
    delete_simulation_results(dry_run, "Sensitivity analysis", constant.DELETE_STUDY_SENSITIVITY_ANALYSIS_RESULTS, constant.GET_SENSITIVITY_ANALYSIS_RESULTS_COUNT)
if shortcircuit or runAll:
    delete_simulation_results(dry_run, "Shortcircuit", constant.DELETE_STUDY_SHORTCIRCUIT_RESULTS, constant.GET_SHORTCIRCUIT_RESULTS_COUNT) 
if voltageinit or runAll:
    delete_simulation_results(dry_run, "Voltage init", constant.DELETE_STUDY_VOLTAGE_INIT_RESULTS, constant.GET_VOLTAGE_INIT_RESULTS_COUNT)