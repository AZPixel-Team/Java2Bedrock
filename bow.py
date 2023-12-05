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
Bow_Util.animation()
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
                    if i == 0:
                        mfile = fa
                        mdefault = dataA["minecraft:attachable"]["description"]["materials"]["default"]
                        menchanted = dataA["minecraft:attachable"]["description"]["materials"]["enchanted"]
                        gmdl = dataA["minecraft:attachable"]["description"]["identifier"].split(":")[1]
                        animations = dataA["minecraft:attachable"]["description"]["animations"]
                        animations["wield"] = "animation.player.bow_custom.first_person"
                        animations["third_person"] = "animation.player.bow_custom"
                        animations["wield_first_person_pull"] = "animation.bow.wield_first_person_pull"
                        gmdllist.append(f"geyser_custom:{gmdl}")
                        files = glob.glob(f"staging/target/rp/models/blocks/{namespace}/{path}.json")
                        with open(files[0], "r") as f:
                            data = json.load(f)
                            if Bow_Util.is2Dbow(data["minecraft:geometry"]["bones"]):
                                geometry = ["geometry.bow_standby","geometry.bow_pulling_0","geometry.bow_pulling_1", "geometry.bow_pulling_2"]
                    else:
                        os.remove(fa)
            Bow_Util.item_texture(gmdl, textures[0])
            Bow_Util.write(mfile, gmdl, textures, geometry, mdefault, menchanted, animations)
    except Exception as e:
        import sys
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
Bow_Util.acontroller(gmdllist)