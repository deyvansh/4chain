import qrcode
import png

#s = "heylo"
#url = pyqrcode.create(s)
#url.png(aloo.png)

def gen_qr(cid, output_path):
    qr_url = f"http:localhost:5000/verify/{cid}"
    qr = qrcode.QRCode()
    qr.add_data(qr_url)
    qr.make(fit=True)
    img = qr.make_image()
    img.save(output_path)

