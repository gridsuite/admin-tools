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
