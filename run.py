from PIL import Image
from sprite import sprite
from io import BytesIO
from zipfile import ZipFile
import glob, os, math, shutil, json, requests, sys

lines = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "a", "b", "c", "d", "e", "f"]

def downloadpack(url):
    req = requests.get(url)
    zipfile = ZipFile(BytesIO(req.content))
    zipfile.extractall('pack/')

downloadpack(os.environ.get("PACK_URL"))
try:
    with open("pack/assets/minecraft/font/default.json", "r") as f:
        data = json.load(f)
        symbols = [d['chars'] for d in data['providers']]
        paths = [d['file'] for d in data['providers']]
except:
    sys.exit("No Have Font")

def createfoler():
    if not os.path.exists(f"images/{glyph}"):
        os.makedirs(f"images/{glyph}")
    if not os.path.exists(f"export/{glyph}"):
        os.makedirs(f"export/{glyph}")
    
def create_empty(glyph, blankimg):
    for line in lines:
        for linee in lines:
            if linee != lines:
                name = f"{line}{linee}"
                if os.path.isfile(f"images/{glyph}/0x{glyph}{name}.png"):
                    continue
                else:
                    imagesus = Image.open(blankimg)
                    image = imagesus.copy()
                    image.save(f"images/{glyph}/0x{glyph}{name}.png", "PNG")
    for line in lines:
        name = f"{line}{line}"
        if os.path.isfile(f"images/{glyph}/0x{glyph}{name}.png"):
            continue
        else:
            imagesus = Image.open(blankimg)
            image = imagesus.copy()
            image.save(f"images/{glyph}/0x{glyph}{name}.png", "PNG")

def imagetoexport(glyph, blankimg):
    filelist = [file for file in os.listdir(f'images/{glyph}') if file.endswith('.png')]
    for img in filelist:
        image = Image.open(blankimg)
        logo = Image.open(f'images/{glyph}/{img}')
        image_copy = image.copy()
        position = (0, 0)
        image_copy.paste(logo, position)
        image_copy.save(f"export/{glyph}/{img}")
            
glyphs = []
for i in symbols:
    if i not in glyphs:
        symbolbe = ''.join(i)
        sbh = (hex(ord(symbolbe)))
        a = sbh[2:]
        ab = a[:2]
        glyphs.append(ab.upper())
glyphs = list(dict.fromkeys(glyphs))
print(glyphs)

def converterpack(glyph):
    if len(symbols) == len(paths):
        maxsw, maxsh = 0, 0
        for symboll, path in zip(symbols, paths):
            symbolbe = ''.join(symboll)
            symbolbehex = (hex(ord(symbolbe)))
            symbol = symbolbehex[4:]
            symbolac = symbolbehex[2:]
            symbolcheck = symbolac[:2]
            if (symbolcheck.upper()) == (glyph.upper()):
                if ":" in path:
                    try:
                        namespace = path.split(":")[0]
                        pathnew = path.split(":")[1]
                        imagefont = Image.open(f"pack/assets/{namespace}/textures/{pathnew}")
                        image = imagefont.copy()
                        #os.remove(f"images/{glyph}/0x{glyph}{symbol}.png")
                        image.save(f"images/{glyph}/0x{glyph}{symbol}.png", "PNG")
                        sw, sh = imagefont.size
                        maxsw, maxsh = max(maxsw, sw), max(maxsh, sh)
                    except Exception as e:
                        print(e)
                        pass
                else:
                    try:
                        imagefont = Image.open(f"pack/assets/minecraft/textures/{path}")
                        image = imagefont.copy()
                        #os.remove(f"images/{glyph}/0x{glyph}{symbol}.png")
                        image.save(f"images/{glyph}/0x{glyph}{symbol}.png", "PNG")
                        sw, sh = imagefont.size
                        maxsw, maxsh = max(maxsw, sw), max(maxsh, sh)
                    except Exception as e: 
                        print(e)
                        pass
            else:
                continue
        else:
            if maxsw == maxsh:
                size = maxsw, maxsh
            elif maxsw > maxsh:
                size = maxsw, maxsw
            elif maxsh > maxsw:
                size = maxsh, maxsh
            glyphsize = size * 16
            img = Image.open("blank256.png")
            imgre = img.resize(size)
            imgre.save("blankimg.png")
            blankimg = "blankimg.png"
            create_empty(glyph, blankimg) 
            imagetoexport(glyph, blankimg)
            sprite(glyph, glyphsize, size)
            
for glyph in glyphs:
    converterpack(glyph)
