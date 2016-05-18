# Requirements
* Python version 3 or higher.
* Tested only on Mac/Linux

# Run
* `./run.sh` OR `cat input.txt | PYTHONPATH=$PYTHONPATH:. python3 sales_taxes/main.py`
* `input.txt` should contain the inputs.

# Tests
* `pip install -r requirements-dev.txt`
* `./test.sh` OR `PYTHONPATH=$PYTHONPATH:.:sales_taxes/ py.test tests`

# Design thoughts

I architected the application to be as flexible as possible to any changes 
to the business rules. As a result, taxation and rounding were abstracted out
from the core shopping cart logic. This allows future maintainers to modify
the taxation rules and rounding logic without affecting the core business logic
of the shopping cart. Furthermore, the separation of concerns results in easily
testable and cleaner code (IMO).

I also approached modifying the cart in a defensive manner where the code
that deals with manipulation of cart objects are executed wrapped in a function
which reverts any changes made to the cart in case an exception occurs.

# Classes

* `main.py` - Program entry point and input parsing
* `cart.py` - Shopping cart logic
* `product.py` - A product that can be added to the cart
* `rounding_policy.py` - A tax rounding policy 
* `tax_definition.py` - A tax rule 
