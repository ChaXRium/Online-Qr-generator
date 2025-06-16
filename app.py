from flask import Flask, render_template, request, send_file
import qrcode
from PIL import Image
import io

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["text"]
        logo = request.files.get("logo")

        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        if logo:
            logo_img = Image.open(logo).convert("RGBA")
            img_w, img_h = img.size
            factor = 4
            logo_size = (img_w // factor, img_h // factor)
            logo_img.thumbnail(logo_size)
            pos = ((img_w - logo_img.size[0]) // 2, (img_h - logo_img.size[1]) // 2)
            img.paste(logo_img, pos, logo_img)

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return send_file(buffer, mimetype="image/png")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
