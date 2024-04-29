# Admin-tools
Gridsuite admin tools


## How to use locally
Use locally by settings the `DEV` property to in `constant.py`
```diff
-DEV = False
+DEV = True
```

Then

```py
python3 [scriptName] [parameters]
```

some example :

Check Loadflow results number :
```py
python3 delete_computation_results.py -lf -n
```

Delete Loadflow results definitively :
```py
python3 delete_computation_results.py -lf
```

## Grafana scripts
All post requests are sent with the header "X-Disable-Provenance" set to "true". Without it, all created entities would be read-only.
### Import existing alert-rules JSON
First, we need to create a folder.
Execute this command :
```py
python3 grafana_create_folder.py {{FOLDER_NAME}}
```

This command should return a json with a field "uid" which will be {{FOLDER_UID}} for the next command

Then we can create alert-rules in the previously created folder.
**Default interval value for rule-group is 60s. If you want a different value, use "-i" option (run "python3 grafana_create_alerts.py -h" for more infos**
Execute this command :
```py
python3 grafana_create_alerts.py -f {{PATH_TO_ALERT_RULES_1}} -f {{PATH_TO_ALERT_RULES_2}} -d {{DATASOURCE_UID}} -p {{FOLDER_UID}}
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

Edit "new_alert.json" file, then :
- replace all "folderUID" values by "{{FOLDER_UID}}
- replace all "datasourceUid" values by "{{DATASOURCE_UID}}"
- remove all those properties :
    - "uid"
    - "id"
    - "updated"
    - "provenance"

*Note: check **resources/grafana/alert-rules/computation-alert-rule.json** for a working template file*

Save it in **resources/grafana/alert-rules** directory

### Edit an existing alert-rule from a JSON file
There is currently no script to update an existing alert-rule
