
import qrcode

<<<<<<< HEAD
PROJECT_DIR = '/home/mishmouse224/democrify'

=======
>>>>>>> d879de03cfa1f199f3015592751264f91f1daaae
def generate(filename, data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1db954", back_color="white")
<<<<<<< HEAD
    filename = "{}/static/qrCodes/{}.png".format(PROJECT_DIR, filename)
=======
    filename = "static/qrCodes/{}.png".format(filename)
>>>>>>> d879de03cfa1f199f3015592751264f91f1daaae
    img.save(filename)
    return filename
