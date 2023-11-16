from PIL import Image
import json
import glob
import os
if os.getenv("ATTACHABLE_MATERIAL") == "entity_emissive_alpha_one_sided" and os.getenv("MEG3_FIX") == "true":
    files = glob.glob("staging/target/rp/attachables/modelengine/**/*.json")
    fdone = []
    for file in files:
        if not file in fdone:
            try:
                with open(file, "r") as f:
                    texture_file = json.load(f)["minecraft:attachable"]["description"]["textures"]["default"]
                    texture = f"staging/target/rp/{texture_file}.png"
                im = Image.open(texture)
                im.convert("RGBA")
                A = im.getchannel("A")
                alpha = A.point(lambda i: 51 if i>0 else 0)
                im.putalpha(alpha)
                im.save()
                fdone.append(file)
            except Exception as e:
                print(e)
                print("Error texture:" + texture)