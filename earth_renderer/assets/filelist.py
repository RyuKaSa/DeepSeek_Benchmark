import os

def list_png_files(root_dir='.'):
    """
    Lists all PNG files in the given directory and its subdirectories.

    Args:
        root_dir (str): The path of the directory to start searching from. Defaults to '.'.

    Returns:
        list: A list of full paths of PNG file names.
    """
    png_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.png'):
                png_files.append(os.path.join(dirpath, filename))
    return png_files

png_files = list_png_files()
print(png_files)