import subprocess
import os
from PIL import Image
import DuMBSwitcher as ds


DUMBSWITCHER_DIR = os.path.expanduser("~/.dumbswitcher/")
WALLPAPER_PATH = DUMBSWITCHER_DIR + "wallpaper.png"


def create_wallpaper_file():
    if not os.path.exists(DUMBSWITCHER_DIR):
        os.mkdir(DUMBSWITCHER_DIR)

    if not os.path.exists(WALLPAPER_PATH):
        image = Image.new('RGB', (10, 10))
        image.save(WALLPAPER_PATH)

def create_or_remove_startup_process_for_slideshow(wallpaper_dir, slideshow_duration, switch_both, remove=False):

    set_wallpaper()

    startup_command_params = " --slideshow_dir=" + wallpaper_dir +\
                      " --slideshow_duration=" + str(slideshow_duration) + " --start_slideshow"

    if switch_both:
        startup_command_params += " --swtich_both"

    # need python dumb_switcher.py + startup_command_params in startup proc list

    home = os.environ["HOME"]

    name = "dumbswitcher"

    # TODO: This command might not be right either

    command = "dumb_switcher" + startup_command_params

    autostart = "true"

    if remove:
        autostart = "false"

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

    set_wallpaper()

    ds.run(WALLPAPER_PATH, left_wallpaper=left_wallpaper, right_wallpaper=right_wallpaper)

def set_lock_screen():
    create_wallpaper_file()

    abs_wallpaper_path = os.path.abspath(WALLPAPER_PATH)

    process = 'gsettings set org.gnome.desktop.screensaver picture-uri file://' + abs_wallpaper_path

    subprocess.call(process, shell=True)

    process = 'gsettings set org.gnome.desktop.screensaver picture-options "spanned"'
    subprocess.call(process, shell=True)

def set_wallpaper():

    create_wallpaper_file()

    abs_wallpaper_path = os.path.abspath(WALLPAPER_PATH)

    process = 'gsettings set org.gnome.desktop.background picture-uri file://' + abs_wallpaper_path

    subprocess.call(process, shell=True)

    process = 'gsettings set org.gnome.desktop.background picture-options "spanned"'
    subprocess.call(process, shell=True)
