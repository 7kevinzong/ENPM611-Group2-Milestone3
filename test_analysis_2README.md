# Test Analysis 2

This analysis includes four test cases:

1. **Test reading dataset ID**
2. **Test if `config.get_parameter` is not called, DATASET defaults to 0**
3. **Test creating and showing graph**
4. **Test empty issue handling**

## Commands Run in Terminal

The following commands were executed to run the tests and generate the coverage report:

```bash
coverage run --source=analysis_2 -m unittest test_analysis_2.py
coverage report -m
```

## Coverage Report

The output of the coverage report is as follows:

```
Name            Stmts   Miss  Cover   Missing
---------------------------------------------
analysis_2.py      63      1    98%   54
---------------------------------------------
TOTAL              63      1    98%
```

### Notes

- The coverage report indicates `analysis_2.py`has 98% test coverage, with one line (line 54) not covered.
