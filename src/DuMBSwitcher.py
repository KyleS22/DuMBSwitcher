import argparse
from PIL import Image


# TODO: Allow slideshow


def create_background_image(primary_monitor_dimensions, secondary_monitor_dimensions, y_displacement, image_1, image_2, out_file):


    # TODO: This does not account for if the prImary monitor is on the right
    img1 = Image.open(image_1, 'r')
    img2 = Image.open(image_2, 'r')

    # Scale the images to fit the monitors
    basewidth_img1 = primary_monitor_dimensions[0]

    wpercent_img1 = (basewidth_img1/float((img1.size[0])))
    hsize_img1 = int((float(img1.size[1]) * float(wpercent_img1)))

    img1 = img1.resize((basewidth_img1, hsize_img1), Image.ANTIALIAS)

    basewidth_img2 = secondary_monitor_dimensions[0]

    wpercent_img2 = (basewidth_img2 / float((img2.size[0])))
    hsize_img2 = int((float(img2.size[1]) * float(wpercent_img2)))

    img2 = img2.resize((basewidth_img2, hsize_img2), Image.ANTIALIAS)

    if primary_monitor_dimensions[1] > secondary_monitor_dimensions[1]:
        total_height = primary_monitor_dimensions[1] - y_displacement
    else:
        total_height = secondary_monitor_dimensions[1] - y_displacement

    total_dimensions = (primary_monitor_dimensions[0] + secondary_monitor_dimensions[0], total_height)

    background = Image.new('RGBA', total_dimensions, (255, 255, 255, 255))

    background.paste(img1, (0,0))

    img2_y_pos = (img1.size[1] - img2.size[1]) - y_displacement

    background.paste(img2, (primary_monitor_dimensions[0], img2_y_pos))

    background.save(out_file)


def run(left_monitor_height, left_monitor_width, right_monitor_height, right_monitor_width, primary_monitor,
        y_displacement, wallpaper_out, left_wallpaper=None, right_wallpaper=None, slideshow_dir=None):


    create_background_image((int(left_monitor_width), int(left_monitor_height)), (int(right_monitor_width), int(right_monitor_height)),
                            int(y_displacement), left_wallpaper,
                            right_wallpaper, wallpaper_out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a spanned wallpaper out of two images to fit on two monitors.")

    parser.add_argument("left_monitor_width", help="The width of the monitor on the left.")
    parser.add_argument("left_monitor_height", help="The height of the monitor on the left.")
    parser.add_argument("right_monitor_width", help="The width of the monitor on the right")
    parser.add_argument("right_monitor_height", help="The height of the monitor on the right")
    parser.add_argument("primary_monitor", help="The monitor used to measure the vertical displacement of the secondary"
                                                " monitor. Values must be 'Left' or 'Right'")
    parser.add_argument("y_displacement", help="The vertical displacement of the secondary monitor, measured from the"
                                               " bottom of the primary monitor to the bottom of the secondary."
                                               "  Negative values denote that the secondary monitor is below the"
                                               " primary monitor")
    parser.add_argument("wallpaper_out", help="The path to store the resulting wallpaper at")
    parser.add_argument("--left_wallpaper", help="The wallpaper to display on the left monitor")
    parser.add_argument("--right_wallpaper", help="The wallpaper to display on the right monitor")
    parser.add_argument("--slideshow_dir", help="The directory to get wallpapers from for a slideshow")


    args = parser.parse_args()

    if args.slideshow_dir is None:
        if args.left_wallpaper is None or args.right_wallpaper is None:
            raise ValueError("Left or Right wallpaper was not specified correctly and no slideshow dir was provided.")

        else:

            run(args.left_monitor_height, args.left_monitor_width, args.right_monitor_height, args.right_monitor_width,
                args.primary_monitor, args.y_displacement, args.wallpaper_out, left_wallpaper=args.left_wallpaper,
                right_wallpaper=args.right_wallpaper)

    else:
        run(args.left_monitor_height, args.left_monitor_width, args.right_monitor_height, args.right_monitor_width,
            args.primary_monitor, args.y_displacement, args.wallpaper_out, slideshow_dir=args.slideshow_dir)


