#!/bin/bash
export PYTHONPATH=$PYTHONPATH:.
cmd="cat input.txt | python3 sales_taxes/main.py" 
eval $cmd
