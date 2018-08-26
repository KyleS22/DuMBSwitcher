# What is it?
DuMBSwitcher is a command line tool for Ubuntu Gnome that allows you to set different wallpapers on a dual monitor setup.  You can use it to set each 
monitor to a different image, or to display a timed slideshow of images on both monitors. 

# Installation
Note that only Ubuntu Gnome is currently supported.

DuMBSwitcher requires python 3.6.5 to operate.  If you don't already have it, you can get it [here](https://www.python.org/).

To install DuMBSwitcher, download the 
[latest release](https://github.com/KyleS22/DuMBSwitcher/releases/latest) and install using

`pip3 install DuMBSwitcher-x-x-x.tar.gz`

Check that the install worked using `dumb-switcher --version`.

# Usage
DuMBSwitcher works by creating one giant image made from two smaller images to fit the exact dimensions and positions of your monitors.  Once you have installed it, you can use these commands to get started:

### Set wallpaper once

To set each monitor to one static wallpaper, use:

`dumb-switcher --left_wallpaper=ABSOLUTE/PATH/TO/IMAGE --right_wallpaper=ABSOLUTE/PATH/TO/IMAGE`

### Set up a timed slideshow

You can also set the background to switch between the images in a directory of images:

`dumb-switcher --slideshow_dir=PATH/TO/IMAGES/ --slideshow_duration=SECONDS_FOR_EACH_IMAGE`

The above command will set the slideshow as a startup application, to start the slideshow now you can use:

`dumb-switcher --slideshow_dir=PATH/TO/IMAGES/ --slideshow_duration=SECONDS_FOR_EACH_IMAGE --start_slideshow &`

This will start a background process for the slideshow and add it to the startup applications list

#### Switch both images at the same time in the slideshow

By default, only one image will change at a time during a slideshow.  This means that if your slideshow_duration is set to 60 seconds (one minute), the left monitor will change in one minute, then one minute later the right monitor will change, then the left again in ten minutes, etc.

To disable this and have both images change at the same time, simply add the `--switch_both` option:

`dumb-switcher --slideshow_dir=PATH/TO/IMAGES/ --slideshow_duration=SECONDS_FOR_EACH_IMAGE --start_slideshow --switch_both &`

#### Stop the slideshow

To stop the slideshow, you can use `dumb-switcher --stop_slideshow`.  This will disable the startup application.

### Enable the lock screen to show the current background image

You can also set the lock screen to mimic the desktop background using

 `dumb-switcher --enable_lock_screen`

More details about usage and options can be found with `dumb-switcher -h`.