import json
import os

class Bow_Util:
    def write(file, gmdl, textures, geometry, mdefault, menchanted, animations, animate, pre_animation):
        with open(file, "w") as f:
            data = {
                "format_version": "1.10.0",
                "minecraft:attachable": {
                    "description": {
                        "identifier": f"geyser_custom:{gmdl}",
                        "materials": {
                            "default": f"{mdefault}",
                            "enchanted": f"{menchanted}"
                        },
                        "textures": {
                            "default": f"{textures[0]}",
                            "bow_pulling_0": f"{textures[1]}",
                            "bow_pulling_1": f"{textures[2]}",
                            "bow_pulling_2": f"{textures[3]}",
                            "enchanted": "textures/misc/enchanted_item_glint"
                        },
                        "geometry": {
                            "default": f"{geometry[0]}",
                            "bow_pulling_0": f"{geometry[1]}",
                            "bow_pulling_1": f"{geometry[2]}",
                            "bow_pulling_2": f"{geometry[3]}"
                        },
                        "animations": animations,
                        "scripts": {
                            "pre_animation": pre_animation,
                            "animate": animate,
                        },
                        "render_controllers": ["controller.render.bow_custom"]
                    }
                }
            }
            json.dump(data, f)
    def rendercontrollers():
        file = "staging/target/rp/render_controllers/bow_custom.render_controllers.json"
        os.makedirs(os.path.dirname(file), exist_ok=True)
        with open(file, "w") as f:
            data = {
                "format_version": "1.10",
                "render_controllers": {
                    "controller.render.bow_custom": {
                    "arrays": {
                        "textures": {
                        "array.bow_texture_frames": [
                            "texture.default",
                            "texture.bow_pulling_0",
                            "texture.bow_pulling_1",
                            "texture.bow_pulling_2"
                        ]
                        },
                        "geometries": {
                        "array.bow_geo_frames": [
                            "geometry.default",
                            "geometry.bow_pulling_0",
                            "geometry.bow_pulling_1",
                            "geometry.bow_pulling_2"
                        ]
                        }
                    },
                    "geometry": "array.bow_geo_frames[math.floor(v.frame)]",
                    "materials": [ { "*": "variable.is_enchanted ? material.enchanted : material.default" } ],
                    "textures": [ "array.bow_texture_frames[math.floor(v.frame)]", "texture.enchanted" ]
                    }
                }
            }
            json.dump(data, f)
    def item_texture(gmdl, texture):
        with open("staging/target/rp/textures/item_texture.json", "r") as f:
            data = json.load(f)
        if gmdl in data["texture_data"]:
            with open("staging/target/rp/textures/item_texture.json", "w") as f:
                data["texture_data"][gmdl]["textures"] = texture
                json.dump(data,f, indent=4)
    def animation():
        with open("staging/target/rp/animations/bow_custom.animation.json","w") as f:
            data = {
                "format_version": "1.8.0",
                "animations": {
                    "animation.player.bow_custom.first_person": {
                    "loop": True,
                    "bones": {
                        "rightitem": {
                        "rotation": [ "c.is_first_person ? 30 : 0", "c.is_first_person ? -120 : 0", "c.is_first_person ? -60 : 0" ],
                        "position": [ " c.is_first_person ? -6 : 0", "c.is_first_person ? -5 : 0", "c.is_first_person ? -2 : 0" ]
                        }
                    }
                    },
                    "animation.player.bow_custom": {
                    "loop": True,
                    "bones": {
                        "rightitem": {
                        "position": [ 0.5, -2, 0 ]
                        }
                    }
                    }
                }
                }
            json.dump(data,f)
    def is2Dbow(file):
        with open(file, "r") as f:
            try:
                modelbone = json.load(f)["minecraft:geometry"][0]["bones"]
            except:
                modelbone = []
        if modelbone == [{"name":"geyser_custom","binding":"c.item_slot == 'head' ? 'head' : q.item_slot_to_bone_name(c.item_slot)","pivot":[0,8,0]},{"name":"geyser_custom_x","parent":"geyser_custom","pivot":[0,8,0]},{"name":"geyser_custom_y","parent":"geyser_custom_x","pivot":[0,8,0]},{"name":"geyser_custom_z","parent":"geyser_custom_y","pivot":[0,8,0],"texture_meshes":[{"texture":"default","position":[0,8,0],"rotation":[90,0,-180],"local_pivot":[8,0.5,8]}]}]:
            return True
        else:
            return False
    def acontroller(gmdllist):
        strlist = str(gmdllist)
        strlist = strlist.replace("[", "").replace("]", "")
        file = "staging/target/rp/animation_controllers/player.animation_controllers.json"
        os.makedirs(os.path.dirname(file), exist_ok=True)
        with open(file, "w") as f:
            data = {
                "format_version" : "1.10.0",
                "animation_controllers" : {
                    "controller.animation.player.root" : {
                        "initial_state" : "first_person",
                        "states" : {
                            "first_person" : {
                                "animations" : [
                                    {
                                        "first_person_swap_item": "!query.blocking"
                                    },
                                    {
                                        "first_person_shield_block": "query.blocking"
                                    },
                                    {
                                        "first_person_attack_controller" : "variable.attack_time > 0.0f && query.get_equipped_item_name != 'filled_map'"
                                    },
                                    "first_person_base_pose",
                                    {
                                        "first_person_empty_hand" : "query.get_equipped_item_name(0, 1) != 'filled_map'"
                                    },
                                    {
                                        "first_person_walk" : "variable.bob_animation"
                                    },
                                    {
                                        "first_person_map_controller" : "(query.get_equipped_item_name(0, 1) == 'filled_map' || query.get_equipped_item_name('off_hand') == 'filled_map')"
                                    },
                                    {
                                        "first_person_crossbow_equipped": "query.get_equipped_item_name == 'crossbow' && (variable.item_use_normalized > 0 && variable.item_use_normalized < 1.0)"
                                    },
                                    {
                                        "first_person_breathing_bob": "variable.attack_time <= 0.0"
                                    }
                                ],
                                "transitions" : [
                                    {
                                        "paperdoll" : "variable.is_paperdoll"
                                    },
                                    {
                                        "map_player" : "variable.map_face_icon"
                                    },
                                    {
                                        "third_person" : "!variable.is_first_person"
                                    }
                                ]
                            },
                            "map_player" : {
                                "transitions" : [
                                    {
                                        "paperdoll" : "variable.is_paperdoll"
                                    },
                                    {
                                        "first_person" : "variable.is_first_person"
                                    },
                                    {
                                        "third_person" : "!variable.map_face_icon && !variable.is_first_person"
                                    }
                                ]
                            },
                            "paperdoll" : {
                                "animations" : [ "humanoid_base_pose", "look_at_target_ui", "move.arms", "move.legs", "cape" ],
                                "transitions" : [
                                    {
                                        "first_person" : "!variable.is_paperdoll && variable.is_first_person"
                                    },
                                    {
                                        "map_player" : "variable.map_face_icon"
                                    },
                                    {
                                        "third_person" : "!variable.is_paperdoll && !variable.is_first_person"
                                    }
                                ]
                            },
                            "third_person" : {
                                "animations" : [
                                    "humanoid_base_pose",
                                    {
                                        "look_at_target" : "!query.is_sleeping && !query.is_emoting"
                                    },
                                    "move.arms",
                                    "move.legs",
                                    "cape",
                                    {
                                        "riding.arms" : "query.is_riding"
                                    },
                                    {
                                        "riding.legs" : "query.is_riding"
                                    },
                                    "holding",
                                    {
                                        "brandish_spear" : "variable.is_brandishing_spear"
                                    },
                                    {
                                        "holding_spyglass": "variable.is_holding_spyglass"
                                    },
                                    {
                                        "charging" : "query.is_charging"
                                    },
                                    {
                                        "sneaking" : "query.is_sneaking && !query.is_sleeping"
                                    },
                                    {
                                        "bob": "!variable.is_holding_spyglass && !variable.is_tooting_goat_horn"
                                    },
                                    {
                                        "damage_nearby_mobs" : "variable.damage_nearby_mobs"
                                    },
                                    {
                                        "swimming" : "variable.swim_amount > 0.0"
                                    },
                                    {
                                        "swimming.legs" : "variable.swim_amount > 0.0"
                                    },
                                    {
                                        "use_item_progress": f"( variable.use_item_interval_progress > 0.0 ) || ( variable.use_item_startup_progress > 0.0 ) && !variable.is_brandishing_spear && !variable.is_holding_spyglass && !variable.is_tooting_goat_horn && !query.is_item_name_any('slot.weapon.mainhand', 'minecraft:bow', {strlist})"
                                    },
                                    {
                                        "sleeping" : "query.is_sleeping && query.is_alive"
                                    },
                                    {
                                        "attack.positions" : "variable.attack_time >= 0.0"
                                    },
                                    {
                                        "attack.rotations" : "variable.attack_time >= 0.0"
                                    },
                                    {
                                        "shield_block_main_hand" : "query.blocking && query.get_equipped_item_name('off_hand') != 'shield' && query.get_equipped_item_name == 'shield'"
                                    },
                                    {
                                        "shield_block_off_hand" : "query.blocking && query.get_equipped_item_name('off_hand') == 'shield'"
                                    },
                                    {
                                        "crossbow_controller" : "query.get_equipped_item_name == 'crossbow'"
                                    },
                                    {
                                        "third_person_bow_equipped" : f"query.is_item_name_any('slot.weapon.mainhand', 0, 'minecraft:bow', {strlist}) && (q.is_using_item)"
                                    },
                                    {
                                        "tooting_goat_horn": "variable.is_tooting_goat_horn"
                                    }
                                ],
                                "transitions" : [
                                    {
                                        "paperdoll" : "variable.is_paperdoll"
                                    },
                                    {
                                        "first_person" : "variable.is_first_person"
                                    },
                                    {
                                        "map_player" : "variable.map_face_icon"
                                    }
                                ]
                            }
                        }
                    }
                }
            }
            json.dump(data, f)