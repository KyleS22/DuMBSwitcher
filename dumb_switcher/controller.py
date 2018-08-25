import subprocess
import os
from PIL import Image
from dumb_switcher import DuMBSwitcher as ds
import dumb_switcher.VERSION_NUMBER as vn

# Define storage dircetory for the wallpaper
DUMBSWITCHER_DIR = os.path.expanduser("~/.dumbswitcher/")
WALLPAPER_PATH = DUMBSWITCHER_DIR + "wallpaper.png"

def get_version():
    """
    Get the version number
    :return: A string containing the version number as vn.VERSION_MAJOR.vn.VERSION_MINOR.VERSION_PATCH
    """
    return str(vn.VERSION_MAJOR) + "." + str(vn.VERSION_MINOR) + "." + str(vn.VERSION_PATCH)

def create_wallpaper_file():
    """
    Create the wallpaper storage directory and file so it can be set
    :return: None
    """
    if not os.path.exists(DUMBSWITCHER_DIR):
        os.mkdir(DUMBSWITCHER_DIR)

    if not os.path.exists(WALLPAPER_PATH):
        image = Image.new('RGB', (10, 10))
        image.save(WALLPAPER_PATH)


def create_or_remove_startup_process_for_slideshow(wallpaper_dir, slideshow_duration, switch_both, remove=False):
    """
    Create or remove the startup process for the slideshow so that it can start on boot
    :param wallpaper_dir: The directory to get wallpapers from
    :param slideshow_duration: The time between switching photos
    :param switch_both: Whether or not to switch both monitors at the same time
    :param remove: Remove the slideshow process so that it does not start on boot
    :return: None
    """
    set_wallpaper()

    startup_command_params = ""

    autostart = "true"

    if remove:
        autostart = "false"

    else:
        startup_command_params = " --slideshow_dir=" + wallpaper_dir + " --slideshow_duration=" +\
                                 str(slideshow_duration) + " --start_slideshow"

    if switch_both and not remove:
        startup_command_params += " --switch_both"

    # need python dumb_switcher.py + startup_command_params in startup proc list

    home = os.environ["HOME"]

    name = "dumbswitcher"

    command = "dumb-switcher" + startup_command_params

    launcher = ["[Desktop Entry]", "Name=", "Exec=", "Type=Application", "X-GNOME-Autostart-enabled="]
    dr = home + "/.config/autostart/"

    if not os.path.exists(dr):
        os.makedirs(dr)

    file = dr+name.lower()+".desktop"


    with open(file, "wt") as out:
        out.seek(0)
        out.truncate()

        for l in launcher:
            l = l+name if l == "Name=" else l
            l = l+command if l == "Exec=" else l
            l = l+autostart if l == "X-GNOME-Autostart-enabled=" else l
            out.write(l+"\n")


def set_wallpaper_once(left_wallpaper, right_wallpaper):
    """
    Set the wallpaper without slideshow
    :param left_wallpaper: The wallpaper for the left monitor
    :param right_wallpaper: The wallpaper for the right monitor
    :return: None
    """
    set_wallpaper()

    ds.run(WALLPAPER_PATH, left_wallpaper=left_wallpaper, right_wallpaper=right_wallpaper)


def set_lock_screen():
    """
    Set the lock screen to display the wallpaper
    :return: None
    """
    create_wallpaper_file()

    abs_wallpaper_path = os.path.abspath(WALLPAPER_PATH)

    process = 'gsettings set org.gnome.desktop.screensaver picture-uri file://' + abs_wallpaper_path

    subprocess.call(process, shell=True)

    process = 'gsettings set org.gnome.desktop.screensaver picture-options "spanned"'
    subprocess.call(process, shell=True)


def set_wallpaper():
    """
    Set the wallpaper for the system to the created wallpaper
    :return:
    """
    create_wallpaper_file()

    abs_wallpaper_path = os.path.abspath(WALLPAPER_PATH)

    process = 'gsettings set org.gnome.desktop.background picture-uri file://' + abs_wallpaper_path

    subprocess.call(process, shell=True)

    process = 'gsettings set org.gnome.desktop.background picture-options "spanned"'
    subprocess.call(process, shell=True)
