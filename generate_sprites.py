import os
import json
import glob

def resolve_model_path(model_str, base_dir):
    # e.g., "iasurvival:item/ia_auto/aqualight_sword"
    if ":" in model_str:
        namespace, path = model_str.split(":", 1)
    else:
        namespace = "minecraft"
        path = model_str
    
    # Resolves to "assets/iasurvival/models/item/ia_auto/aqualight_sword.json"
    return os.path.join(base_dir, namespace, "models", path + ".json")

def clean_texture_path(texture_str):
    # e.g., "iasurvival:item/ia_auto/aqualight_sword"
    if ":" in texture_str:
        namespace, path = texture_str.split(":", 1)
    else:
        namespace = "minecraft"
        path = texture_str
        
    # java2bedrock usually expects just the texture path without "item/" if it's items
    # let's just keep the full namespace:path because the converter handles it, or return the name.
    # Actually java2bedrock expects exactly the texture identifier found in the resource pack.
    # Usually returning the raw texture_str works.
    return texture_str

def main():
    assets_dir = os.path.join("temp_pack", "assets")
    mc_item_models = glob.glob(os.path.join(assets_dir, "minecraft", "models", "item", "*.json"))
    
    sprites_map = {}
    
    for mc_model_file in mc_item_models:
        base_item_name = os.path.basename(mc_model_file).replace(".json", "")
        base_item_key = f"minecraft:{base_item_name}"
        
        with open(mc_model_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except Exception:
                continue
                
        if "overrides" not in data:
            continue
            
        for override in data["overrides"]:
            if "predicate" not in override or "custom_model_data" not in override["predicate"]:
                continue
                
            cmd = str(override["predicate"]["custom_model_data"])
            custom_model_str = override["model"]
            
            # Now we look into the custom model JSON to find the texture
            custom_model_path = resolve_model_path(custom_model_str, assets_dir)
            
            texture_found = False
            if os.path.exists(custom_model_path):
                with open(custom_model_path, 'r', encoding='utf-8') as cf:
                    try:
                        cdata = json.load(cf)
                        if "textures" in cdata:
                            # Prefer layer0 for inventory icon
                            if "layer0" in cdata["textures"]:
                                texture_val = cdata["textures"]["layer0"]
                                
                                if base_item_key not in sprites_map:
                                    sprites_map[base_item_key] = {}
                                sprites_map[base_item_key][cmd] = texture_val
                                texture_found = True
                    except Exception:
                        pass
                        
            # If we couldn't find layer0 texture, we use the custom model base identifier itself
            if not texture_found:
                 if base_item_key not in sprites_map:
                     sprites_map[base_item_key] = {}
                 sprites_map[base_item_key][cmd] = custom_model_str

    out_file = os.path.join("temp_pack", "sprites.json")
    with open(out_file, "w", encoding='utf-8') as f:
         json.dump(sprites_map, f, indent=4)
         
    print(f"Generated sprites.json with {len(sprites_map)} base items configured!")

if __name__ == "__main__":
    main()
