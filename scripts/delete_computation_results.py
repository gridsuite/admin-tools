#
# Copyright (c) 2023, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import argparse
import constant
from functions.delete_computation_results.delete_computation_results import delete_computation_results 

#
# @author Hugo Marcellin <hugo.marcelin at rte-france.com>
#

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
parser.add_argument("-nee", "--nonevacuatedenergy", help="delete all non evacuated energy analysis results",
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
nonevacuatedenergy = args.nonevacuatedenergy
shortcircuit = args.shortcircuit
voltageinit = args.voltageinit

runAll = not(loadflow or dynamicsimulation or security or sensitivity or nonevacuatedenergy or shortcircuit or voltageinit)

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
if nonevacuatedenergy or runAll:
    delete_computation_results(dry_run, constant.NON_EVACUATED_ENERGY_ANALYSIS)
if shortcircuit or runAll:
    delete_computation_results(dry_run, constant.SHORTCIRCUIT)
if voltageinit or runAll:
    delete_computation_results(dry_run, constant.VOLTAGE_INIT)
