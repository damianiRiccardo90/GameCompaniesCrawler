from setuptools import setup, find_packages

setup(
    name='crawlerproject',
    version='1.0',
    packages=find_packages(),
    package_data={
        'crawlerproject': [
            'data/game_companies/*.html'
        ],
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'crawlerproject = crawlerproject.__main__:main',
        ],
    },
)