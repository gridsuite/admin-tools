# Admin-tools
Gridsuite admin tools


## How to use locally
Use locally by settings the `DEV` property to in `scripts/constant.py`
```diff
-DEV = False
+DEV = True
```

Then

```py
python3 [scriptName] [parameters]
```

> **_NOTE:_**  
> Please be sure to exclude 172.17.0.1 from your proxy configuration.    
> export NO_PROXY=localhost,172.17.0.1

some example :

Check Loadflow results number :
```py
python3 scripts/delete_computation_results.py -lf -n
```

Delete Loadflow results definitively :
```py
python3 scripts/delete_computation_results.py -lf
```

## How to use locally with a container

If you want to run a python script via a docker container, please edit the Dockerfile CMD content as you wish, be sure to still activate DEV mode. 

```py
DEV = True
```
And finally:
```docker
docker build . < Dockerfile --tag admin-tools
docker run admin-tools python [SCRIPT_NAME].py [...OPTIONS]
```
**SCRIPT_NAME**: script file name in 'scripts/' folder    
**OPTIONS** :    
    (see individual scripts)    
    common option is :    
    
| -n, --dry-run  | test mode (default) will not execute any deletion or saving request |
| -------------- | ------------------------------------------------------------------- |

## Elasticsearch scripts

You could use `scripts/ES_requests.py` to execute requests on elasticsearch host directly
respecting the REST API documentation (i.e. https://www.elastic.co/guide/en/elasticsearch/reference/current/rest-apis.html)

example:
```py
python3 scripts/ES_requests.py -m GET -u /_cat/indices?v
```

## Grafana scripts
All post requests are sent with the header "X-Disable-Provenance" set to "true". Without it, all created entities would be read-only.
See REST API documentation : https://grafana.com/docs/grafana/v11.3/developers/http_api

### Import existing dashboards JSON
First, we need to create a folder.
Create a folder from the Grafana GUI or execute this command :
```py
python3 scripts/grafana_create_folder.py {{FOLDER_NAME}}
```

This command should return a json with a field "uid" which will be {{FOLDER_UID}} for the next command

Then we can create dashboards in the previously created folder.

To import all dashboards present in **resources/grafana/dashboards**, execute this command :
```py
python3 scripts/grafana_create_dashboards.py -a -p {{FOLDER_UID}}
```

To import a single dashboard or multiple dashboards from files, execute this command :
```py
python3 scripts/grafana_create_dashboards.py -f {{PATH_TO_DASHBOARD_FILE_1}} [... -f {{PATH_TO_DASHBOARD_FILE_N}}] -p {{FOLDER_UID}}
```

### Create a new dashboard JSON file
From local grafana, create the dashboard you want to export as a JSON file

Once done, export it using this curl command :
```
curl localhost:7000/api/dashboards/uid/{{DASHBOARD_UID}} > new_dashboard.json
```
*Note : you can find dashboard UID in URL when inspecting/editing it from grafana UI*

Edit "new_dashboard.json" file, then :
- replace "uid" value by a new value corresponding to a UUID (you can use https://www.uuidgenerator.net/)
- remove all those properties :
    - "id"

*Note: check **resources/grafana/dashboards/users-metrics.json** for a working template file*

Save it in **resources/grafana/dashboards** directory
You can create a subdirectory or use an existing subdirectory

### Import existing alert-rules JSON
First, we need to create a folder.
Create a folder from the Grafana GUI or execute this command :
```py
python3 scripts/grafana_create_folder.py {{FOLDER_NAME}}
```

This command should return a json with a field "uid" which will be {{FOLDER_UID}} for the next command

Then we can create alert-rules in the previously created folder.
Execute this command :
```py
python3 scripts/grafana_create_alerts.py -f {{PATH_TO_ALERT_RULES_1}} -f {{PATH_TO_ALERT_RULES_2}} -d {{DATASOURCE_UID}} -p {{FOLDER_UID}}
```

*Notes:*
- **DATASOURCE_UID** can be found in URL by editing a datasource in grafana UI*
- **FOLDER_UID** can be found in URL by clicking on a folder in grafana UI, "Dashboard" menu

### Create a new alert-rule JSON file
From local grafana, create the alert you want to export as a JSON file

Once done, export it using this curl command :
```
curl localhost:7000/api/v1/provisioning/alert-rules/{{ALERT_RULE_UID}} > new_alert.json
```
*Note : you can find alert rule UID in URL when inspecting/editing it from grafana UI*

Rule-group for evaluation interval must be one of these values : **'alert_eval_group_10s', 'alert_eval_group_30s', 'alert_eval_group_1m', 'alert_eval_group_5m'**

Edit "new_alert.json" file, then :
- replace all "folderUID" values by "{{FOLDER_UID}}
- replace all "datasourceUid" values by "{{DATASOURCE_UID}}"
- replace "uid" value by a new value corresponding to a UUID (you can use https://www.uuidgenerator.net/)
- replace "ruleGroup" by a value present in this list : 'alert_eval_group_10s', 'alert_eval_group_30s', 'alert_eval_group_1m', 'alert_eval_group_5m',
- remove all those properties :
    - "id"
    - "updated"
    - "provenance"

*Note: check **resources/grafana/alerts/computation_queue_alert.json** for a working template file*

Save it in **resources/grafana/alerts** directory

### Edit an existing alert-rule from a JSON file
There is currently no script to update an existing alert-rule

# Clean orphan elements
This python script will send requests to gridsuite services configured in "constant.py" in order to clean orphan elements.
Cleans : 
 - orphan networks
 - orphan contingency lists
 - orphan filters
 - orphan cases
 - orphan studies
 - orphan root networks

Developed with Python version 3.10.12

## Script modes and Execution

Command line to run script using the standard mode (ie will actually remove orphan elements by executing DELETE requests to services) :
<pre>
    python3 scripts/clean_orphan_elements.py
</pre>

Has a test --dry-run mode :
| --dry-run  | this test mode will not modify nor remove any element. It will only display which elements will be deleted if the script is ran in standard mode
<pre>
    python3 scripts/clean_orphan_elements.py --dry-run
</pre>
