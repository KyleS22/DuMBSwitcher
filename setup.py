from setuptools import setup
import dumb_switcher.controller as controller

setup(
    name='dumb_switcher',
    version=controller.get_version(),
    packages=['dumb_switcher'],
    entry_points = {
        'console_scripts': ['dumb-switcher=dumb_switcher.CLI:main'],
    },
    description="Command line tool for setting dual monitor wallpapers on ubuntu gnome.",
    install_requires = [
        'Pillow',
    ],
    setup_requires = [
        'Pillow',
    ]
)