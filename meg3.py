from PIL import Image
import json
import glob
import os
if os.getenv("ATTACHABLE_MATERIAL") == "entity_emissive_alpha_one_sided" and os.getenv("MEG3_FIX") == "true":
    files = glob.glob("staging/target/rp/attachables/modelengine/**/*.json")
    for file in files:
        try:
            with open(file, "r") as f:
                texture_file = json.load(f)["minecraft:attachable"]["description"]["textures"]["default"]
                texture = f"staging/target/rp/{texture_file}"
            im = Image.open(texture)
            im = im.convert('RGBA')
            sx, sy = im.size
            im.putalpha(51)
            imd = im.load()
            for x in range(sx):
                for y in range(sy):
                    if imd[x,y] == (0, 0, 0, 51):
                        imd[x,y] = 0,0,0,0
            im.save(texture)
        except Exception as e:
            print(e)
            print("Error texture:" + texture)