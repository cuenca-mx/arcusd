from setuptools import setup, find_packages

setup(
    name='arcusd',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['Click'],
    entry_points='''
        [console_scripts]
        arcusd=arcusd.commands.arcusd_command:arcusd_cli
    ''',
)
