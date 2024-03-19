import json
import glob
import os

def get_am_file(model):
    namespace = model.split(":")[0]
    path = model.split(":")[1]
    files = glob.glob(f"staging/target/rp/attachables/{namespace}/{path}*.json")
    for fa in files:
        if f"{path.split('/')[-1]}." in fa:
            return fa
def write_animated_cube():
    #Created by: ofunny, contact: https://ofunny.world/, repository: https://github.com/ofunny/ofunnysBedrockExamples/
    #file from ofunny
    data = {"format_version":"1.8.0","animations":{"animation.geo_cube.thirdperson_main_hand":{"loop":True,"bones":{"block":{"rotation":[-20,145,-10],"position":[0,14,-6],"scale":[0.375,0.375,0.375]}}},"animation.geo_cube.thirdperson_off_hand":{"loop":True,"bones":{"block":{"rotation":[20,40,20],"position":[0,13,-6],"scale":[0.375,0.375,0.375]}}},"animation.geo_cube.head":{"loop":True,"bones":{"block":{"position":[0,19.9,0],"scale":0.625}}},"animation.geo_cube.firstperson_main_hand":{"loop":True,"bones":{"block":{"rotation":[140,45,15],"position":[-1,17,0],"scale":[0.52,0.52,0.52]}}},"animation.geo_cube.firstperson_off_hand":{"loop":True,"bones":{"block":{"rotation":[-5,45,-5],"position":[-17.5,17.5,15],"scale":[0.52,0.52,0.52]}}}}}
    with open("staging/target/rp/animations/cube.json", "w") as f:
        json.dump(data, f)
def write_geometry_cube():
    #Created by: ofunny, contact: https://ofunny.world/, repository: https://github.com/ofunny/ofunnysBedrockExamples/
    #file from ofunny
    data = {"format_version":"1.19.40","minecraft:geometry":[{"description":{"identifier":"geometry.cube","texture_width":16,"texture_height":16,"visible_bounds_width":2,"visible_bounds_height":2.5,"visible_bounds_offset":[0,0.75,0]},"bones":[{"name":"block","binding":"c.item_slot == 'head' ? 'head' : q.item_slot_to_bone_name(c.item_slot)","pivot":[0,8,0],"cubes":[{"origin":[-8,0,-8],"size":[16,16,16],"uv":{"north":{"uv":[0,0],"uv_size":[16,16]},"east":{"uv":[0,0],"uv_size":[16,16]},"south":{"uv":[0,0],"uv_size":[16,16]},"west":{"uv":[0,0],"uv_size":[16,16]},"up":{"uv":[16,16],"uv_size":[-16,-16]},"down":{"uv":[16,16],"uv_size":[-16,-16]}}}]}]}]}
    with open("staging/target/rp/models/blocks/cube.json", "w") as f:
        json.dump(data, f)
def write_mapping_block(block: str):
    #Created by: ofunny, contact: https://ofunny.world/, repository: https://github.com/ofunny/ofunnysBedrockExamples/
    #file from ofunny 
    data = {"format_version":1,"blocks":{f"minecraft:{block}":{"name":f"{block}","geometry":"geometry.cube","included_in_creative_inventory":False,"only_override_states":True,"place_air":True,"state_overrides":{}}}}
    with open(f"staging/target/geyser_block_{block}_mappings.json", "w") as f:
        json.dump(data, f, indent=4)
def regsister_block(block: str, gmdl: str, state: str, texture: str, block_material: str, geometry: str):
    with open(f"staging/target/geyser_block_{block}_mappings.json", "r") as f:
        data = json.load(f)
    with open(f"staging/target/geyser_block_{block}_mappings.json", "w") as f:
        data["blocks"][f"minecraft:{block}"]["state_overrides"][state] = {"name":f"block_{gmdl}","display_name":f"block_{gmdl}","geometry":geometry,"material_instances":{"*":{"texture":texture,"render_method":block_material,"face_dimming":True,"ambient_occlusion":True}}}
        json.dump(data, f, indent=4)
def create_terrain_texture(gmdl: str, texture_file: str):
    with open("staging/target/rp/textures/terrain_texture.json", "r") as f:
        data = json.load(f)
    with open("staging/target/rp/textures/terrain_texture.json", "w") as f:
        data["texture_data"][f"block_{gmdl}"] = {"textures": texture_file}
        json.dump(data, f, indent=4)
    return f"block_{gmdl}"
def get_geometry_block(model: str):
    namespace = model.split(":")[0]
    path = model.split(":")[1]
    geometry_file = glob.glob(f"staging/target/rp/models/blocks/{namespace}/{path}.json")[0]
    if geometry_file != None:
        with open(geometry_file, "r") as f:
            geo_data = f.read()
            if geo_data == "":
                os.remove(geometry_file)
                return "geometry.cube"
            else:
                data = json.loads(geo_data)
                return data["minecraft:geometry"][0]["description"]["identifier"]
    else: return "geometry.cube"
