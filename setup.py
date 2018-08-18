from setuptools import setup


setup(
    name='dumb_switcher',
    version='0.1.0',
    packages=['dumb_switcher'],
    entry_points = {
        'console_scripts': ['dumb-switcher=dumb_switcher.CLI:main'],
    },
    description="Command line tool for setting dual monitor wallpapers on ubuntu gnome.",
    install_requires = [
        'Pillow',
    ]
)