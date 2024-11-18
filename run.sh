#!/usr/bin/env bash

EXAMPLE_NUMBER=$1

EXAMPLE_FOLDER="example_$EXAMPLE_NUMBER"

# fucntion that runs the example
run_example() {
    echo hi
}


echo "Running example $EXAMPLE_NUMBER"
if [ -d "$EXAMPLE_FOLDER" ]; then
    cd $EXAMPLE_FOLDER
    run_example
else
    echo "Example folder not found"
fi