from setuptools import setup, find_packages
# pyrcc5 img.qrc -o icons.py
setup(
    name='my_project',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'my_project=my_project.main:main',
        ],
    },
)
