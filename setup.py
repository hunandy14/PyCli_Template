from setuptools import setup, find_packages

setup(
    name='MyApp',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'myapp=myapp.cli.config:entry',
        ],
    },
    include_package_data=True
)
