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
    exit()

def createfolder(glyph):
    os.mkdir("images/{glyph}", exist_ok = True)
    os.mkdir("export/{glyph}", exist_ok = True)

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
    if os.path.isdir(f"export/{glyph}") == False:
        os.mkdir(f"export/{glyph}")
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

listglyphdone = []
    
def converterpack(glyph):
    if os.path.isdir(f"images/{glyph}") == False:
        os.mkdir(f"images/{glyph}")
    if len(symbols) == len(paths):
        maxsw, maxsh = 0, 0
        for symboll, path in zip(symbols, paths):
            symbolbe = ''.join(symboll)
            symbolbehex = (hex(ord(symbolbe)))
            if glyph in listglyphdone:
                return False
            if len(symbolbehex) == 6:
                symbol = symbolbehex[4:]
                symbolac = symbolbehex[2:]
                symbolcheck = symbolac[:2]
            elif len(symbolbehex) == 5:
                symbolbehex = symbolbehex[:2] + "0" + symbolbehex[2:]
                symbol = symbolbehex[4:]
                symbolac = symbolbehex[2:]
                symbolcheck = symbolac[:2]
                glyphs.append(symbolcheck.upper())
            if (symbolcheck.upper()) == (glyph.upper()):
                print(symbolbehex)
                if ":" in path:
                    try:
                        namespace = path.split(":")[0]
                        pathnew = path.split(":")[1]
                        imagefont = Image.open(f"pack/assets/{namespace}/textures/{pathnew}")
                        image = imagefont.copy()
                        image.save(f"images/{glyph}/0x{glyph}{symbol}.png", "PNG")
                    except Exception as e:
                        print(e)
                        continue
                else:
                    try:
                        imagefont = Image.open(f"pack/assets/minecraft/textures/{path}")
                        image = imagefont.copy()
                        image.save(f"images/{glyph}/0x{glyph}{symbol}.png", "PNG")
                    except Exception as e: 
                        print(e)
                        continue
            else:
                continue
        else:                
            files = glob.glob(f"images/{glyph}/*.png")
            for file in files:
                image = Image.open(file)
                sw, sh = image.size
                maxsw, maxsh = max(maxsw, sw), max(maxsh, sh)
            if maxsw == maxsh:
                size = maxsw, maxsw
            elif maxsw > maxsh:
                size = maxsw, maxsw
            elif maxsh > maxsw:
                size = maxsh, maxsh
            if size == (0, 0):
                pass
            else:
                glyphsize = size * 16
                img = Image.open("blank256.png")
                imgre = img.resize(size)
                imgre.save("blankimg.png")
                blankimg = "blankimg.png"
                create_empty(glyph, blankimg) 
                imagetoexport(glyph, blankimg)
                sprite(glyph, glyphsize, size)
                listglyphdone.append(glyph)
            
for glyph in glyphs:
    converterpack(glyph)
