import json, glob, os, shutil

files = glob.glob("pack/assets/**/sounds.json")
print(f"Sounds Files: {files}")
os.makedirs("staging/target/rp/sounds", exist_ok=True)
with open("staging/target/rp/sounds/sound_definitions.json", "w") as f:
    f.write('{"format_version": "1.14.0", "sound_definitions": {}}')
for file in files:
    with open(file, "r") as f:
        data = json.load(f)
    namespace = file.split(os.sep)[1]
    names = [d for d in data]
    with open("staging/target/rp/sounds/sound_definitions.json", "r") as f:
        dj = json.load(f)
        for name in names:
            dj['sound_definitions'][f"{namespace}:{name}"] = {}
            with open("staging/target/rp/sounds/sound_definitions.json", "w") as f:
                try:
                    dj['sound_definitions'][f"{namespace}:{name}"]["category"] = data[name]["category"]
                except:
                    dj['sound_definitions'][f"{namespace}:{name}"]["category"] = "neutral"
                sounds = data[name]["sounds"]
                listsound = []
                for sound in sounds:
                    if type(sound).__name__  == "dict":
                        sound["name"]
                        b = (sound["name"].split(":")[-1] + ".ogg").split((sound['name'].split(':')[-1] + ".ogg").split("/")[-1])[0]
                        sound["name"] = "sounds/" + sound["name"].split(":")[-1]
                        os.makedirs("staging/target/rp/sounds/" + b, exist_ok=True)
                        shutil.copyfile(f"pack/assets/minecraft/{sound['name'].split(':')[-1]}.ogg", f"staging/target/rp/{sound['name'].split(':')[-1]}.ogg")
                        listsound.append(sound)
                    else:
                        b = (sound.split(":")[-1] + ".ogg").split((sound.split(':')[-1] + ".ogg").split("/")[-1])[0]
                        os.makedirs("staging/target/rp/sounds/" + b, exist_ok=True)
                        shutil.copyfile(f"pack/assets/minecraft/sounds/{sound.split(':')[-1]}.ogg", f"staging/target/rp/sounds/{sound.split(':')[-1]}.ogg")
                        a = "sounds/" + sound.split(":")[-1]
                        listsound.append(a)
                dj["sound_definitions"][f"{namespace}:{name}"]["sounds"] = listsound
                json.dump(dj, f, indent=2)
