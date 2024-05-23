import segno
from PIL import Image, ImageFont, ImageDraw
import io
import flask

from packages.log import logger


def generate(dorm_name, dorm_code):
    qrcode = segno.make(f"https://dormhub.space/register/{dorm_code}/", error="H")
    qrcode.save(
        dorm_code + ".png",
        scale=15,
        border=10,
    )

    qr = Image.open(dorm_code + ".png")
    width, height = qr.size
    font_path = "/app/LiberationSans-Regular.ttf"
    font1 = ImageFont.truetype(font_path, height * 0.03)
    font2 = ImageFont.truetype(font_path, height * 0.052)
    font3 = ImageFont.truetype(font_path, height * 0.03)

    draw = ImageDraw.Draw(qr)
    w_qr = draw.textlength(dorm_name, font=font1)
    wScan = draw.textlength("Scan me to join this Dorm's group", font=font2)
    wCode = draw.textlength("DormCode: " + dorm_code, font=font3)

    draw.text(((width - w_qr) / 2, height * 0.05), dorm_name, fill="black", font=font1)
    draw.text(
        ((width - wScan) / 2, height * 0.10),
        "Scan me to join this Dorm's group",
        fill="black",
        font=font2,
    )
    draw.text(
        ((width - wCode) / 2, height * 0.84), "Dorm code: " + dorm_code, fill="black", font=font3
    )

    img_width, img_height = qr.size
    qr = qr.convert("RGB")

    logo_max_size = height * 0.23
    logo_img = Image.open("/app/static/logo.png")
    logo_img.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)
    box = ((img_width - logo_img.size[0]) // 2, (img_height - logo_img.size[1]) // 2)
    qr.paste(logo_img, box)
    qr.save(f"{dorm_code}.png")
    return qr


def download(dorm_name, dorm_code, filename='QrCode.png'):
    qr = generate(dorm_name, dorm_code)
    img_io = io.BytesIO()

    qr.save(img_io, 'PNG')
    img_io.seek(0)

    return flask.send_file(
        img_io,
        mimetype='image/png',
        as_attachment=True,
        download_name=filename
    )
