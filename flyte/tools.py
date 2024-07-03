import os


def find_directories_with_extensions(root_dir, extensions):
    """
    Finds directories within root_dir containing files with specified extensions.

    :param root_dir: The root directory to search.
    :param extensions: A list of file extensions to look for.
    :return: A list of directories containing files with the specified extensions.
    """
    directories = set()
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in extensions):
                directories.add(dirpath)
                break  # Stop checking other files in this directory
    return list(directories)
