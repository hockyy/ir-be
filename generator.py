from PIL import Image, ImageFont, ImageDraw
import datetime

TITLE_COLOR = "#9f8468"
SUBTITLE_COLOR = "#4a5467"
FONT_PATH = "./assets/genshin.ttf"
BASE_ACHIEVEMENT = "./assets/Proto2id.png"
FONT_SIZE = 75
X = 505
Y = 155
DELTA = 90
ROW_LIMIT = 20
COLUMN_LIMIT = 2
FONT = ImageFont.truetype(FONT_PATH, size=FONT_SIZE)

def init(subtitle: str):
    with Image.open(BASE_ACHIEVEMENT) as im:
        base = ImageDraw.Draw(im)
        subtitle = subtitle.split(' ')
        subtitlePart = []
        for i in subtitle:
            if (subtitlePart == [] or len(subtitlePart[-1]) + len(i) > ROW_LIMIT):
                subtitlePart.append(i)
            else:
                subtitlePart[-1] += f" {i}"

        for idx, val in enumerate(subtitlePart):
            if (idx >= COLUMN_LIMIT): break
            base.text((X, Y + idx * DELTA), val, font=FONT, fill=SUBTITLE_COLOR)
        # im.show()

        basewidth = 500
        wpercent = (basewidth / float(im.size[0]))
        hsize = int((float(im.size[1]) * float(wpercent)))
        im = im.resize((basewidth, hsize), Image.ANTIALIAS)

        filename = f'{datetime.datetime.now()}'
        filename = filename.replace(' ', '-').split(':')
        filename = f'./output/{filename[0]}-{filename[1]}-{filename[2]}.png'
        im.save(f'{filename}', quality=20, optimize=True)

def main():
    init(input())

if __name__ == '__main__':
    main()