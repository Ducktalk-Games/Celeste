import unreal

asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

master_mat_name = "M_PropsMaster"
master_mat_path = "/Game/AssetTools/MasterMaterials/" + master_mat_name

master_mat = unreal.EditorAssetLibrary.load_asset(master_mat_path)


def set_mi_texture(mi_asset, param_name, tex_path):
    if not unreal.EditorAssetLibrary.does_asset_exist(tex_path):
        unreal.log_warning("Can't find texture: " + tex_path)
        return False
    tex_asset = unreal.EditorAssetLibrary.find_asset_data( tex_path ).get_asset()
    return unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(mi_asset, param_name, tex_asset)

if unreal.EditorAssetLibrary.does_asset_exist(master_mat_path):
    print("Master Mat exists!")

    selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()

    for asset in selected_assets:

        if type(asset) == unreal.Texture2D:
            print("this is a texture!")

            asset_name = asset.get_name()

            if "T_" in asset_name:

                texture_path = asset.get_path_name()

                material_instance_name = "MI_" + asset_name.split("_")[1]

                asset_path = "/".join(texture_path.split("/")[:-2])

                material_instance_path = asset_path + "/" + material_instance_name

                material_instance = None

                if unreal.EditorAssetLibrary.does_asset_exist(material_instance_path):
                    material_instance = unreal.EditorAssetLibrary.load_asset(material_instance_path)

                if not material_instance:
                    material_instance = asset_tools.create_asset(material_instance_name,
                                                                 asset_path,
                                                                 None,
                                                                 unreal.MaterialInstanceConstantFactoryNew())

                    material_instance.set_editor_property("parent", master_mat)
                    unreal.EditorAssetLibrary.save_loaded_asset(material_instance)

                    master_mat = unreal.EditorAssetLibrary.load_asset(master_mat_path)

                if material_instance:
                    set_mi_texture(material_instance, asset_name.split("_")[2], texture_path)