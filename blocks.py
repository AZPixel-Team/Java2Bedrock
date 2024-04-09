import json
import glob
import os
import blocks_util

#Not Support For Fire
files = glob.glob("pack/assets/minecraft/blockstates/*.json")
if files != []:
    blocks_util.write_animated_cube()
    blocks_util.write_geometry_cube()
for file in files:
    file = file.replace("\\", "/")
    block = (file.split("/")[-1]).replace(".json", "")
    if (block == "fire"): continue
    block_material = os.getenv("BLOCK_MATERIAL")
    blocks_util.write_mapping_block(block)
    with open(file, "r") as f:
        data = json.load(f)["variants"]
        for k, v in data.items():
            if not("block/original" in v["model"] or "block/tripwire_attached_n" in v["model"]):
                print(v["model"])
                am = blocks_util.get_am_file(v["model"])
                if am == None: continue
                with open(am, "r") as f:
                    data_am = json.load(f)
                    gmdl = data_am["minecraft:attachable"]["description"]["identifier"].split(":")[1]
                    geometry = blocks_util.get_geometry_block(v["model"])
                    texture = blocks_util.create_terrain_texture(gmdl, data_am["minecraft:attachable"]["description"]["textures"]["default"])
                if geometry == "geometry.cube":
                    with open(am, "w") as f:
                        data_am["minecraft:attachable"]["description"]["geometry"]["default"] = "geometry.cube"
                        data_am["minecraft:attachable"]["description"]["animations"] = {"thirdperson_main_hand":"animation.geo_cube.thirdperson_main_hand","thirdperson_off_hand":"animation.geo_cube.thirdperson_off_hand","thirdperson_head":"animation.geo_cube.head","firstperson_main_hand":"animation.geo_cube.firstperson_main_hand","firstperson_off_hand":"animation.geo_cube.firstperson_off_hand","firstperson_head":"animation.geyser_custom.disable"}
                        json.dump(data_am, f)
                if block == "tripwire":
                    sstate = k.split(",")
                    k = f"{sstate[0]},{sstate[4]},{sstate[1]},{sstate[2]},{sstate[6]},{sstate[3]},{sstate[5]}"
                blocks_util.regsister_block(block, gmdl, k, texture, block_material, geometry)
