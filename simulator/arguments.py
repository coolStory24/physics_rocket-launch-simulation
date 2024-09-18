import argparse
import sys
import config
from logger import ConsoleLogger


def configure():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description="Physical rocket simulation",
    )

    parser.add_argument("-v", "--verbose", help="Verbose", action="store_true")
    parser.add_argument("-C", "--hide-markers", help="Disable text markers in start", action="store_true")
    parser.add_argument("-H", "--hide-widgets", help="Disable interface widgets in start", action="store_true")
    parser.add_argument("-f", "--font-path", help="Set path to font .ttf file", )
    parser.add_argument("-s", "--font-size", help="Set font size", )
    parser.add_argument("-m", "--widget-margin", help="Set widget margin", )
    parser.add_argument("-t", "--time_scale", help="Set time scale", )

    args = parser.parse_args()

    config.draw_markers = not args.hide_markers if args.hide_markers is not None else config.draw_markers
    config.draw_widgets = not args.hide_widgets if args.hide_widgets is not None else config.draw_widgets
    config.FONT_PATH = args.font_path if args.font_path is not None else config.FONT_PATH
    config.FONT_SIZE = int(args.font_size) if args.font_size is not None else config.FONT_SIZE
    config.WIDGET_MARGIN = int(args.widget_margin) if args.widget_margin is not None else config.WIDGET_MARGIN
    config.TIME_SCALE = int(args.time_scale) if args.time_scale is not None else config.TIME_SCALE

    if args.verbose:
        console_logger = ConsoleLogger()
