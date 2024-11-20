import os
import const

def get_output_folder():
    folder_path_1 = const.folder_path_1
    folder_path_2 = const.folder_path_2
    output_folder = f"graph__{os.path.basename(folder_path_1)}_{os.path.basename(folder_path_2)}"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder
