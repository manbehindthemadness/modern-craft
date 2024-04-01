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
    path.mkdir(parents=True, exist_ok=True)
    file_name = url.split('/')[-1]
    file_path = path / file_name
    if not file_path.exists():
        print(f"Downloading {path.name} from {url}...")
        urllib.request.urlretrieve(url, file_path)
        print("Download complete!")
    else:
        print(f"Confirmed {file_path} exists")


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

