# Test Data loader

This analysis includes five test cases:

1. Test if the JSON file is empty, ensuring it returns an empty list.
2. Test error handling when the data is malformed.
3. Test that passing invalid dataset indices to the data loader raises a `ValueError`.
4. Test that the data loader selects the correct dataset path based on the dataset index.
5. Test the `get_issues` method.

## Commands Run in Terminal

The following commands were executed to run the tests and generate the coverage report:

```bash
coverage run --source=data_loader -m unittest test_data_loader.py
coverage report -m
```

## Coverage Report

The output of the coverage report is as follows:

```
Name             Stmts   Miss  Cover   Missing
----------------------------------------------
data_loader.py      22      1    95%   49
----------------------------------------------
TOTAL               22      1    95%
```

### Notes

- The coverage report indicates `data_loader.py`has 95% test coverage, with one line (line 49) not covered.
