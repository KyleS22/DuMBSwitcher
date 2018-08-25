from setuptools import setup

VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_PATCH = 2


setup(
    name='dumb_switcher',
    version=str(VERSION_MAJOR) + "." + str(VERSION_MINOR) + "." + str(VERSION_PATCH),
    packages=['dumb_switcher'],
    entry_points={
        'console_scripts': ['dumb-switcher=dumb_switcher.CLI:main'],
    },
    description="Command line tool for setting dual monitor wallpapers on ubuntu gnome.",
    install_requires=[
        'Pillow',
    ],
    setup_requires=[
        'Pillow',
    ]
)
