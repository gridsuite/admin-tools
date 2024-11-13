# Admin-tools
Gridsuite admin tools


## How to use locally
Use locally by settings the `DEV` property to in `scripts/constant.py`
```diff
-DEV = False
+DEV = True
```

Then

```shell
python3 [scriptName] [parameters]
```

> [!NOTE]
> Please be sure to exclude 172.17.0.1 from your proxy configuration.    
> ```shell
> export NO_PROXY=localhost,172.17.0.1
> ```

Some examples:

* Check Loadflow results number :
  ```shell
  python3 scripts/delete_computation_results.py -lf -n
  ```

* Delete Loadflow results definitively :
  ```shell
  python3 scripts/delete_computation_results.py -lf
  ```


## How to use locally with a container

If you want to run a python script via a docker container, please edit the Dockerfile CMD content as you wish, be sure to still activate DEV mode. 

```python
DEV = True
```
And finally:
```shell
docker build . < Dockerfile --tag admin-tools
docker run admin-tools [SCRIPT_NAME].py [...OPTIONS]
```
**SCRIPT_NAME**: script file name in 'scripts/' folder  
**OPTIONS** :  
_(see individual scripts)_  
Common options is :  
| Parameter      | Description                                                         |
| -------------- | ------------------------------------------------------------------- |
| -n, --dry-run  | test mode (default) will not execute any deletion or saving request |


## Scripts

### Elasticsearch scripts

You could use `scripts/ES_requests.py` to execute requests on elasticsearch host directly
respecting the REST API documentation (i.e. https://www.elastic.co/guide/en/elasticsearch/reference/current/rest-apis.html)

example:
```shell
python3 scripts/ES_requests.py -m GET -u /_cat/indices?v
```

### Grafana scripts
All post requests are sent with the header "X-Disable-Provenance" set to "true". Without it, all created entities would be read-only.

#### Import existing alert-rules JSON
First, we need to create a folder.
Execute this command :
```shell
python3 scripts/grafana_create_folder.py {{FOLDER_NAME}}
```

This command should return a json with a field "uid" which will be {{FOLDER_UID}} for the next command.

Then we can create alert-rules in the previously created folder.  
**Default interval value for rule-group is 60s. If you want a different value, use "-i" option _(run `python3 scripts/grafana_create_alerts.py -h` for more infos_).**  
Execute this command :
```shell
python3 scripts/grafana_create_alerts.py -f {{PATH_TO_ALERT_RULES_1}} -f {{PATH_TO_ALERT_RULES_2}} -d {{DATASOURCE_UID}} -p {{FOLDER_UID}}
```

> [!NOTE]
> - `DATASOURCE_UID` can be found in URL by editing a datasource in grafana UI
> - `FOLDER_UID` can be found in URL by clicking on a folder in grafana UI, "Dashboard" menu

#### Create a new alert-rule JSON file
From local grafana, create the alert you want to export as a JSON file
Once done, export it using this curl command :
```shell
curl localhost:7000/api/v1/provisioning/alert-rules/{{ALERT_RULE_UID}} > new_alert.json
```
> [!NOTE]
> You can find alert rule UID in the URL when inspecting/editing it from grafana UI.

Edit `new_alert.json` file, then :
- replace all `folderUID` values by `{{FOLDER_UID}}`
- replace all `datasourceUid` values by `{{DATASOURCE_UID}}`
- remove all those properties :
    - `uid`
    - `id`
    - `updated`
    - `provenance`

> [!NOTE]
> Check `/scripts/resources/grafana/alert-rules/computation-alert-rule.json` for a working template file.

Save it in `/scripts/resources/grafana/alert-rules` directory.

#### Edit an existing alert-rule from a JSON file
There is currently no script to update an existing alert-rule.
