import argparse

from functions.clean_simulation_results.clean_loadflow_results import delete_loadflow_results
from functions.clean_simulation_results.clean_dynamic_simulation_results import delete_dynamic_simulation_results
from functions.clean_simulation_results.clean_security_analysis_results import delete_security_analysis_results
from functions.clean_simulation_results.clean_sensitivity_analysis_results import delete_sensitivity_analysis_results
from functions.clean_simulation_results.clean_shortcircuit_results import delete_shortcircuit_results
from functions.clean_simulation_results.clean_voltage_init_results import delete_voltage_init_results

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

if runAll:
    delete_loadflow_results(dry_run)    
    delete_dynamic_simulation_results(dry_run)
    delete_security_analysis_results(dry_run)
    delete_sensitivity_analysis_results(dry_run)    
    delete_shortcircuit_results(dry_run)    
    delete_voltage_init_results(dry_run) 
else: 
    if loadflow:
        delete_loadflow_results(dry_run)
    if dynamicsimulation:
        delete_dynamic_simulation_results(dry_run)
    if security:
        delete_security_analysis_results(dry_run)
    if sensitivity:
        delete_sensitivity_analysis_results(dry_run)
    if shortcircuit:
        delete_shortcircuit_results(dry_run)
    if voltageinit:
        delete_voltage_init_results(dry_run)

   