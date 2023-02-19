def test_folder_file():
    """
    Creates testing folder to place things in.
    Creates testing file to place things in.
    """
    from pathlib import Path

    test_folder = Path.cwd() / 'test_folder'
    test_file = test_folder / 'test_file.txt'
    test_folder.mkdir(exist_ok=True)
    test_file.touch(exist_ok=True)
    
    return test_folder, test_file
