from setuptools import setup, find_packages

setup(
    name='plutoid_web',
    version='0.1.2',
    packages=find_packages(),
    include_package_data=True,
    url = "https://github.com/manasgarg/plutoid-web",
    install_requires=[
        'Click', 'blinker>=1.4', 'numpy>=1.13.1', 'matplotlib>=2.0.2'
    ],
    entry_points='''
        [console_scripts]
        plutoidweb=plutoid_web.scripts.plutoidweb:main
    ''',
)
