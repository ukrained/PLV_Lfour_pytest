import os


def test_case1_ilpt(setup_fs):
    """ test simple fs commands """
    # get initial data
    dirname, filepath, test_string = setup_fs

    # check directory exists
    assert os.path.exists(dirname)

    # check file exists
    assert os.path.exists(filepath)

    # check file content matches
    with open(filepath, 'r') as fp:
        assert fp.read() == test_string