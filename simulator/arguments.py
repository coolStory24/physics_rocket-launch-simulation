import argparse
import sys
import config
from logger import ConsoleLogger


def configure():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description="Physical rocket simulation",
    )

    parser.add_argument("-v", "--verbose", help="Verbose", action=argparse.BooleanOptionalAction)
    parser.add_argument("-m", "--show-markers", help="Disable text markers in start", action=argparse.BooleanOptionalAction)
    parser.add_argument("-w", "--show-widgets", help="Disable interface widgets in start", action=argparse.BooleanOptionalAction)
    parser.add_argument("-f", "--font-path", help="Set path to font .ttf file")
    parser.add_argument("-s", "--font-size", help="Set font size")
    parser.add_argument("--widget-margin", help="Set widget margin")
    parser.add_argument("-t", "--time_scale", help="Set time scale")

    args = parser.parse_args()

    config.draw_markers = args.show_markers if args.show_markers is not None else config.draw_markers
    config.draw_widgets = args.show_widgets if args.show_widgets is not None else config.draw_widgets
    config.VERBOSE = args.verbose if args.verbose is not None else config.VERBOSE
    config.FONT_PATH = args.font_path if args.font_path is not None else config.FONT_PATH
    config.FONT_SIZE = int(args.font_size) if args.font_size is not None else config.FONT_SIZE
    config.WIDGET_MARGIN = int(args.widget_margin) if args.widget_margin is not None else config.WIDGET_MARGIN
    config.TIME_SCALE = int(args.time_scale) if args.time_scale is not None else config.TIME_SCALE
