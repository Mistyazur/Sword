from PIL import Image, ImageFilter
from ctypes import *
from io import BytesIO
import time
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


if __name__ == "__main__":
    # print(datetime.datetime.now())
    # img2 = Image.open("1.bmp")
    # img2 = img2.convert("RGB")
    # imgf2 = img2.filter(ImageFilter.SHARPEN)
    # imgf2 = imgf2.filter(ImageFilter.FIND_EDGES)

    # imgf2 = imgf2.convert("L")
    # table = [0 if x < 175 else 1 for x in range(256)]

    # #  convert to binary image by the table
    # imgf2 = imgf2.point(table, "1")
    # print(datetime.datetime.now())
    # imgf2.save("11.bmp")
    # print(datetime.datetime.now())

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

    time.sleep(1)
    rt = robot.Robot(True)
    rt.reg("FateCynff62bb4a6ec42e04e68567c3e009ec88", "Sword")
    print(rt.bind(66586, "normal", "normal", "normal", 0))
    res = rt.getScreenBmp(0, 0, 30, 30)
    print(res)
    s = string_at(res[1], res[2])
    b = BytesIO(s)
    im = Image.open(b)
    im = im.convert("1")
    im = im.convert("RGB")

    ofile = BytesIO()
    im.save(ofile, 'BMP')
    converted_data = ofile.getvalue()
    buf = create_string_buffer(converted_data)

    mode = "mem:%d,%d" % (addressof(buf), sizeof(buf))
    print(mode)
    print(rt.setDisplayInput(mode))
    print(rt.getColor(7, 1))
    print(rt.getColor(7, 2))

    # print(ss)
    # print(addressof(ss))
    # sss = string_at(ss)
    # im2 = Image.open(BytesIO(sss))
    # im2.show()