import argparse
from PIL import Image

import re
import subprocess
import os
import random
import time


def parse_screen_properties_to_resolution_and_position(resolutions):
    """
    Parse a list of resolutions of the format ####x####+####+#### into width, height, x_position, y_position
    :param resolutions: A list of resolutions in the form ####x####+####+####
    :return: A list of dictionaries of the form {'width': #, 'height': #, 'x_pos': #, 'y_pos': #}
    """

    parsed_resolutions = []
    num_pattern = re.compile("[0-9]+")


    for res in resolutions:
        d = {}
        width, more = res.split('x')

        d["width"] = int(width)
        split = more.split('+')

        d["height"] = int(split[0])
        d["x_pos"] = int(split[1])
        d["y_pos"] = int(split[2])

        parsed_resolutions.append(d)

    return parsed_resolutions

def get_screen_properties():
    """
    Retreive the properties of the current screen using xrandr
    :return: A dictionary containing the screen_space and resolutions and positons of monitors
    """

    properties = {}

    # Get current screen space
    xrandr_screen = subprocess.Popen('xrandr | grep "current [0-9]* x [0-9]*"', shell=True, stdout=subprocess.PIPE).communicate()[0]

    screen_pattern = re.compile("current [0-9]* x [0-9]*")

    screen_space = []

    for screen_prop in xrandr_screen.split(b', '):
        decoded_str = screen_prop.decode("utf-8")

        if screen_pattern.match(decoded_str):
            for string in decoded_str.split():
                pattern = re.compile("[0-9]+")
                if pattern.match(string):
                    screen_space.append(int(string))

    properties["screen_space"] = screen_space

    # Get screen resolutions
    xrandr_out = subprocess.Popen('xrandr | grep "[0-9]*x[0-9]*+[0-9]*+[0-9]*"', shell=True, stdout=subprocess.PIPE).communicate()[0]

    resolutions = []

    pattern = re.compile("[0-9]*x[0-9]*\+[0-9]*\+[0-9]*")

    for res in xrandr_out.split():
        decoded_str = res.decode("utf-8")
        if pattern.match(decoded_str):
            resolutions.append(decoded_str)

    properties["resolutions"] = parse_screen_properties_to_resolution_and_position(resolutions)

    return properties

def create_background_image(screen_properties, left_image, right_image, out_file):
    """
    Create a new background image to fit the current monitor setup
    :param screen_properties: A dictionary containg the specifications of the monitors and the space they are in
    :param left_image: The path to the image to go on the left monitor
    :param right_image: The path to the image to go on the right monitor
    :param out_file: The file to save the new image to
    :return: None
    """

    screen_width = screen_properties["screen_space"][0]
    screen_height = screen_properties["screen_space"][1]


    monitors = screen_properties["resolutions"]

    if len(monitors) > 2:
        raise NotImplementedError("More than 2 monitors is not supported")
    elif len(monitors) < 2:
        raise NotImplementedError("You should probably just use the default wallpaper switcher")

    mon_1 = monitors[0]
    mon_2 = monitors[1]

    if mon_1["x_pos"] < mon_2["x_pos"]:
        left_monitor = mon_1
        right_monitor = mon_2

    elif mon_1["x_pos"] > mon_2["x_pos"]:
        left_monitor = mon_2
        right_monitor = mon_1
    else:
        raise ValueError("Monitors are overlapping!")


    left_image = Image.open(left_image, 'r')
    right_image = Image.open(right_image, 'r')

    # Scale the images to fit the monitors
    basewidth_left = left_monitor["width"]

    wpercent_left = (basewidth_left/float((left_image.size[0])))
    hsize_left = int((float(left_image.size[1]) * float(wpercent_left)))

    left_image = left_image.resize((basewidth_left, hsize_left), Image.ANTIALIAS)

    basewidth_right = right_monitor["width"]

    wpercent_right = (basewidth_right / float((right_image.size[0])))
    hsize_right = int((float(right_image.size[1]) * float(wpercent_right)))

    right_image = right_image.resize((basewidth_right, hsize_right), Image.ANTIALIAS)

    background = Image.new('RGBA', [screen_width, screen_height], (255, 255, 255, 255))

    background.paste(left_image, (left_monitor["x_pos"],left_monitor["y_pos"]))

    background.paste(right_image, (right_monitor["x_pos"], right_monitor["y_pos"]))

    background.save(out_file)

def start_slideshow(slideshow_dir, switch_both, slideshow_duration, properties, wallpaper_out):
    """
    Start the slideshow by creating the image and then sleeping for the specified duration.
    :param slideshow_dir: The directory to get wallpapers from
    :param switch_both: If true, both monitors will be switched at the same time, rather than seperately.
    :param slideshow_duration: The amount of time to wait before changing wallpapers.
    :param properties: The properties of the screen
    :param wallpaper_out: The place to save the wallpaper to
    :return: None
    """

    image_to_switch = 1

    new_image_1 = None
    new_image_2 = None

    while True:

            new_image_1, new_image_2 = choose_next_images(slideshow_dir, new_image_1, new_image_2, switch_both,
                                                          image_to_switch)

            create_background_image(properties, new_image_1, new_image_2, wallpaper_out)

            if not switch_both:
                image_to_switch += 1

                if image_to_switch >= 3:
                    image_to_switch = 1

            time.sleep(slideshow_duration)

def choose_next_images(slideshow_dir, image1=None, image2=None, switch_both=False, image_to_switch=1):
    """
    Choose the next images to be displayed on each monitor
    :param slideshow_dir: The directory to get the images from
    :param image1: The current first image
    :param image2: The current second image
    :param switch_both: if True both monitor's wallpapers will be switched at the same time.  If False, only one will be
    switched at a time
    :param image_to_switch: The image to switch.  Only applies if switch_both is false.  1 indexed to match the variable names
    for the images (image1, image2)
    :return: (new_image1, new_image2) where both values of the tuple are paths to the chosen wallpapers
    """

    images = os.listdir(slideshow_dir)

    new_image1 = image1
    new_image2 = image2

    if switch_both or image2 is None:

        while new_image1 == image1 or new_image1 == image2:
            new_image1 = os.path.join(slideshow_dir, random.choice(images))

        while new_image2 == image1 or new_image2 == image2 or new_image2 == new_image1:
            new_image2 = os.path.join(slideshow_dir, random.choice(images))

    else:
        if image_to_switch == 1:
            while new_image1 == image1 or new_image1 == image2:
                new_image1 = os.path.join(slideshow_dir, random.choice(images))

        elif image_to_switch == 2:
            while new_image2 == image2 or new_image2 == image1:
                new_image2 = os.path.join(slideshow_dir, random.choice(images))

    return new_image1, new_image2


def run(wallpaper_out, slideshow=False, slideshow_duration=0, switch_both_monitors=False, left_wallpaper=None, right_wallpaper=None, slideshow_dir=None):

    properties = get_screen_properties()

    if slideshow:
        start_slideshow(slideshow_dir, switch_both_monitors, slideshow_duration, properties, wallpaper_out)

    else:
        create_background_image(properties, left_wallpaper,
                             right_wallpaper, wallpaper_out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a spanned wallpaper out of two images to fit on two monitors.")

    parser.add_argument("wallpaper_out", help="The path to store the resulting wallpaper at")
    parser.add_argument("--left_wallpaper", help="The wallpaper to display on the left monitor")
    parser.add_argument("--right_wallpaper", help="The wallpaper to display on the right monitor")
    parser.add_argument("--slideshow_dir", help="The directory to get wallpapers from for a slideshow")
    parser.add_argument("--switch_both", action="store_true", help="Switch both monitors at the same time")
    parser.add_argument("--slideshow_duration", help="The amount of time before switching a wallpaper.")


    args = parser.parse_args()

    if args.slideshow_dir is None:
        if args.left_wallpaper is None or args.right_wallpaper is None:
            raise ValueError("Left or Right wallpaper was not specified correctly and no slideshow dir was provided.")

        else:
            run(args.wallpaper_out, left_wallpaper=args.left_wallpaper,
                right_wallpaper=args.right_wallpaper)

    else:

        if not args.slideshow_duration:
            raise ValueError("A duration must be given for a slideshow.")

        if args.switch_both:

            run(args.wallpaper_out, slideshow=True, slideshow_duration=int(args.slideshow_duration),
                switch_both_monitors=True, slideshow_dir=args.slideshow_dir)

        else:
            run(args.wallpaper_out, slideshow=True, slideshow_duration=int(args.slideshow_duration),
                switch_both_monitors=False, slideshow_dir=args.slideshow_dir)


