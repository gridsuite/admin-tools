#
# Copyright (c) 2023, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

#
# @author Kevin Le Saulnier <kevin.lesaulnier at rte-france.com>
#

# ENV FOLDERS
DEV_FOLDER = "sql/dev/"
PROD_FOLDER = "sql/prod/"

# SQL FILES
GET_EXISTING_NETWORKS_SQL = "get_existing_networks.sql"
GET_ORPHAN_NETWORKS_SQL = "get_orphan_networks.sql"
DELETE_ORPHAN_NETWORKS_SQL = "delete_orphan_networks.sql"

# SERVICES URL
HTTP_PROTOCOL = "http://"
API_VERSION = "/v1"

STUDY_SERVER_URL = HTTP_PROTOCOL + "study-server" + API_VERSION
NETWORK_STORE_SERVER_URL = HTTP_PROTOCOL + "network-store-server" + API_VERSION
DIRECTORY_SERVER_URL = HTTP_PROTOCOL + "directory-server" + API_VERSION
ACTIONS_SERVER_URL = HTTP_PROTOCOL + "actions-server" + API_VERSION
FILTER_SERVER_URL = HTTP_PROTOCOL + "filter-server" + API_VERSION

LOADFLOW_SERVER_URL = HTTP_PROTOCOL + "loadflow-server" + API_VERSION
DYNAMIC_SIMULATION_SERVER_URL = HTTP_PROTOCOL + "dynamic-simulation-server" + API_VERSION
SECURITY_ANALYSIS_SERVER_URL = HTTP_PROTOCOL + "security-analysis-server" + API_VERSION
SENSITIVITY_ANALYSIS_SERVER_URL = HTTP_PROTOCOL + "sensitivity-analysis-server" + API_VERSION
SHORTCIRCUIT_SERVER_URL = HTTP_PROTOCOL + "shortcircuit-server" + API_VERSION
VOLTAGE_INIT_SERVER_URL = HTTP_PROTOCOL + "voltage-init-server" + API_VERSION

# PATHS
GET_STUDIES = STUDY_SERVER_URL + "/supervision/studies"

GET_NETWORKS = NETWORK_STORE_SERVER_URL + "/networks"
DELETE_NETWORKS = NETWORK_STORE_SERVER_URL + "/networks"

GET_DIRECTORY_ELEMENTS = DIRECTORY_SERVER_URL + "/supervision/elements"

GET_CONTINGENCY_LISTS = ACTIONS_SERVER_URL + "/contingency-lists"
DELETE_CONTINGENCY_LISTS = ACTIONS_SERVER_URL + "/contingency-lists"

GET_FILTERS = FILTER_SERVER_URL + "/filters"
DELETE_FILTERS = FILTER_SERVER_URL + "/filters"

DELETE_COMPUTATION_RESULTS = STUDY_SERVER_URL + "/supervision/computation/results"

# COMPUTATION TYPES FOR RESULTS DELETION
LOADFLOW = "LOAD_FLOW"
DYNAMIC_SIMULATION = "DYNAMIC_SIMULATION"
SECURITY_ANALYSIS = "SECURITY_ANALYSIS"
SENSITIVITY_ANALYSIS = "SENSITIVITY_ANALYSIS"
SHORTCIRCUIT = "SHORT_CIRCUIT"
VOLTAGE_INIT = "VOLTAGE_INITIALIZATION"

#INDEXES
DELETE_STUDIES_INDEXED_EQUIPMENTS = STUDY_SERVER_URL + "/supervision/indexed-equipments"

