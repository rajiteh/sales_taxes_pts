#!/bin/bash
export PYTHONPATH=$PYTHONPATH:.:sales_taxes/
cmd="py.test tests/" 
eval $cmd
