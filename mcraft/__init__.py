"""
Load all the goodies.
"""
from pathlib import Path
try:
    from utils import download_if_not_exist
    from networks import TNet
except (ImportError, ModuleNotFoundError):
    from .utils import download_if_not_exist
    from .networks import TNet

base_url = 'https://huggingface.co/Manbehindthemadness/craft_mlt_25k/resolve/main/'
models = ['craft_mlt_25k.pth', 'craft_refiner_CTW1500.pth']
for model_name in models:
    model_path = Path('~/.cache/mcraft').expanduser()
    download_if_not_exist(model_path, f'{base_url}{model_name}')
