import os
import json
import glob
from bow_util import Bow_Util

if os.path.exists("pack/assets/minecraft/models/item/bow.json"):
    with open("pack/assets/minecraft/models/item/bow.json") as f:
        data = json.load(f)
        predicate = [d["predicate"] for d in data["overrides"]]
        model = [d["model"] for d in data["overrides"]]
    for m, p in zip(model, predicate):
        if m in ["item/bow", "item/bow_pulling_0", "item/bow_pulling_1", "item/bow_pulling_2"]:
            continue
        i = 0
        try:
            if p["pulling"] == 1:
                i = 1
                if p["pull"] <= 0.65:
                    i = 2
                elif p["pull"] > 0.65:
                    i = 3
        except:
            pass
        fpath = (f"cache/{p['custom_model_data']}.json")
        if not os.path.exists(fpath):
            os.makedirs(os.path.dirname(fpath), exist_ok=True)
            with open(fpath, "w") as f:
                f.write("{}")
        with open(fpath, "r") as f:
            data = json.load(f)
        with open(fpath, "w") as f:
            if "check" in data:
                data["check"] = data["check"] + 1
            else:
                data["check"] = 1
            data[f'texture_{i}'] = m
            json.dump(data, f, indent=2)

files = glob.glob("cache/*.json")
Bow_Util.rendercontrollers()
gmdllist = []
for file in files:
    try:
        with open(file, "r") as f:
            data = json.load(f)
        if data["check"] == 4:
            textures = []
            geometry = []
            for i in range(4):
                namespace = data[f"texture_{i}"].split(":")[0]
                path = data[f"texture_{i}"].split(":")[1]
                files = glob.glob(f"staging/target/rp/attachables/{namespace}/{path}*.json")
                for fa in files:
                    if f"{path.split('/')[-1]}." in fa:
                        break
                with open(fa, "r") as f:
                    dataA = json.load(f)
                    f.close()
                    textures.append(dataA["minecraft:attachable"]["description"]["textures"]["default"])
                    geometry.append(dataA["minecraft:attachable"]["description"]["geometry"]["default"])
                    la = len(path)
                    lb = len(path.split("/")[-1])
                    l = path[:la-lb]
                    apath = l + "animation." + path.split('/')[-1]
                    if i == 0:
                        files = glob.glob(f"staging/target/rp/animations/{namespace}/{apath}.json")
                        for fan in files:
                            if f"{path.split('/')[-1]}.json" in fan:
                                animationfile = fan
                                break
                        mfile = fa
                        mdefault = dataA["minecraft:attachable"]["description"]["materials"]["default"]
                        menchanted = dataA["minecraft:attachable"]["description"]["materials"]["enchanted"]
                        gmdl = dataA["minecraft:attachable"]["description"]["identifier"].split(":")[1]
                        gmdllist.append(f"geyser_custom:{gmdl}")
                    else:
                        files = glob.glob(f"staging/target/rp/animations/{namespace}/{apath}.json")
                        for fan in files:
                            if f"{path.split('/')[-1]}.json" in fan:
                                os.remove(fan)
                                break
                        os.remove(fa)
            Bow_Util.item_texture(gmdl, textures[0])
            Bow_Util.animations(animationfile)
            Bow_Util.write(mfile, gmdl, textures, geometry, mdefault, menchanted)
    except Exception as e:
        print(e)
Bow_Util.acontroller(gmdllist)