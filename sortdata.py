import os

from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont, ImageChops, ImageOps
import colorsys
import datetime

def SortWordText():
    with open("Question.txt", "r") as rf, open("Q.txt", "w") as wf:
        preWord = ""
        for line in rf.readlines():
            word = line[line.find("$") + 1]
            if word != preWord:
                wf.write(line)
                preWord = word
            else:
                print(word)


def clear(image, x, y):
    rgb = image.getpixel((x, y))
    # print(rgb)
    # print(colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2]))
    # print(colorsys.rgb_to_hsv(127/255.0, 133/255.0, 141/255.0))
    h, s, v = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
    # theshord = 50
    # count = 0
    # if L + theshord < image.getpixel((x - 1, y)):
    #     count += 1
    # if L + theshord < image.getpixel((x, y - 1)):
    #     count += 1
    # if L + theshord < image.getpixel((x, y + 1)):
    #     count += 1
    # if L + theshord < image.getpixel((x + 1, y)):
    #     count += 1
    # if L + theshord < image.getpixel((x - 1, y - 1)):
    #     count += 1
    # if L + theshord < image.getpixel((x - 1, y + 1)):
    #     count += 1
    # if L + theshord < image.getpixel((x + 1, y - 1)):
    #     count += 1
    # if L + theshord < image.getpixel((x + 1, y + 1)):
    #     count += 1
    #
    # if count > 4:
    #     return True

    return False


def clearNoise(img):
    draw = ImageDraw.Draw(img)
    for x in range(1, img.size[0] - 1):
        for y in range(1, img.size[1] - 1):
            res = clear(img, x, y)
            if res:
                draw.point((x, y), 0)


def optimize(img):
    # precount = 0
    # for i in range(100):
    #     count = 0

    for x in range(1, img.size[0] - 1):
        for y in range(1, img.size[1] - 1):
            rgb = img.getpixel((x, y))
            h, s, v = colorsys.rgb_to_hsv(rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0)
            s = int(round(s * 100))
            v = int(round(v * 100))
            # if v - s > i:
            #     count += 1

            if v - s >= 55:
                img.putpixel((x, y), (255, 255, 255))
        # print((i, count, count - precount))
        # precount = count


def SortPic():
    paths = [".\\21", ".\\41", ".\\100PW"]
    for path in paths:
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.find("eh") == -1:
                    print(os.path.join(root, name))
                    img = Image.open(os.path.join(root, name))
                    img = img.convert("RGB")

                    # # Method 1
                    img = img.convert("L")
                    enhancer = ImageEnhance.Contrast(img)
                    img = enhancer.enhance(0.75)
                    img = img.filter(ImageFilter.FIND_EDGES)
                    img = ImageChops.invert(img)
                    img = ImageOps.posterize(img, 1)

                    # Method 2
                    # img = img.convert("L")
                    # img = ImageChops.invert(img)
                    # enhancer = ImageEnhance.Contrast(img)
                    # img = enhancer.enhance(0.75)
                    # # enhancer = ImageEnhance.Sharpness(img)
                    # # img = enhancer.enhance(2)
                    # img = ImageOps.posterize(img, 1)

                    # Save
                    img.save(os.path.join(path, "0eh_" + name))


if __name__ == "__main__":
    # SortData()
    SortPic()

