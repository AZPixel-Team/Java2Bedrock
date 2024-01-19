import zipfile, os

with zipfile.ZipFile("staging/input_pack.zip", "r") as file:
    file.extractall("pack/")

try: 
    if os.getenv("SOUNDS_CONVERSION") == "true": import sound
except Exception as e: print(e)
try:
    if os.getenv("MEG3_FIX") == "true": import meg3
except Exception as e: print(e)
try:
    if os.getenv("ARMOR_CONVERSION") == "true": import armor
except Exception as e: print(e)
try:
    if os.getenv("FONT_CONVERSION") == "true": import font
except Exception as e: print(e)
try:
    if os.getenv("BOW_CONVERSION") == "true": import bow
except Exception as e: print(e)
try:
    if os.getenv("SHIELD_CONVERSION") == "true": import shield
except Exception as e: print(e)
try:
    if os.getenv("BLOCK_CONVERSION") == "true": import blocks
except Exception as e: print(e)
