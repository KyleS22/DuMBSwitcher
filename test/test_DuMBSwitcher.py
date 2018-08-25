from dumb_switcher import DuMBSwitcher as ds
import pytest
import os
from PIL import Image

import unittest
from unittest import mock

TEST_IMAGE_NUM = 0


def test_parse_screen_properties_to_resolution_and_position():
    """
    Test cases for parsing the resolution from xrandr
    :return: None
    """

    # These are valid resolutions
    resolutions = ["1600x900+0+0", "450x250+3+5"]
    expected_result = [{"width": 1600, "height": 900, "x_pos": 0, "y_pos": 0},
                       {"width": 450, "height": 250, "x_pos": 3, "y_pos": 5}]

    result = ds.parse_screen_properties_to_resolution_and_position(resolutions)

    assert expected_result == result

    # These are not valid resolutions
    resolutions = ["HelloxThis+is+notvalid"]

    with pytest.raises(ValueError):
        ds.parse_screen_properties_to_resolution_and_position(resolutions)

    resolutions = ["10500x51512x123x123"]

    with pytest.raises(ValueError):
        ds.parse_screen_properties_to_resolution_and_position(resolutions)

    resolutions = ["123456789"]

    with pytest.raises(ValueError):
        ds.parse_screen_properties_to_resolution_and_position(resolutions)

    resolutions = ["12345x123+2"]

    with pytest.raises(IndexError):
        ds.parse_screen_properties_to_resolution_and_position(resolutions)


def test_create_background_image(tmpdir):
    """
    Test cases for creating a new background image
    :param tmpdir:
    :return:
    """
    script_dir = os.path.dirname(__file__)

    left_image = os.path.join(script_dir, "test_images/Cathédrale_Marie-Rheine-du-Monde_by_Thierry_Pon.jpg")

    right_image = os.path.join(script_dir, "test_images/clock_by_Bernhard_Hanakam.jpg")

    screen_properties = {"screen_space": [3286, 1335], "resolutions": [{"width": 1920, "height": 1080, "x_pos": 0,
                                                                        "y_pos": 0},
                                                                       {"width": 1366, "height": 768, "x_pos": 1920,
                                                                        "y_pos": 567}]}

    out_file = os.path.join(script_dir, "test_images/test.png")

    ds.create_background_image(screen_properties, left_image, right_image, out_file)

    assert os.path.exists(out_file)

    img = Image.open(out_file, 'r')

    assert img.size == (3286, 1335)

    remove_test_images()

    # Switch monitor positions
    screen_properties = {"screen_space": [3286, 1335], "resolutions": [{"width": 1920, "height": 1080, "x_pos": 1920,
                                                                        "y_pos": 0},
                                                                       {"width": 1366, "height": 768, "x_pos": 0,
                                                                        "y_pos": 567}]}

    ds.create_background_image(screen_properties, left_image, right_image, out_file)

    assert os.path.exists(out_file)

    img = Image.open(out_file, 'r')

    assert img.size == (3286, 1335)

    remove_test_images()

    # Three monitors
    screen_properties = {"screen_space": [3286, 1335], "resolutions": [{"width": 1920, "height": 1080, "x_pos": 0,
                                                                        "y_pos": 0},
                                                                       {"width": 1366, "height": 768, "x_pos": 1920,
                                                                        "y_pos": 567},
                                                                       {"width": 1366, "height": 768, "x_pos": 1920,
                                                                        "y_pos": 567}]}
    with pytest.raises(NotImplementedError):
        ds.create_background_image(screen_properties, left_image, right_image, out_file)

    # One monitor
    screen_properties = {"screen_space": [3286, 1335], "resolutions": [{"width": 1920, "height": 1080, "x_pos": 0,
                                                                        "y_pos": 0}]}

    with pytest.raises(NotImplementedError):
        ds.create_background_image(screen_properties, left_image, right_image, out_file)

    # Overlapping monitors
    screen_properties = {"screen_space": [3286, 1335], "resolutions": [{"width": 1920, "height": 1080, "x_pos": 1920,
                                                                        "y_pos": 0},
                                                                       {"width": 1366, "height": 768, "x_pos": 1920,
                                                                        "y_pos": 567}]}

    with pytest.raises(ValueError):
        ds.create_background_image(screen_properties, left_image, right_image, out_file)


def test_choose_next_images():
    """
    Test cases for choosing a random next image
    :return: None
    """

    script_dir = os.path.dirname(__file__)

    slideshow_dir = os.path.join(script_dir, "test_images")

    image1 = None
    image2 = None

    switch_both = False

    image_to_switch = 1

    with pytest.raises(Exception):
        ds.choose_next_images(slideshow_dir, image1, image2, switch_both, image_to_switch)

    create_test_image(0)

    new_image_1, new_image_2 = ds.choose_next_images(slideshow_dir, image1, image2, switch_both, image_to_switch)

    assert new_image_1 is not None
    assert new_image_2 is not None

    new_image_1, new_image_2 = ds.choose_next_images(slideshow_dir, new_image_1, new_image_2, switch_both,
                                                     image_to_switch)

    assert new_image_1 is not None
    assert new_image_2 is not None

    image_to_switch = 2

    new_image_1, new_image_2 = ds.choose_next_images(slideshow_dir, new_image_1, new_image_2, switch_both,
                                                     image_to_switch)

    assert new_image_1 is not None
    assert new_image_2 is not None

    remove_test_images()


def remove_test_images():
    """
    Helper function to remove generated images for testing
    :return: None
    """
    script_dir = os.path.dirname(__file__)
    # out_file = os.path.join(script_dir, "test_images/test.png")
    # os.remove(out_file)

    for image in os.listdir(os.path.join(script_dir, "test_images")):
        image_path = os.path.join(script_dir, "test_images", image)

        if "test" in os.path.split(image_path)[-1]:
            os.remove(image_path)


def create_test_image(image_num):
    """
    Helper function to create images for testing
    :param image_num: A number to uniquely name new images
    :return: None
    """
    script_dir = os.path.dirname(__file__)
    out_path = os.path.join(script_dir, "test_images/test" + str(image_num) + ".png")
    image = Image.new("RGBA", [10, 10], (255, 255, 255, 255))
    image.save(out_path)
