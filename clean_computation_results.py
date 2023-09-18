import argparse
import constant
import requests

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
            print("An error occured : " + str(result.status_code))

parser = argparse.ArgumentParser(description='Send requests to the gridsuite services to delete computation results', )

parser.add_argument("-n", "--dry-run", help="test mode (default) will not execute any modification request",
                    action="store_true")
parser.add_argument("-lf", "--loadflow", help="delete all loadflow results",
                    action="store_true")
parser.add_argument("-ds", "--dynamicsimulation", help="delete all dynamic simulation results",
                    action="store_true")
parser.add_argument("-sa", "--security", help="delete all security analysis results",
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
    print("Computation results deletion script will run without deleting anything (test mode)")
else:
    print("Computation results deletion script (exec mode)")
print("\n")

if loadflow or runAll:
    delete_computation_results(dry_run, constant.LOADFLOW)    
if dynamicsimulation or runAll:
    delete_computation_results(dry_run, constant.DYNAMIC_SIMULATION)
if security or runAll:
    delete_computation_results(dry_run, constant.SECURITY_ANALYSIS)
if sensitivity or runAll:
    delete_computation_results(dry_run, constant.SENSITIVITY_ANALYSIS)
if shortcircuit or runAll:
    delete_computation_results(dry_run, constant.SHORTCIRCUIT)
if voltageinit or runAll:
    delete_computation_results(dry_run, constant.VOLTAGE_INIT)