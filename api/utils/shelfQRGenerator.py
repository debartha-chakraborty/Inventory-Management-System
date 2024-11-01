import pyqrcode
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO
from uuid import uuid4


ZONES = 4
STACKS = 16
LEVELS = 5

#dataformat = 'ZONECODE-STACKNUM-LEVELCODE' i.e. 'A-08-B', 'B-12-C', 'D-03-A'
index = -1
def autoIncrement():
    global index
    index += 1
    return index

def formatData(zone, stack=None, level=None):
    '''
    Input: (0, 7, 2), (1, 11, 3), (3, 2, 1)
    Output: 'A008B', 'B012C', 'D003A'
    '''
    ## TODO: REWRITE THIS FUNCTION
    zonemap = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
    levelmap = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}
    id = f'{zonemap[zone]}{str(stack+1).zfill(3)}{levelmap[level]}'
    return id

def IDtoFormat(ID):
    '''
    Input: 37, 138, 251
    Output: (1, 8, 2), (2, 12, 3), (4, 3, 1)
    '''
    zoneVal = STACKS * LEVELS
    stackVal = LEVELS
    zone = ID // zoneVal
    stack = (ID % zoneVal) // stackVal 
    level = (ID % zoneVal) % stackVal 
    return zone, stack, level
    

def genQRCode(data):
    return pyqrcode.create(data)

def getSEQUENTIALQRCode(): 
    ID = formatData(*IDtoFormat(autoIncrement()))
    return genQRCode(ID), ID

fontpath = f"./api/utils/Roboto-Bold.ttf"
SCL = 30 #HARDCODED SCALE
A4_DIM = (2480, 3508) #HARDCODED A4 DIMENSION RESOLUTION
QRDIM = 870 #HARDCODED QR CODE DIMENSION
PRANGEX = A4_DIM[0] // (QRDIM - 80) #REDUCED BY 80
PRANGEY = A4_DIM[1] // QRDIM


def genQRWithID():
    qr, id = getSEQUENTIALQRCode()
    qr = BytesIO(base64.b64decode(qr.png_as_base64_str(scale=SCL)))
    image = Image.open(qr)
    draw = ImageDraw.Draw(image)
    x_delta = image.size[0] // 2 - 80 #HARDCODED HORIZONTAL
    y_delta = image.size[1] - 50 #HARDCODED VERTICAL
    fnt = ImageFont.truetype(fontpath, size=40) #HARDCODED FONT SIZE
    draw.text((x_delta, y_delta), f'S-{id}', font=fnt)
    return image

def generateQRPage(_):
    page = Image.new("RGB", A4_DIM, (255, 255, 255))
    for y in range(PRANGEY):
        posY = (y % (A4_DIM[1] // QRDIM)) * QRDIM
        for x in range(PRANGEX):
            if (y + x) % 2 == 0:
                qrib = genQRWithID()
            posX = (x % (A4_DIM[0] // (QRDIM - 100))) * (QRDIM - 80)
            page.paste(qrib, (posX, posY))      
    print(f"Generated QR Page {_+1}")      
    return page

def generateQRBook(pages: int = 10):
    try:
        filename = f"Shelf-QR-Book-{str(uuid4())[:8]}.pdf"
        if pages < 1:
            raise ValueError("Pages must be greater than 0")
        pages = [generateQRPage(_) for _ in range(pages)]
        pages[0].save(filename, save_all=True, append_images=pages[1:], optimize=False)
        print(f"Generated QR Book: {filename}")
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":
    # qr = genQRWithID()
    # qr = generateQRPage()
    # qr.show()
    generateQRBook(10)
    pass