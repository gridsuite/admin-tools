#
# Copyright (c) 2023, RTE (http://www.rte-france.com)
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

#
# @author Kevin Le Saulnier <kevin.lesaulnier at rte-france.com>
# @author Sylvain Bouzols <sylvain.bouzols at rte-france.com>
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

GRAFANA_API_VERSION = "/v1"
GRAFANA_API = "/api"
GRAFANA_PROVISIONING = "/provisioning"

# TODO add command parameter to set this DEV
DEV = False

# hostnames
GRIDEXPLORE_HOSTNAME = "localhost:80" if DEV else "gridexplore-app"
STUDY_SERVER_HOSTNAME = "localhost:5001" if DEV else "study-server"

NETWORK_STORE_SERVER_HOSTNAME = "localhost:8080" if DEV else "network-store-server"
DIRECTORY_SERVER_HOSTNAME = "localhost:5026" if DEV else "directory-server"
ACTIONS_SERVER_HOSTNAME = "localhost:5022" if DEV else "actions-server"
FILTER_SERVER_HOSTNAME = "localhost:5027" if DEV else "filter-server"
EXPLORE_SERVER_HOSTNAME = "localhost:5029" if DEV else "explore-server"

LOADFLOW_SERVER_HOSTNAME = "localhost:5008" if DEV else "loadflow-server"
DYNAMIC_SIMULATION_SERVER_HOSTNAME = "localhost:5032" if DEV else "dynamic-simulation-server"
SECURITY_ANALYSIS_SERVER_HOSTNAME = "localhost:5023" if DEV else "security-analysis-server"
SENSITIVITY_ANALYSIS_SERVER_HOSTNAME = "localhost:5030" if DEV else "sensitivity-analysis-server"
SHORTCIRCUIT_SERVER_HOSTNAME = "localhost:5031" if DEV else "shortcircuit-server"
VOLTAGE_INIT_SERVER_HOSTNAME = "localhost:5038" if DEV else "voltage-init-server"

GRAFANA_HOSTNAME = "localhost:7000" if DEV else "grafana"

# URLs
GRIDEXPLORE_URL = HTTP_PROTOCOL + GRIDEXPLORE_HOSTNAME

STUDY_SERVER_URL = HTTP_PROTOCOL + STUDY_SERVER_HOSTNAME + API_VERSION
NETWORK_STORE_SERVER_URL = HTTP_PROTOCOL + NETWORK_STORE_SERVER_HOSTNAME + API_VERSION
DIRECTORY_SERVER_URL = HTTP_PROTOCOL + DIRECTORY_SERVER_HOSTNAME + API_VERSION
ACTIONS_SERVER_URL = HTTP_PROTOCOL + ACTIONS_SERVER_HOSTNAME + API_VERSION
FILTER_SERVER_URL = HTTP_PROTOCOL + FILTER_SERVER_HOSTNAME + API_VERSION
EXPLORE_SERVER_URL = HTTP_PROTOCOL + EXPLORE_SERVER_HOSTNAME + API_VERSION

LOADFLOW_SERVER_URL = HTTP_PROTOCOL + LOADFLOW_SERVER_HOSTNAME + API_VERSION
DYNAMIC_SIMULATION_SERVER_URL = HTTP_PROTOCOL + DYNAMIC_SIMULATION_SERVER_HOSTNAME + API_VERSION
SECURITY_ANALYSIS_SERVER_URL = HTTP_PROTOCOL + SECURITY_ANALYSIS_SERVER_HOSTNAME + API_VERSION
SENSITIVITY_ANALYSIS_SERVER_URL = HTTP_PROTOCOL + SENSITIVITY_ANALYSIS_SERVER_HOSTNAME + API_VERSION
SHORTCIRCUIT_SERVER_URL = HTTP_PROTOCOL + SHORTCIRCUIT_SERVER_HOSTNAME + API_VERSION
VOLTAGE_INIT_SERVER_URL = HTTP_PROTOCOL + VOLTAGE_INIT_SERVER_HOSTNAME + API_VERSION

GRAFANA_URL = HTTP_PROTOCOL + GRAFANA_HOSTNAME + GRAFANA_API

# PATHS
GET_STUDIES = STUDY_SERVER_URL + "/studies"
GET_ACTUATOR_INFO = HTTP_PROTOCOL + "{serverHostName}/actuator/info"

GET_NETWORKS = NETWORK_STORE_SERVER_URL + "/networks"
DELETE_NETWORKS = NETWORK_STORE_SERVER_URL + "/networks"

GET_DIRECTORY_ELEMENTS = DIRECTORY_SERVER_URL + "/supervision/elements"
GET_DIRECTORY_STASHED_ELEMENTS = DIRECTORY_SERVER_URL + "/supervision/elements/stash"

GET_CONTINGENCY_LISTS = ACTIONS_SERVER_URL + "/contingency-lists"
DELETE_CONTINGENCY_LISTS = ACTIONS_SERVER_URL + "/contingency-lists"

GET_FILTERS = FILTER_SERVER_URL + "/filters"
DELETE_FILTERS = FILTER_SERVER_URL + "/filters"

DELETE_EXPLORE_ELEMENTS = EXPLORE_SERVER_URL + "/supervision/explore/elements"

DELETE_COMPUTATION_RESULTS = STUDY_SERVER_URL + "/supervision/computation/results"

GET_DIRECTORIES = DIRECTORY_SERVER_URL + "/supervision/directories"

# COMPUTATION TYPES FOR RESULTS DELETION
LOADFLOW = "LOAD_FLOW"
DYNAMIC_SIMULATION = "DYNAMIC_SIMULATION"
SECURITY_ANALYSIS = "SECURITY_ANALYSIS"
SENSITIVITY_ANALYSIS = "SENSITIVITY_ANALYSIS"
NON_EVACUATED_ENERGY_ANALYSIS = "NON_EVACUATED_ENERGY_ANALYSIS"
SHORTCIRCUIT = "SHORT_CIRCUIT"
VOLTAGE_INIT = "VOLTAGE_INITIALIZATION"

# INDEXED EQUIPMENTS
GET_PLATEFORM_INFO = GRIDEXPLORE_URL + "/idpSettings.json"
DELETE_STUDY_INDEXED_EQUIPMENTS = STUDY_SERVER_URL + "/supervision/studies/{studyUuid}/indexed-equipments"
DELETE_STUDY_NODES_BUILDS = STUDY_SERVER_URL + "/supervision/studies/{studyUuid}/nodes/builds"
GET_STUDIES_INDEXED_EQUIPMENTS_COUNT = STUDY_SERVER_URL + "/supervision/indexed-equipments-count"
GET_STUDIES_INDEXED_TOMBSTONED_EQUIPMENTS_COUNT = STUDY_SERVER_URL + "/supervision/indexed-tombstoned-equipments-count"
GET_STUDIES_INDEXED_EQUIPMENTS_INDEX_NAME = STUDY_SERVER_URL + "/supervision/indexed-equipments-index-name"
GET_STUDIES_INDEXED_TOMBSTONED_EQUIPMENTS_INDEX_NAME = STUDY_SERVER_URL + "/supervision/indexed-tombstoned-equipments-index-name"
GET_ELASTICSEARCH_HOST = STUDY_SERVER_URL + "/supervision/elasticsearch-host"
ES_FORCE_MERGE = "{elasticsearchHost}/{indexName}/_forcemerge"

# GRAFANA ENDPOINTS
GRAFANA_FOLDER = GRAFANA_URL + "/folders"
GRAFANA_ALERT_RULES = GRAFANA_URL + API_VERSION + GRAFANA_PROVISIONING + "/alert-rules"
GRAFANA_RULE_GROUPS = GRAFANA_URL + API_VERSION + GRAFANA_PROVISIONING + "/folder/{folderUid}/rule-groups/{ruleGroupId}"

# INDEXED ELEMENTS
GET_DIRECTORY_ELEMENTS_COUNT = DIRECTORY_SERVER_URL + "/supervision/indexed-directory-elements-count"
GET_DIRECTORY_ELEMENTS_INDEX_NAME = DIRECTORY_SERVER_URL + "/supervision/indexed-directory-elements-index-name"
DELETE_INDEXED_ELEMENTS = DIRECTORY_SERVER_URL + "/supervision/directories/{directoryUuid}/indexed-directory-elements"
REINDEX_ELEMENTS = DIRECTORY_SERVER_URL + "/supervision/directoris/{directoryUuid}/reindex"
