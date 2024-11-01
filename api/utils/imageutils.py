import pyqrcode
from PIL import Image, ImageDraw, ImageFont
import base64, base36
from io import BytesIO
from uuid import uuid4

def serialHexaAutoIncrement():
    with open(".autoInc", "r") as f:
        serial = int(f.read())
    with open(".autoInc", "w") as f:
        f.write(str(serial + 1))
        
    alphabase = base36.dumps(serial)
    
    # if contains i or o, recall function
    if any(c in "io" for c in alphabase):
        return serialHexaAutoIncrement()
    return alphabase.upper()  

def genQRCode(data):
    return pyqrcode.create(data)

def getSEQUENTIALQRCode(): 
    ID = serialHexaAutoIncrement()
    return genQRCode(ID), ID

fontpath = f"./api/utils/Roboto-Bold.ttf"
SCL = 12 #HARDCODED SCALE
A4_DIM = (2480, 3508) #HARDCODED A4 DIMENSION RESOLUTION
QRDIM = 348 #HARDCODED QR CODE DIMENSION
PRANGE = (A4_DIM[0] // QRDIM) * (A4_DIM[1] // QRDIM)

def genQRWithID():
    qr, id = getSEQUENTIALQRCode()
    qr = BytesIO(base64.b64decode(qr.png_as_base64_str(scale=SCL)))
    image = Image.open(qr)
    draw = ImageDraw.Draw(image)
    x_delta = image.size[0] // 2 - 110 #HARDCODED HORIZONTAL
    y_delta = image.size[1] - 50 #HARDCODED VERTICAL
    fnt = ImageFont.truetype(fontpath, size=40) #HARDCODED FONT SIZE
    draw.text((x_delta, y_delta), f'I-{id}', font=fnt)
    return image

def generateQRPage():
    page = Image.new("RGB", A4_DIM, (255, 255, 255)) 
    for n in range(PRANGE):
        if n % 2 == 0:
            qrib = genQRWithID()
        posX = (n % (A4_DIM[0] // QRDIM)) * QRDIM
        posY = (n // (A4_DIM[0] // QRDIM)) * QRDIM
        page.paste(qrib, (posX, posY))
            
    return page

def generateQRBook(pages: int = 10):
    filename = f"QR-Book-{uuid4()}.pdf"
    if pages < 1:
        raise ValueError("Pages must be greater than 0")
    pages = [generateQRPage() for _ in range(pages)]
    pages[0].save(filename, save_all=True, append_images=pages[1:], optimize=False)
    return filename
    
    
if __name__ == "__main__":
    print(generateQRBook())
    # print(generateQRBook(5))
    # print(base36.dumps(783641640960))