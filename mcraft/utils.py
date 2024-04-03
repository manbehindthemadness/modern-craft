import os
import shutil
import zipfile
import urllib.request
from pathlib import Path
from collections import OrderedDict


def download_if_not_exist(path: Path, url: str):
    """
    Checks if a file specified by path exists. If not, downloads it from the given URL.

    Args:
        path (Path): The path to the file.
        url (str): The URL from which to download the file.
    """
    def remove_file_or_folder(_path: Path):
        """
        Aptly named...
        """
        if file_path.is_file():
            os.remove(_path)
        elif file_path.is_dir():
            shutil.rmtree(_path)

    path.mkdir(parents=True, exist_ok=True)
    file_name = url.split('/')[-1]
    file_path = path / file_name
    if not file_path.exists():
        print(f"Downloading {file_name} from {url}...")
        urllib.request.urlretrieve(url, file_path)
        print(f"Download complete: {file_path.as_posix()}")
        if zipfile.is_zipfile(file_path):
            folder_path = path / Path(file_name).stem
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(folder_path.parent)
            remove_file_or_folder(file_path)
            print(f"Decompressed zip archive to {folder_path.as_posix()}")
            file_path.touch()  # add a placeholder, so we know we don't have to re-download.
    else:
        finished_message = f"Confirmed {file_path} exists"
        file_extension = file_name.split('.')[-1]
        if file_extension.lower() == 'zip':
            zip_file_size = os.path.getsize(file_path)
            if zip_file_size > 0:
                print(f"partial ZIP file: {zip_file_size} bytes, re-downloading...")
                remove_file_or_folder(file_path)
                download_if_not_exist(path, url)
            else:
                print(finished_message)
        else:
            print(finished_message)


def copy_state_dict(state_dict):
    if list(state_dict.keys())[0].startswith("module"):
        start_idx = 1
    else:
        start_idx = 0
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = ".".join(k.split(".")[start_idx:])
        new_state_dict[name] = v
    return new_state_dict


def str2bool(v):
    return v.lower() in ("yes", "y", "true", "t", "1")


def fix_path(file_path: [Path, str]) -> Path:
    """
    This just ensures that the path is properly expanded for home folder annotations.
    """
    result = file_path
    if isinstance(file_path, str):
        result = Path(file_path)
        if '~' in file_path:
            result = result.expanduser()
    elif isinstance(file_path, Path):
        if '~' in file_path.as_posix():
            result = result.expanduser()
    return result
