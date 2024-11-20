import os

def get_output_folder():
    folder_path_1 = 'Impersonation_attack_dataset.txt'
    folder_path_2 = 'Fuzzy_attack_dataset.txt'
    output_folder = f"graph__{os.path.basename(folder_path_1)}_{os.path.basename(folder_path_2)}"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder
