import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def save_all_graphs(id_to_filename_map_1, id_to_filename_map_2, output_folder):
    for selected_id in sorted(set(id_to_filename_map_1.keys()) | set(id_to_filename_map_2.keys())):
        save_graph_to_file(selected_id, 'timestamp_diff', id_to_filename_map_1, id_to_filename_map_2, output_folder)
        save_graph_to_file(selected_id, 'data', id_to_filename_map_1, id_to_filename_map_2, output_folder)
    print("All graphs saved.")


def generate_graph(selected_id, column, id_to_filename_map_1, id_to_filename_map_2):
    folder_path_1 = 'Impersonation_attack_dataset.txt'
    folder_path_2 = 'Fuzzy_attack_dataset.txt'

    file_path_1 = os.path.join(folder_path_1, id_to_filename_map_1.get(selected_id, ""))
    file_path_2 = os.path.join(folder_path_2, id_to_filename_map_2.get(selected_id, ""))

        # 로그: 파일 경로 출력
    print(f"Attempting to load files for ID {selected_id}:")
    print(f"  File 1: {file_path_1} {'[FOUND]' if os.path.isfile(file_path_1) else '[NOT FOUND]'}")
    print(f"  File 2: {file_path_2} {'[FOUND]' if os.path.isfile(file_path_2) else '[NOT FOUND]'}")

    if not os.path.isfile(file_path_1) and not os.path.isfile(file_path_2):
        print(f"Warning: No valid files for ID {file_path_1}.")
        print(f"Warning: No valid files for ID {selected_id}.")
        print(f"Warning: No valid files for ID {column}.")
        return plt.figure()

    df1 = pd.read_csv(file_path_1) if os.path.isfile(file_path_1) else pd.DataFrame()
    df2 = pd.read_csv(file_path_2) if os.path.isfile(file_path_2) else pd.DataFrame()

    # 로그: 데이터프레임 상태 출력
    print(f"  File 1: {'Loaded successfully' if not df1.empty else 'Empty or invalid data'}")
    print(f"  File 2: {'Loaded successfully' if not df2.empty else 'Empty or invalid data'}")

    if df1.empty and df2.empty:
        print(f"Warning: Both files for ID {selected_id} are empty or do not contain data.")
        return plt.figure()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), gridspec_kw={'height_ratios': [1, 1]})

    # 공백 조정
    fig.subplots_adjust(hspace=0.4, top=0.95, bottom=0.1, left=0.1, right=0.95)

    if column == 'data':
        if not df1.empty and 'data' in df1.columns:
            bit_counts_1 = calculate_bit_percentage(df1['data'])
            ax1.bar(range(len(bit_counts_1)), bit_counts_1, label='Folder 1')
            ax1.set_title(f"Folder 1: {file_path_1}")
            ax1.set_ylabel("Bit Percentage (%)")
        else:
            ax1.set_title(f"Folder 1: {file_path_1} - No Data")

        if not df2.empty and 'data' in df2.columns:
            bit_counts_2 = calculate_bit_percentage(df2['data'])
            ax2.bar(range(len(bit_counts_2)), bit_counts_2, label='Folder 2', color='orange')
            ax2.set_title(f"Folder 2: {file_path_2}")
            ax2.set_ylabel("Bit Percentage (%)")
        else:
            ax2.set_title(f"Folder 2: {file_path_2} - No Data")

        ax1.set_xlabel("Bit Position")
        ax2.set_xlabel("Bit Position")
    elif column == 'data_change_rate':
        # 변화율 계산
        if not df1.empty and 'data' in df1.columns:
            bit_change_rate_1 = calculate_bitwise_change_rate(df1['data'])
            ax1.bar(range(len(bit_change_rate_1)), bit_change_rate_1, label='Folder 1')
            ax1.set_title(f"Bitwise Change Rate - Folder 1: {file_path_1}")
            ax1.set_ylabel("Bit Change Percentage (%)")
            ax1.set_xlabel("Bit Position")
        else:
            ax1.set_title(f"Folder 1: {file_path_1} - No Data")

        if not df2.empty and 'data' in df2.columns:
            bit_change_rate_2 = calculate_bitwise_change_rate(df2['data'])
            ax2.bar(range(len(bit_change_rate_2)), bit_change_rate_2, label='Folder 2', color='orange')
            ax2.set_title(f"Bitwise Change Rate - Folder 2: {file_path_2}")
            ax2.set_ylabel("Bit Change Percentage (%)")
            ax2.set_xlabel("Bit Position")
        else:
            ax2.set_title(f"Folder 2: {file_path_2} - No Data")

    else:
        y_max = max(
            df1[column].max() if not df1.empty and column in df1.columns else 0,
            df2[column].max() if not df2.empty and column in df2.columns else 0,
        )

        if y_max == 0:
            print(f"Warning: Column '{column}' has no data in both files for ID {selected_id}.")
            y_max = 1

        if not df1.empty and column in df1.columns:
            ax1.plot(df1.index, df1[column], label='Folder 1', marker='o')
            ax1.set_title(f"Folder 1: {file_path_1}")
        else:
            ax1.set_title(f"Folder 1: {file_path_1} - No Data")

        if not df2.empty and column in df2.columns:
            ax2.plot(df2.index, df2[column], label='Folder 2', marker='x', color='orange')
            ax2.set_title(f"Folder 2: {file_path_2}")
        else:
            ax2.set_title(f"Folder 2: {file_path_2} - No Data")

        ax1.set_ylim(0, y_max)
        ax2.set_ylim(0, y_max)
        ax1.set_ylabel(column)
        ax2.set_ylabel(column)

    return fig


def plot_csv_comparison(selected_id, selected_column, id_to_filename_map_1, id_to_filename_map_2, plot_frame):
    # 기존 그래프 삭제
    for widget in plot_frame.winfo_children():
        widget.destroy()

    # 그래프 생성
    # print(f"plot_csv_comparsion {selected_id, selected_column, id_to_filename_map_1, id_to_filename_map_2}")
    fig = generate_graph(selected_id, selected_column, id_to_filename_map_1, id_to_filename_map_2)

    # 그래프를 Tkinter 창에 표시
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True, pady=10)


def save_graph_to_file(selected_id, column, id_to_filename_map_1, id_to_filename_map_2, output_folder):
    fig = generate_graph(selected_id, column, id_to_filename_map_1, id_to_filename_map_2)

    output_file = os.path.join(output_folder, f"{selected_id}_{column}.png")
    os.makedirs(output_folder, exist_ok=True)
    plt.savefig(output_file)
    plt.close(fig)


def calculate_bit_percentage(data_series):
    bit_counts = np.zeros(64)
    total_bits = 0
    for data_byte in data_series.dropna():
        try:
            data_bytes = bytes.fromhex(str(data_byte).zfill(len(str(data_byte)) + len(str(data_byte)) % 2))
            bit_string = ''.join(format(byte, '08b') for byte in data_bytes)
            total_bits += 1
            # total_bits += len(bit_string)
            for i, bit in enumerate(bit_string):
                if bit == '1':
                    bit_counts[i] += 1
        except ValueError:
            continue
    return (bit_counts / total_bits) * 100 if total_bits > 0 else bit_counts

def calculate_bitwise_change_rate(data_series):
    """Calculate the bit-level change rate across the dataset."""
    if data_series.empty:
        return []

    total_changes = np.zeros(64)
    total_rows = 0
    prev_bits = None

    for value in data_series.dropna():
        try:
            # Convert current value to binary string
            current_bits = ''.join(format(byte, '08b') for byte in bytes.fromhex(str(value).zfill(16)))

            if prev_bits is not None:
                # Compare each bit and count changes
                for i, (prev_bit, current_bit) in enumerate(zip(prev_bits, current_bits)):
                    if prev_bit != current_bit:
                        total_changes[i] += 1
            prev_bits = current_bits
            total_rows += 1
        except ValueError:
            continue

    # Calculate change percentage for each bit
    return (total_changes / total_rows) * 100 if total_rows > 0 else total_changes
