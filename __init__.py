
def teardown_module(module):
    print("Here must be some code, that will initialise testing DB to be cleaned from test data. \nJust in case if this step is not implemented in the pipeline.")
#Or instead of teardown method, there can be tearup one, which will do the same, will clean testing environment before a test run.