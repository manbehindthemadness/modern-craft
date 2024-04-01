from setuptools import setup, find_packages

print('THIS PACHAGE REQUIRES OPENCV; HOWEVER, IT"S NOT GOING TO BE AUTOMATICALLY INSTALLED')
setup(
    name='mcraft',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'torch>=2.0.0',
        'torchvision>=0.17.0',
        'opencv-python>=3.4.2.17',
        'scikit-image>=0.14.2',
        'scipy>=1.1.0',
        'numpy'
    ],
    entry_points={
        'console_scripts': [
        ],
    },
    author='Manbehindthemadness',
    author_email='manbehindthemadness@gmail.com',
    description='A modern version of CRAFT-pytorch using the latest versions',
    long_description_content_type='text/markdown',
    url='https://github.com/manbehindthemadness/modern-craft',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
