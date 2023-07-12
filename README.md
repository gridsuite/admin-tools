# admin-tools
Gridsuite admin tools

# Clean orphan elements
This python script will send requests to gridsuite services configured in "constant.py" in order to clean orphan elements

Developed with Python version 3.8.10

## Script modes

Two executions modes are available :
- **exec** : this mode will actually remove orphan elements by executing DELETE requests to services
- **test** (default) : this mode will not modify nor remove any element. It will only display which element will be delete if script is ran with "exec" mode

## Execution

Command line to run script with "exec" mode :
<pre>
    python clean_oprhans_element.py --mode=exec
</pre>

