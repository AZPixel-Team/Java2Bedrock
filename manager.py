import zipfile, os

with zipfile.ZipFile("staging/input_pack.zip", "r") as file:
    file.extractall("pack/")
if os.getenv("SOUNDS_CONVERSION") == "true":
    import sound
if os.getenv("ATTACHABLE_MATERIAL") == "entity_emissive_alpha_one_sided" and os.getenv("MEG3_FIX") == "true":
    import meg3
if os.getenv("ARMOR_CONVERSION") == "true":
    import armor
if os.getenv("FONT_CONVERSION") == "true":
    import font