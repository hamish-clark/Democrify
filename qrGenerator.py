
import qrcode

PROJECT_DIR = '/home/mishmouse224/democrify'

def generate(filename, data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1db954", back_color="white")
    filename = "{}/static/qrCodes/{}.png".format(PROJECT_DIR, filename)
    img.save(filename)
    return filename
