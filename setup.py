from setuptools import setup
import dumb_switcher.VERSION_NUMBER as vn

setup(
    name='dumb_switcher',
    version=str(vn.VERSION_MAJOR) + "." + str(vn.VERSION_MINOR) + "." + str(vn.VERSION_PATCH),
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
