# Setup

* `pip install -r requirements-dev.txt`

# Run
* `cat input.txt | PYTHONPATH=$PYTHONPATH:. python sales_taxes/main.py`
* `input.txt` should contain the inputs.

# Tests
* `PYTHONPATH=$PYTHONPATH:. py.test tests`

