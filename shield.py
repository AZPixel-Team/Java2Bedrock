import os
import json
import glob

if os.path.exists("pack/assets/minecraft/models/item/shield.json"):
    with open("pack/assets/minecraft/models/item/shield.json") as f:
        data = json.load(f)
        predicate = [d["predicate"] for d in data["overrides"]]
        model = [d["model"] for d in data["overrides"]]
    for m, p in zip(model, predicate):
        if m == "item/shield" or "custom_model_data" not in p: continue
        try:
            fpath = (f"cache/shield/{p['custom_model_data']}.json")
            if not os.path.exists(fpath):
                os.makedirs(os.path.dirname(fpath), exist_ok=True)
                with open(fpath, "w") as f:
                    f.write("{}")
            with open(fpath, "r") as f:
                data = json.load(f)
            with open(fpath, "w") as f:
                if ("blocking" in p): data["blocking"] = m
                else: data["default"] = m
                if "check" in data: data["check"] = data["check"] + 1
                else: data["check"] = 1
                json.dump(data, f, indent=2)
        except Exception as e:
            print(e)
            pass

for file in glob.glob("cache/shield/*.json"):
    with open(file, "r") as f:
        data = json.load(f)
    if data["check"] == 2:
        animation = {}
        for i in ["default", "blocking"]:
            namespace = data[i].split(":")[0]
            path = data[i].split(":")[1]
            files = glob.glob(f"staging/target/rp/attachables/{namespace}/{path}*.json")
            for fa in files:
                if f"{path.split('/')[-1]}." in fa:
                    break
            with open(fa, "r") as f:
                dataA = json.load(f)
                animationitem = dataA["minecraft:attachable"]["description"]["animations"]
                gmdl = dataA["minecraft:attachable"]["description"]["identifier"]
            if i == "default":
                saf = fa
                adata = dataA
                animation["mainhand.first_person"] = animationitem["firstperson_main_hand"]
                animation["mainhand.thierd_person"] = animationitem["thirdperson_main_hand"]
                animation["offhand.first_person"] = animationitem["firstperson_off_hand"]
                animation["offhand.thierd_person"] = animationitem["thirdperson_off_hand"]
                animate = [
                    {"mainhand.thierd_person.block": f"!c.is_first_person && c.item_slot == 'main_hand' && q.is_item_name_any('slot.weapon.mainhand', '{gmdl}') && query.is_sneaking"},
                    {"mainhand.first_person.block": f"c.is_first_person && c.item_slot == 'main_hand' && q.is_item_name_any('slot.weapon.mainhand', '{gmdl}') && query.is_sneaking"},
                    {"mainhand.first_person": f"c.is_first_person && c.item_slot == 'main_hand' && q.is_item_name_any('slot.weapon.mainhand', '{gmdl}') && !query.is_sneaking"},
                    {"mainhand.thierd_person": f"!c.is_first_person && c.item_slot == 'main_hand' && q.is_item_name_any('slot.weapon.mainhand', '{gmdl}') && !query.is_sneaking"},

                    {"offhand.thierd_person.block": f"!c.is_first_person && c.item_slot == 'off_hand' && q.is_item_name_any('slot.weapon.offhand', '{gmdl}') && query.is_sneaking"},
                    {"offhand.first_person.block": f"c.is_first_person && c.item_slot == 'off_hand' && q.is_item_name_any('slot.weapon.offhand', '{gmdl}') && query.is_sneaking"},
                    {"offhand.first_person": f"c.is_first_person && c.item_slot == 'off_hand' && q.is_item_name_any('slot.weapon.offhand', '{gmdl}') && !query.is_sneaking"},
                    {"offhand.thierd_person": f"!c.is_first_person && c.item_slot == 'off_hand' && q.is_item_name_any('slot.weapon.offhand', '{gmdl}') && !query.is_sneaking"}
                ]
            else:
                animation["mainhand.first_person.block"] = animationitem["firstperson_main_hand"]
                animation["mainhand.thierd_person.block"] = animationitem["thirdperson_main_hand"]
                animation["offhand.first_person.block"] = animationitem["firstperson_off_hand"]
                animation["offhand.thierd_person.block"] = animationitem["thirdperson_off_hand"]
                os.remove(fa)
        with open(saf, "w") as f:
            adata["minecraft:attachable"]["description"]["animations"] = animation
            adata["minecraft:attachable"]["description"]["scripts"]["animate"] = animate
            json.dump(adata, f)