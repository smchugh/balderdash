old_python_path=`echo $PYTHONPATH`
current_path=`pwd`

# Add current project path to python path
export PYTHONPATH="$current_path":$PYTHONPATH

# Run all tests
# TODO replace with loop through all files in integration/unit, skipping 'common'
APPLICATION_ENV=testing python $current_path/tests/integration/Players.py
APPLICATION_ENV=testing python $current_path/tests/integration/Games.py
APPLICATION_ENV=testing python $current_path/tests/integration/DefinitionFillers.py
APPLICATION_ENV=testing python $current_path/tests/integration/DefinitionTemplates.py

# Reset the python path
export PYTHONPATH="$old_python_path"
