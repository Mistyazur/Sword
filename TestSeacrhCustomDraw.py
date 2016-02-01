from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
import robot
import time

def test_draw_pic():
    img = Image.new('RGB', (100, 100), "#152e4b")

    font = ImageFont.truetype('FZLTCXHJW.TTF', 13)
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), "觞", font=font)
    # img = img.convert("L")
    # img = img.point([0 if x < 1 else 1 for x in range(256)], "1")
    # img = img.convert("RGB")
    img = img.resize((85, 85), Image.ANTIALIAS)
    img.save("test.bmp")
    # img.show()

# def search():
#     rt = robot.Robot(True)
#     rt.reg("FateCynff62bb4a6ec42e04e68567c3e009ec88", "Sword")
#     print(rt.bind(1704632, "normal", "normal", "normal", 0))
#     rt.setPath("test")
#     for i in range(1, 11):
#         sim = i/10
#         print(sim)
#         print(rt.findPic(0, 0, 1920, 1040, "test.bmp", "444444", sim, 0))
#     rt.unbind()
#     rt.beep()

if __name__ == "__main__":
    # SortData()
    SortPic()

    # time.sleep(2)
    # test_draw_pic()
    # time.sleep(1)
    # search()