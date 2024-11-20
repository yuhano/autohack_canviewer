import os
import const

def load_files():
    folder_path_1 = const.folder_path_1
    folder_path_2 = const.folder_path_2

    csv_files_1 = [f for f in os.listdir(folder_path_1) if f.endswith('.csv')]
    csv_files_2 = [f for f in os.listdir(folder_path_2) if f.endswith('.csv')]

    id_to_filename_map_1 = {file.split('_')[0]: file for file in csv_files_1}
    id_to_filename_map_2 = {file.split('_')[0]: file for file in csv_files_2}

    files_info = []
    for id in sorted(set(id_to_filename_map_1.keys()) | set(id_to_filename_map_2.keys())):
        dlc_1 = dlc_2 = per_f1 = per_f2 = ""
        if id in id_to_filename_map_1:
            file_1 = id_to_filename_map_1[id]
            parts = file_1.split('_')
            if len(parts) >= 4:
                dlc_1 = parts[1]
                per_f1 = parts[2]
        if id in id_to_filename_map_2:
            file_2 = id_to_filename_map_2[id]
            parts = file_2.split('_')
            if len(parts) >= 4:
                dlc_2 = parts[1]
                per_f2 = parts[2]
        files_info.append((id, dlc_1, dlc_2, per_f1, per_f2))

    return files_info, id_to_filename_map_1, id_to_filename_map_2
