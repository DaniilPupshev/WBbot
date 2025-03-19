from PIL import Image, ImageFont, ImageDraw
import random

from DATA_BASE import db
from LOGIC import config

db_process = db.options_db()

img = "API_WB/image/"
images = ["2.png", "3.png", "4.png", "5.png"]

def edit_qr_conde_image(chat_id, tmp_text, text_msg):
    text = tmp_text.split(' ', maxsplit=2)

    name_delivery = text[0]
    name_sum = text[1]

    if len(text) == 2 and len(name_delivery) >= 8 and name_delivery.isdigit() == True and name_sum.isdigit() == True:
        qr_code = Image.open(img+random.choice(images))
        fontbold = ImageFont.truetype("API_WB/Fonts/arial_bolditalicmt.ttf", size=89.12)
        font_arial = ImageFont.truetype("API_WB/Fonts/arialmt.ttf", size=96.58)
        draw_text = ImageDraw.Draw(qr_code)
        draw_text.text((32,86-96.58/2), "WB-GI-"+name_delivery, font= fontbold, fill=("#000000"))
        draw_text.text((34,172+705+25), f"{name_sum} шт.", font= font_arial, fill=("#000000"))
        draw_text.text((32,172+705+130), "Москва_Восток", font= font_arial, fill=("#000000"))
        tmp = "temp_" + str(chat_id) + ".pdf"

        path = f"API_WB/image/temp_qr_code/{tmp}"
        qr_code.rotate(90, expand=True).save(f"{path}")
        return text_msg[0], path
    return text_msg[1], ''