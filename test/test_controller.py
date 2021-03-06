from dumb_switcher import controller as controller
import pytest
import os
import shutil

import unittest
from unittest import mock
import dumb_switcher.VERSION_NUMBER as vn

def test_get_version():
    """
    Test that the correct version string is returned
    :return:
    """
    assert controller.get_version() == str(vn.VERSION_MAJOR) + "." + str(vn.VERSION_MINOR) + "." + \
           str(vn.VERSION_PATCH)


def test_create_wallpaper_file():
    """
    Test that the proper config dirs are created
    :return:
    """

    create_test_dirs()

    script_dir = os.path.dirname(__file__)

    remove_test_files("test_dumbswitcher_dir")

    controller.DUMBSWITCHER_DIR = os.path.join(script_dir, "test_dumbswitcher_dir/dumb_home/")
    controller.WALLPAPER_PATH = os.path.join(controller.DUMBSWITCHER_DIR, "wallpaper.png")

    controller.create_wallpaper_file()

    assert os.path.exists(controller.DUMBSWITCHER_DIR)

    assert os.path.exists(controller.WALLPAPER_PATH)

    remove_test_files("test_dumbswitcher_dir")


def test_create_or_remove_startup_process_for_slideshow():
    """
    Test cases for createing the startup process for the slideshow
    :return:
    """

    create_test_dirs()

    script_dir = os.path.dirname(__file__)

    home_dir = os.path.join(script_dir, "test_home")
    wallpaper_dir = os.path.join(script_dir, "test_images")

    mock_env = mock.patch.dict(os.environ, {"HOME": home_dir})

    # Mock the home directory so we dont mess up the actual home dir
    mock_env.start()

    controller.create_or_remove_startup_process_for_slideshow(wallpaper_dir, 10, False)

    config_dir = os.path.join(home_dir, ".config/autostart/dumbswitcher.desktop")

    assert os.path.exists(config_dir)

    with open(config_dir, 'r') as f:
        contents = f.read()

        expected = "[Desktop Entry]\n" \
                   "Name=dumbswitcher\n" \
                   "Exec=dumb-switcher --slideshow_dir=" + wallpaper_dir + " --slideshow_duration=10 " \
                                                                           "--start_slideshow\n" \
                                                                           "Type=Application\n" \
                                                                           "X-GNOME-Autostart-enabled=true\n"

        assert contents == expected

    remove_test_files("test_home")

    controller.create_or_remove_startup_process_for_slideshow(wallpaper_dir, 10, switch_both=True)

    config_dir = os.path.join(home_dir, ".config/autostart/dumbswitcher.desktop")

    assert os.path.exists(config_dir)

    with open(config_dir, 'r') as f:
        contents = f.read()

        expected = "[Desktop Entry]\n" \
                   "Name=dumbswitcher\n" \
                   "Exec=dumb-switcher --slideshow_dir=" + wallpaper_dir + " --slideshow_duration=10 --start_slideshow " \
                                                                           "--switch_both\n" \
                                                                           "Type=Application\n" \
                                                                           "X-GNOME-Autostart-enabled=true\n"

        assert contents == expected

    remove_test_files("test_home")

    controller.create_or_remove_startup_process_for_slideshow(wallpaper_dir, 10, switch_both=True, remove=True)

    config_dir = os.path.join(home_dir, ".config/autostart/dumbswitcher.desktop")

    assert os.path.exists(config_dir)

    with open(config_dir, 'r') as f:
        contents = f.read()

        expected = "[Desktop Entry]\n" \
                   "Name=dumbswitcher\n" \
                   "Exec=dumb-switcher\n" \
                   "Type=Application\n" \
                   "X-GNOME-Autostart-enabled=false\n"

        assert contents == expected

    remove_test_files("test_home")
    remove_test_files("test_dumbswitcher_dir")

    # end mock
    mock_env.stop()


def remove_test_files(test_dir):
    """
    Helper function to remove generated files for testing
    :return: None
    """

    create_test_dirs()

    script_dir = os.path.dirname(__file__)
    # out_file = os.path.join(script_dir, "test_images/test.png")
    # os.remove(out_file)

    for file in os.listdir(os.path.join(script_dir, test_dir)):

        file_path = os.path.join(script_dir, test_dir, file)

        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else:
            os.remove(file_path)


def create_test_dirs():
    """
    Create test directories
    :return:
    """
    script_dir = os.path.dirname(__file__)

    test_dumbswitcher_dir = os.path.join(script_dir, "test_dumbswitcher_dir")
    test_home = os.path.join(script_dir, "test_home")

    if not os.path.exists(test_dumbswitcher_dir):
        os.makedirs(test_dumbswitcher_dir)

    if not os.path.exists(test_home):
        os.makedirs(test_home)