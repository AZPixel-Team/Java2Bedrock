from PIL import Image
import json
import glob
import os
files = glob.glob("staging/target/rp/attachables/modelengine/**/*.json")
texture_done = []
for file in files:
    try:
        with open(file, "r") as f:
            data = json.load(f)
            texture_file = data["minecraft:attachable"]["description"]["textures"]["default"]
            texture = f"staging/target/rp/{texture_file}.png"
        if not os.getenv("ATTACHABLE_MATERIAL") == "entity_emissive_alpha_one_sided":
            with open(file, "w") as f:
                data["minecraft:attachable"]["description"]["materials"]["default"] = "entity_emissive_alpha_one_sided"
                data["minecraft:attachable"]["description"]["materials"]["enchanted"] = "entity_emissive_alpha_one_sided"
                json.dump(data, f)
        if texture_file in texture_done: continue
        im = Image.open(texture).convert("RGBA")
        im.putalpha(51)
        pixels = im.load()
        for x in range(im.width):
            for y in range(im.height):
                if pixels[x,y] == (0,0,0,51):
                    pixels[x,y] = (0,0,0,0)
        im.save(texture)
        texture_done.append(texture_file)
    except Exception as e:
        print(e)
        print("Error texture:" + texture)
print(texture_done)
