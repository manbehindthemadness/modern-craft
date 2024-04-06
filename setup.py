from setuptools import setup, find_packages
import importlib.util

install_requires = [
    'scikit-image>=0.14.2',
    'scipy>=1.1.0',
    'numpy'
]


"""
Try to not overwrite hand-compiled versions...
"""

if importlib.util.find_spec("cv2") is None:  # Check if cv2 is not installed
    install_requires.append('opencv-python>=3.4.2.17')
if importlib.util.find_spec("torch") is None:  # Check if torch is not installed
    install_requires.append('torch>=2.0.0')
if importlib.util.find_spec("torchvision") is None:  # Check if torchvision is not installed
    install_requires.append('torchvision>=0.17.0')


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='mcraft',
    version='0.0.1',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
        ],
    },
    author='Manbehindthemadness',
    author_email='manbehindthemadness@gmail.com',
    description='A modern version of CRAFT-pytorch using the latest versions',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/manbehindthemadness/modern-craft',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
