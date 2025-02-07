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
GRIDEXPLORE_HOSTNAME = "172.17.0.1:80" if DEV else "gridexplore-app"
STUDY_SERVER_HOSTNAME = "172.17.0.1:5001" if DEV else "study-server"

NETWORK_STORE_SERVER_HOSTNAME = "172.17.0.1:8080" if DEV else "network-store-server"
DIRECTORY_SERVER_HOSTNAME = "172.17.0.1:5026" if DEV else "directory-server"
ACTIONS_SERVER_HOSTNAME = "172.17.0.1:5022" if DEV else "actions-server"
FILTER_SERVER_HOSTNAME = "172.17.0.1:5027" if DEV else "filter-server"
EXPLORE_SERVER_HOSTNAME = "172.17.0.1:5029" if DEV else "explore-server"
CASE_SERVER_HOSTNAME = "172.17.0.1:5000" if DEV else "case-server"
S3_MIGRATION_CASE_SERVER_HOSTNAME = "172.17.0.1:5500" if DEV else "s3-migration-case-server"

LOADFLOW_SERVER_HOSTNAME = "172.17.0.1:5008" if DEV else "loadflow-server"
DYNAMIC_SIMULATION_SERVER_HOSTNAME = "172.17.0.1:5032" if DEV else "dynamic-simulation-server"
SECURITY_ANALYSIS_SERVER_HOSTNAME = "172.17.0.1:5023" if DEV else "security-analysis-server"
SENSITIVITY_ANALYSIS_SERVER_HOSTNAME = "172.17.0.1:5030" if DEV else "sensitivity-analysis-server"
SHORTCIRCUIT_SERVER_HOSTNAME = "172.17.0.1:5031" if DEV else "shortcircuit-server"
VOLTAGE_INIT_SERVER_HOSTNAME = "172.17.0.1:5038" if DEV else "voltage-init-server"

GRAFANA_HOSTNAME = "172.17.0.1:7000" if DEV else "grafana"
DEV_ELASTICSEARCH_IP = "172.17.0.1"
DEV_ELASTICSEARCH_URL = HTTP_PROTOCOL + "172.17.0.1:9200"


# URLs
GRIDEXPLORE_URL = HTTP_PROTOCOL + GRIDEXPLORE_HOSTNAME

SERVER_URL = HTTP_PROTOCOL + "{serverHostName}" + API_VERSION
STUDY_SERVER_URL = HTTP_PROTOCOL + STUDY_SERVER_HOSTNAME + API_VERSION
NETWORK_STORE_SERVER_URL = HTTP_PROTOCOL + NETWORK_STORE_SERVER_HOSTNAME + API_VERSION
DIRECTORY_SERVER_URL = HTTP_PROTOCOL + DIRECTORY_SERVER_HOSTNAME + API_VERSION
ACTIONS_SERVER_URL = HTTP_PROTOCOL + ACTIONS_SERVER_HOSTNAME + API_VERSION
FILTER_SERVER_URL = HTTP_PROTOCOL + FILTER_SERVER_HOSTNAME + API_VERSION
EXPLORE_SERVER_URL = HTTP_PROTOCOL + EXPLORE_SERVER_HOSTNAME + API_VERSION
CASE_SERVER_URL = HTTP_PROTOCOL + CASE_SERVER_HOSTNAME + API_VERSION
S3_MIGRATION_CASE_SERVER_URL = HTTP_PROTOCOL + S3_MIGRATION_CASE_SERVER_HOSTNAME + API_VERSION

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
GET_ELASTICSEARCH_HOST = SERVER_URL + "/supervision/elasticsearch-host"

GET_NETWORKS = NETWORK_STORE_SERVER_URL + "/networks"
GET_NETWORK = NETWORK_STORE_SERVER_URL + "/networks/{networkId}"
MIGRATE_V211_LIMITS = NETWORK_STORE_SERVER_URL + "/migration/v211limits/{networkId}/{variantNum}"

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
NON_EVACUATED_ENERGY_ANALYSIS = "NON_EVACUATED_ENERGY_ANALYSIS"
SHORTCIRCUIT = "SHORT_CIRCUIT"
VOLTAGE_INIT = "VOLTAGE_INITIALIZATION"

# INDEXED EQUIPMENTS
GET_PLATEFORM_INFO = GRIDEXPLORE_URL + "/idpSettings.json"
DELETE_STUDY_INDEXED_EQUIPMENTS = STUDY_SERVER_URL + "/supervision/studies/{studyUuid}/equipments/indexation"
DELETE_STUDY_INDEXED_EQUIPMENTS_BY_NETWORK_UUID = STUDY_SERVER_URL + "/supervision/studies/{networkUuid}/indexed-equipments-by-network-uuid"
DELETE_STUDY_NODES_BUILDS = STUDY_SERVER_URL + "/supervision/studies/{studyUuid}/nodes/builds"
GET_STUDIES_INDEXED_EQUIPMENTS_COUNT = STUDY_SERVER_URL + "/supervision/equipments/indexation-count"
GET_STUDIES_INDEXED_TOMBSTONED_EQUIPMENTS_COUNT = STUDY_SERVER_URL + "/supervision/tombstoned-equipments/indexation-count"
GET_STUDIES_INDEXED_EQUIPMENTS_INDEX_NAME = STUDY_SERVER_URL + "/supervision/equipments/index-name"
GET_STUDIES_INDEXED_TOMBSTONED_EQUIPMENTS_INDEX_NAME = STUDY_SERVER_URL + "/supervision/tombstoned-equipments/index-name"
GET_ALL_ORPHAN_INDEXED_EQUIPMENTS_NETWORK_UUIDS = STUDY_SERVER_URL + "/supervision/orphan_indexed_network_uuids"

ES_FORCE_MERGE = "{elasticsearchHost}/{indexName}/_forcemerge"

# GRAFANA ENDPOINTS
GRAFANA_FOLDER = GRAFANA_URL + "/folders"
GRAFANA_ALERT_RULES = GRAFANA_URL + API_VERSION + GRAFANA_PROVISIONING + "/alert-rules"
GRAFANA_RULE_GROUPS = GRAFANA_URL + API_VERSION + GRAFANA_PROVISIONING + "/folder/{folderUid}/rule-groups/{ruleGroupId}"

# INDEXED ELEMENTS
GET_DIRECTORY_ELEMENTS_COUNT = DIRECTORY_SERVER_URL + "/supervision/elements/indexation-count"
GET_DIRECTORY_ELEMENTS_INDEX_NAME = DIRECTORY_SERVER_URL + "/supervision/elements/index-name"
DELETE_INDEXED_ELEMENTS = DIRECTORY_SERVER_URL + "/supervision/elements/indexation"
REINDEX_ELEMENTS = DIRECTORY_SERVER_URL + "/supervision/elements/reindex"


# INDEXED ELEMENTS
GET_CASES_ELEMENTS_COUNT = CASE_SERVER_URL + "/supervision/cases/indexation-count"
GET_CASES_ELEMENTS_INDEX_NAME = CASE_SERVER_URL + "/supervision/cases/index-name"
DELETE_INDEXED_CASES_ELEMENTS = CASE_SERVER_URL + "/supervision/cases/indexation"
REINDEX_CASES_ELEMENTS = CASE_SERVER_URL + "/supervision/cases/reindex"

# CASES
GET_ALL_CASES = CASE_SERVER_URL + "/cases"
GET_CASE = CASE_SERVER_URL + "/cases/{caseUuid}"
COPY_CASE = S3_MIGRATION_CASE_SERVER_URL + "/migration/cases"
