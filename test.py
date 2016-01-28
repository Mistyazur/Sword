from PIL import Image, ImageFilter, ImageWin 
from ctypes import *
import robot

img = Image.open("1.bmp")
img = img.convert("RGB")

# 经过PIL自带filter处理
imgfilted_b = img.filter(ImageFilter.BLUR)
imgfilted_c = img.filter(ImageFilter.CONTOUR)
imgfilted_ee = img.filter(ImageFilter.EDGE_ENHANCE)
imgfilted_ee_m = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
imgfilted_em = img.filter(ImageFilter.EMBOSS)
imgfilted_fe = img.filter(ImageFilter.FIND_EDGES)
imgfilted_sm = img.filter(ImageFilter.SMOOTH)
imgfilted_sm_m = img.filter(ImageFilter.SMOOTH_MORE)
imgfilted_sh = img.filter(ImageFilter.SHARPEN)
imgfilted_d = img.filter(ImageFilter.DETAIL)

# 组合使用filter
group_imgfilted = img.filter(ImageFilter.CONTOUR)
group_imgfilted = group_imgfilted.filter(ImageFilter.SMOOTH_MORE)

group1_imgfilted = img.filter(ImageFilter.SHARPEN)
group1_imgfilted = group1_imgfilted.filter(ImageFilter.FIND_EDGES)
group1_imgfilted = group1_imgfilted.convert("L")
table = [0 if x < 175 else 1 for x in range(256)]
group1_imgfilted.save("11.bmp")

img2 = Image.open("2.bmp")
img2 = img2.convert("RGB")
imgf2 = img2.filter(ImageFilter.SHARPEN)
imgf2 = imgf2.filter(ImageFilter.FIND_EDGES)

imgf2 = imgf2.convert("L")
table = [0 if x < 175 else 1 for x in range(256)]

#  convert to binary image by the table
imgf2 = imgf2.point(table, "1")
imgf2.save("22.bmp")

import datetime
import time
if __name__ == "__main__":
    print(datetime.datetime.now())
    img2 = Image.open("1.bmp")
    img2 = img2.convert("RGB")
    imgf2 = img2.filter(ImageFilter.SHARPEN)
    imgf2 = imgf2.filter(ImageFilter.FIND_EDGES)

    imgf2 = imgf2.convert("L")
    table = [0 if x < 175 else 1 for x in range(256)]

    #  convert to binary image by the table
    imgf2 = imgf2.point(table, "1")
    print(datetime.datetime.now())
    imgf2.save("11.bmp")
    print(datetime.datetime.now())
    # img2 = Image.open("33.bmp")
    # print(type(img2.tobytes()))
    # print(create_string_buffer(11))
    # # s = create_string_buffer('\000' * 32)
    # i = c_int(42)
    # print(i)
    # pi = pointer(i)
    # print(pi)
    # print(byref(i))

    # short_array = (c_ubyte * 4)()
    # print(short_array)
