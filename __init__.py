# Used once before running all the package tests
def setup_module(module):
# Here must be some code, that will initialise testing DB to be cleaned from previous test data.
# Just in case if this step is not a part of a pipeline.
# Or instead of setup method, there can be teardown one, which will do the same,
# but in the end, will clean testing environment after a test run.

    print("\n\nPreparing files for storing additional test data\n")
    with open("users.txt", "w") as file:
        file.write("Created valid users:")
        file.close()
