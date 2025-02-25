import qrcode
import qrcode.constants

qr=qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=7,
    border=2
)
qr.add_data(input("Digite la frase a convertir: "))
qr.make(fit=True)

img =qr.make_image(fill_color='black', black_color='white')
img.save('prbQR.png')

#4,Mandarinas,0.2,400