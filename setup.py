from setuptools import setup, find_packages
try:
    from install_preserve import preserve
except ImportError:
    import pip  # noqa
    pip.main(['install', 'install-preserve'])
    from install_preserve import preserve  # noqa

install_requires = [
    'scikit-image>=0.14.2',
    'scipy>=1.1.0',
    'numpy',
    'opencv-python>=3.4.2.17',
    'torch>=2.0.0',
    'torchvision>=0.17.0'
]

excludes = [
    'opencv-python:cv2',
    'torch',
    'torchvision'
]

install_requires = preserve(install_requires, excludes, verbose=True)


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
