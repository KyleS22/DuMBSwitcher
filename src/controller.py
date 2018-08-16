import subprocess
import os
from PIL import Image
import DuMBSwitcher as ds


dumbswitcher_dir = os.path.expanduser("~/.DuMBSwitcher/")
wallpaper_path = dumbswitcher_dir + "wallpaper.png"


def create_wallpaper_file():
    if not os.path.exists(dumbswitcher_dir):
        os.mkdir(dumbswitcher_dir)

    if not os.path.exists(wallpaper_path):
        image = Image.new('RGB', (10, 10))
        image.save(wallpaper_path)

def create_startup_process_for_slideshow(wallpaper_dir, slideshow_duration, switch_both):


    startup_command_params = wallpaper_path + " --slideshow_dir=" + wallpaper_dir +\
                      " --slideshow_duration=" + str(slideshow_duration)

    # need python DuMBSwitcher.py + startup_command_params in startup proc list


def set_wallpaper_once(left_wallpaper, right_wallpaper):

    set_wallpaper()

    ds.run(wallpaper_path, left_wallpaper=left_wallpaper, right_wallpaper=right_wallpaper)

def set_lock_screen():
    create_wallpaper_file()

    abs_wallpaper_path = os.path.abspath(wallpaper_path)

    process = 'gsettings set org.gnome.desktop.screensaver picture-uri file://' + abs_wallpaper_path

    subprocess.call(process, shell=True)

    process = 'gsettings set org.gnome.desktop.screensaver picture-options "spanned"'
    subprocess.call(process, shell=True)

def set_wallpaper():

    create_wallpaper_file()

    abs_wallpaper_path = os.path.abspath(wallpaper_path)

    process = 'gsettings set org.gnome.desktop.background picture-uri file://' + abs_wallpaper_path

    subprocess.call(process, shell=True)

    process = 'gsettings set org.gnome.desktop.background picture-options "spanned"'
    subprocess.call(process, shell=True)