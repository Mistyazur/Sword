import os

from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont, ImageChops
import colorsys

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
    draw = ImageDraw.Draw(img)
    for x in range(1, img.size[0] - 1):
        for y in range(1, img.size[1] - 1):
            rgb = img.getpixel((x, y))
            h, s, v = colorsys.rgb_to_hsv(rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0)
            s = int(s * 100)
            v = int(v * 100)
            if v - s < 45:
                draw.point((x, y), "#000000")


def SortPic():
    paths = [".\\21", ".\\41"]
    for path in paths:
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.find("eh") == -1:
                    print(os.path.join(root, name))
                    img = Image.open(os.path.join(root, name))
                    img = img.convert("RGB")
                    #
                    # # imgf = img.filter(ImageFilter.SHARPEN)
                    # # # imgf = imgf.filter(ImageFilter.FIND_EDGES)
                    # # # imgf = imgf.convert("L")
                    # # # imgf = imgf.point([0 if x < 15 else 1 for x in range(256)], "1")
                    #
                    # enhancer = ImageEnhance.Contrast(img)
                    # # img = enhancer.enhance(2.5)
                    # img = enhancer.enhance(theshord)
                    # # img.save(os.path.join(".\\enhance", name.split(".")[0] + "_eh{0}".format(i) + ".bmp"))
                    # img.save(os.path.join(".\\enhance", "0eh_" + name))

                    # img = img.convert("L")
                    # clearNoise(img, int(path[2:]))
                    # img = ImageChops.invert(img)
                    # img = ImageChops.invert(img)
                    # img = ImageChops.multiply(img, img)
                    # enhancer = ImageEnhance.Contrast(img)
                    # img = enhancer.enhance(1)

                    # mask = Image.open("mask.bmp")
                    # mask = mask.resize((img.size[0], img.size[1]))
                    # img = ImageChops.lighter(img, mask)

                    optimize(img)
                    img.save(os.path.join(path, "0eh_" + name))


if __name__ == "__main__":
    # SortData()
    SortPic()

