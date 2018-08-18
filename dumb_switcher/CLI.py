"""
Provides a command line interface to the DuMBSwitcher
"""

import dumb_switcher.controller as controller
from dumb_switcher.controller import WALLPAPER_PATH
import argparse
import sys
import dumb_switcher.DuMBSwitcher as ds


def main():
    """
    Parse command line arguments and call the associated controller functions.
    :return:
    """
    parser = argparse.ArgumentParser(description="Create a spanned wallpaper out of two images to fit on two monitors.")

    parser.add_argument("--left_wallpaper", help="The wallpaper to display on the left monitor")
    parser.add_argument("--right_wallpaper", help="The wallpaper to display on the right monitor")
    parser.add_argument("--slideshow_dir", help="The directory to get wallpapers from for a slideshow")
    parser.add_argument("--switch_both", action="store_true", help="Switch both monitors at the same time")
    parser.add_argument("--slideshow_duration", help="The amount of time before switching a wallpaper.")
    parser.add_argument("--enable_lock_screen", action="store_true",
                        help="Show the current wallpaper on the lock screen as well.")
    parser.add_argument("--stop_slideshow", action="store_true", help="Stop playing the slideshow on startup.")
    parser.add_argument("--start_slideshow", action="store_true",
                        help="Start the slideshow that is currently set to play.")

    args = parser.parse_args()

    # Display help if there are not enough arguments
    if len(sys.argv) == 1:
        parser.print_help()

    # If the left and right wallpaper are specified, create the new wallpaper and set it
    if args.left_wallpaper and args.right_wallpaper:
        controller.set_wallpaper_once(args.left_wallpaper, args.right_wallpaper)

    # If the user wants the image on their lock screen, set the lock screen
    if args.enable_lock_screen:
        controller.set_lock_screen()

    # If the user wants to stop the slideshow, remove it from the startup programs
    if args.stop_slideshow:
        controller.create_or_remove_startup_process_for_slideshow(None, 0, False, remove=True)

    switch_both = False

    if args.switch_both:
        switch_both = True

    # If a slideshow directory was provided, set up a slideshow
    if args.slideshow_dir:

        if args.slideshow_duration:
            controller.create_or_remove_startup_process_for_slideshow(args.slideshow_dir, args.slideshow_duration,
                                                                      switch_both)
    # If the user wants to start the slideshow, start it
    if args.start_slideshow:
        
        if not args.slideshow_dir or not args.slideshow_duration:
            print("Error: You must specify a slideshow directory and duration")
        else:

            ds.run(WALLPAPER_PATH, slideshow=True, slideshow_duration=args.slideshow_duration,
                   switch_both_monitors=switch_both, slideshow_dir=args.slideshow_dir)


if __name__ == "__main__":
    main()