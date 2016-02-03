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
    paths = [".\\sample"]
    for path in paths:
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.find("000_") == -1:
                    print(os.path.join(root, name))
                    img = Image.open(os.path.join(root, name))

                    # Test 1: Fail at 000_2015-12-09_14-22-54
                    # img = ImageOps.posterize(img, 1)

                    # Test 2:
                    img = img.convert("L")
                    img = ImageOps.posterize(img, 1)
                    # img = img.filter(ImageFilter.FIND_EDGES)
                    
                    # img = img.convert("L")


                    # Save
                    img.save(os.path.join(path, "000_" + name))



def SortPic2():
    for c in range(1, 10):
        img = Image.open("test\\s%d.bmp" % c)


        # img2 = img.convert("L")
        # img2 = img2.point([int(round(x*0.5)) for x in range(256)], "L")
        # img2 = img2.point([x if x > 0x2F else 0 for x in range(256)], "L")
        # img2 = ImageOps.posterize(img2, i)
        # img2 = ImageOps.posterize(img2, i)
        # img2 = ImageOps.invert(img2)

        # img2 = img.convert("L")
        # img2 = img2.filter(ImageFilter.FIND_EDGES)
        # img2 = ImageOps.posterize(img2, 1)

        # img2 = img.convert("L")
        # img2 = img2.convert("P", dither=Image.NONE, palette=Image.ADAPTIVE, colors=8)
        # img2 = img2.convert("1")

        # img2 = img.convert("L")
        # img2 = ImageOps.posterize(img2, 3)
        # img2 = img2.filter(ImageFilter.FIND_EDGES)

        # img2 = img.convert("L")
        # img2 = img2.point([x if x > 0x2F else 0 for x in range(256)], "L")
        # img2 = img2.filter(ImageFilter.FIND_EDGES)
        # img2 = ImageOps.posterize(img2, 1)


        
        # img = img.convert("L")
        # img = img.point([x if x > 0x2F else 0 for x in range(256)], "L")
        # ie = ImageEnhance.Sharpness(img)
        # img = ie.enhance(4)
        # ie = ImageEnhance.Contrast(img)
        # img = ie.enhance(0.5)

        # img = ImageOps.posterize(img, 1)

        # img = img.filter(ImageFilter.FIND_EDGES)
        # img = ImageOps.posterize(img, 1)


        source = img.split()
        R, G, B = 0, 1, 2

        # select regions where red is less than 100
        mask = source[G].point(lambda i: i > 150)

        # paste the processed band back, but only where red was < 100
        source[R].paste(source[R], None, mask)

        # select regions where red is less than 100
        mask = source[B].point(lambda i: i > 150)

        # paste the processed band back, but only where red was < 100
        source[R].paste(source[R], None, mask)

        # build a new multiband image
        img = Image.merge(img.mode, source)

        # Save
        img.save("test\\0%d.bmp" % (c))


if __name__ == "__main__":
    # SortData()
    # SortPic()
    SortPic2()
