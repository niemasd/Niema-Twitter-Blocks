#! /usr/bin/env python3
'''
Create a summary of Niema's Twitter blocks
'''
from datetime import datetime
from gzip import open as gopen
from json import loads as jloads
from os.path import isfile
from PIL import Image, ImageFont, ImageDraw
from pytz import timezone
from sys import argv, stderr

# useful constants
IMG_BG = (255, 255, 255) # white
IMG_FONT_PATH = "Pillow/Tests/fonts/FreeMono.ttf"
IMG_FONT_SIZE = 30
IMG_FONT = ImageFont.truetype(IMG_FONT_PATH, IMG_FONT_SIZE)
IMG_WIDTH_PER_SYMBOL = 18
IMG_HEIGHT_PER_LINE = 28
TIMEZONE = timezone('America/Los_Angeles')

# main program
if __name__ == "__main__":
    # load data
    if '-h' in argv or '--help' in argv or len(argv) != 2:
        stderr.write("USAGE: %s block.js.gz\n" % argv[0]); exit(1)
    elif not isfile(argv[1]):
        stderr.write("ERROR: File not found: %s\n" % argv[1]); exit(1)
    elif argv[1].lower().endswith('.gz'):
        data = gopen(argv[1], 'rt').read()
    else:
        data = open(argv[1]).read()
    data = jloads(data.lstrip('window.YTD.block.part0 =').strip())

    # create list of blocked IDs
    blocked_IDs = sorted(int(d['blocking']['accountId']) for d in data)
    f = gopen('blocked_accounts.txt.gz', 'wt', compresslevel=9)
    for ID in blocked_IDs:
        f.write('%s\n' % ID)
    f.close()

    # create summary file
    summary_data = ""
    summary_data += "Summary Generated %s\n\n" % datetime.now(tz=TIMEZONE).strftime("%Y-%m-%d %H:%M:%S %Z")
    summary_data += "- Total Blocked Accounts: %s\n" % '{:,}'.format(len(blocked_IDs))
    f = open('summary.txt', 'w'); f.write(summary_data); f.close()
    img_width = max(len(l) for l in summary_data.splitlines()) * IMG_WIDTH_PER_SYMBOL
    img_height = len(summary_data.strip().splitlines()) * IMG_HEIGHT_PER_LINE
    img = Image.new('RGB', (img_width,img_height), color=IMG_BG)
    fnt = IMG_FONT
    ImageDraw.Draw(img).text((0,0), summary_data.strip(), font=fnt, fill=(0,0,0))
    img.save('summary.png')
