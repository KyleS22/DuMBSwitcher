# DuMBSwitcher
### Dual Monitor Background Switcher
DuMBSwitcher is a command line tool for configuring wallpapers on multi monitor Ubuntu Gnome setups.  It allows a different wallpaper to be displayed on each monitor, as well as a slideshow of images to be displayed as the wallpaper on both monitors.

## Build Status
| Service | Master | Development |
|---------|--------|-------------|
| CI      |[![Build Status](https://travis-ci.org/KyleS22/DuMBSwitcher.svg?branch=master)](https://travis-ci.org/KyleS22/DuMBSwitcher) | [![Build Status](https://travis-ci.org/KyleS22/DuMBSwitcher.svg?branch=development)](https://travis-ci.org/KyleS22/DuMBSwitcher)| 

# Installation
You can install DuMBSwitcher by downloading the [latest release](https://github.com/KyleS22/DuMBSwitcher/releases/latest) tar file and running 

`pip install DuMBSwitcher-x.x.x.tar.gz`



# Tests
Tests can be run with `pytest`

Tests with coverage can be run with `pytest --cov=dumb_switcher --cov-branch --cov-report term-missing`
