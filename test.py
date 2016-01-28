from PIL import Image,ImageDraw,ImageFilter
import random,sys



class MyGaussianBlur(ImageFilter.Filter):
    name = "GaussianBlur"
    def __init__(self, radius=2, bounds=None):
        self.radius = radius
        self.bounds = bounds
    def filter(self, image):
        if self.bounds:
            clips = image.crop(self.bounds).gaussian_blur(self.radius)
            image.paste(clips, self.bounds)
            return image
        else:
            return image.gaussian_blur(self.radius)

class Binary(ImageFilter.Filter):

    def __init__(self):
        super(Binary, self).__init__()

    def filter(self, image):
        pixels = image.load()
        for x in ramge(image.width):
          for y in range(image.height):
            pixsels[x, y] = 255 if pixsels[x, y] > 125 else 0
        return image


img = Image.open("1.bmp")

##图像处理##
#转换为RGB图像
img = img.convert("RGB")              

#经过PIL自带filter处理
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

##组合使用filter
group_imgfilted = img.filter(ImageFilter.CONTOUR)
group_imgfilted = group_imgfilted.filter(ImageFilter.SMOOTH_MORE)

##图像保存##
# imgfilted_b.save("1b.bmp")
# imgfilted_c.save("1c.bmp")
imgfilted_ee.save("1ee.bmp")
imgfilted_ee_m.save("1eem.bmp")
# imgfilted_em.save("1em.bmp")
imgfilted_fe.save("1fe.bmp")                                
# imgfilted_sm.save("1sm.bmp")
# imgfilted_sm_m.save("1smm.bmp")
imgfilted_sh.save("1sh.bmp")
# imgfilted_d.save("1d.bmp")
group_imgfilted.save("1group.bmp")


group1_imgfilted = img.filter(ImageFilter.FIND_EDGES)
group1_imgfilted = group1_imgfilted.filter(Binary())
group1_imgfilted.save("2.bmp")
