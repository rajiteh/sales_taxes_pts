# Setup

* `pip install -r requirements-dev.txt`

# Run
* `cat input.txt | PYTHONPATH=$PYTHONPATH:sales_taxes/ python sales_taxes/main.py`
* `input.txt` should contain the inputs.

# Tests
* `PYTHONPATH=$PYTHONPATH:sales_taxes/:tests/ py.test tests/`

