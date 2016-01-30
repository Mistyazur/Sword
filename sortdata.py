import os

from PIL import Image, ImageFilter, ImageEnhance


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


def SortPic():
    for root, dirs, files in os.walk(".\\enhance"):
        for name in files:
            if name.find("eh") == -1:
                print(os.path.join(root, name))
                img = Image.open(os.path.join(root, name))
                img = img.convert("RGB")

                # imgf = img.filter(ImageFilter.SHARPEN)
                # # imgf = imgf.filter(ImageFilter.FIND_EDGES)
                # # imgf = imgf.convert("L")
                # # imgf = imgf.point([0 if x < 15 else 1 for x in range(256)], "1")

                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(2.5)
                # img.save(os.path.join(".\\enhance", name.split(".")[0] + "_eh{0}".format(i) + ".bmp"))
                img.save(os.path.join(".\\enhance", "0eh_" + name))

if __name__ == "__main__":
    # SortData()
    SortPic()

