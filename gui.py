import tkinter as tk
from tkinter import font
from tkinter import ttk, messagebox
from graph_plotter import plot_csv_comparison, save_all_graphs
from file_manager import load_files
from utils import get_output_folder
import os
import sys
import const

# 현재 선택된 플롯 타입을 저장하는 변수
selected_plot_type = "timestamp_diff"  # 초기값: "timestamp_diff"


def create_gui(root):
    root.title("CSV File Selection and Graph Comparison")
    root.geometry("1200x800")
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=3)

    # Left frame
    left_frame = tk.Frame(root)
    left_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
    root.grid_rowconfigure(0, weight=1)
    left_frame.grid_columnconfigure(0, weight=1)

    label = tk.Label(left_frame, text="Select CSV File for Comparison:")
    label.grid(row=0, column=0, pady=10, sticky='w')

    # Treeview columns with new E1, E2 columns for file existence
    columns = ('_ID_', 'd1', 'd2', 'Per_1', 'Per_2', 'E1', 'E2')
    file_treeview = ttk.Treeview(left_frame, columns=columns, show='headings', selectmode='browse')
    file_treeview.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
    left_frame.grid_rowconfigure(1, weight=1)

    # Set column width based on header text size
    header_font = font.Font()
    for col in columns:
        text_width = header_font.measure(col) + 20  # Add some padding
        file_treeview.heading(col, text=col, anchor='w')
        file_treeview.column(col, width=text_width, anchor='w')  # Adjust column width

    button_frame = tk.Frame(left_frame)
    button_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=10)

    # Right frame
    plot_frame = tk.Frame(root)
    plot_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
    root.grid_columnconfigure(1, weight=3)

    # Load files and populate the treeview
    files_info, id_to_filename_map_1, id_to_filename_map_2 = load_files()

    # Check file existence and populate Treeview
    folder_path_1 = const.folder_path_1
    folder_path_2 = const.folder_path_2

    for file_data in files_info:
        file_id = file_data[0]
        file_path_1 = os.path.join(folder_path_1, id_to_filename_map_1.get(file_id, ""))
        file_path_2 = os.path.join(folder_path_2, id_to_filename_map_2.get(file_id, ""))
        e1_status = "O" if os.path.isfile(file_path_1) else "X"
        e2_status = "O" if os.path.isfile(file_path_2) else "X"

        # Add file existence status to Treeview
        file_treeview.insert('', 'end', values=(*file_data, e1_status, e2_status))

    def get_selected_id(treeview):
        selected_item = treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a file from the list.")
            return None
        return treeview.item(selected_item, 'values')[0]

    def update_selected_plot_type_and_plot(plot_type, treeview, id_to_filename_map_1, id_to_filename_map_2, plot_frame):
        global selected_plot_type  # 선택한 플롯 타입을 저장하는 변수
        selected_plot_type = plot_type  # 현재 선택한 플롯 타입 업데이트
        selected_id = get_selected_id(treeview)  # 트리뷰에서 선택된 ID 가져오기
        if selected_id:
            plot_csv_comparison(selected_id, selected_plot_type, id_to_filename_map_1, id_to_filename_map_2, plot_frame)

    def select_file(event):
        selected_id = get_selected_id(file_treeview)
        if selected_id:
            # 이전에 선택된 플롯 타입으로 그래프를 그리기
            plot_csv_comparison(selected_id, selected_plot_type, id_to_filename_map_1, id_to_filename_map_2, plot_frame)

    file_treeview.bind("<<TreeviewSelect>>", select_file)

    def create_dynamic_button(parent, text, command):
        button = tk.Button(parent, text=text, command=command, wraplength=200)
        button.pack(fill='x', pady=5, padx=5)
        button.update_idletasks()
        button.config(width=len(text) + 5)
        return button

    # 버튼 생성
    create_dynamic_button(
        button_frame,
        "Plot timestamp_diff",
        lambda: update_selected_plot_type_and_plot(
            "timestamp_diff", file_treeview, id_to_filename_map_1, id_to_filename_map_2, plot_frame
        )
    )
    create_dynamic_button(
        button_frame,
        "Plot data bit count",
        lambda: update_selected_plot_type_and_plot(
            "data", file_treeview, id_to_filename_map_1, id_to_filename_map_2, plot_frame
        )
    )
        # 변화율 플롯 버튼 추가
    # 비트 변화율 플롯 버튼 추가
    create_dynamic_button(
        button_frame,
        "Plot Bitwise Change Rate",
        lambda: update_selected_plot_type_and_plot(
            "data_change_rate", file_treeview, id_to_filename_map_1, id_to_filename_map_2, plot_frame
        )
    )



    # 새로고침 버튼 추가
    def refresh_program():
        """Restart the current program."""
        python = sys.executable
        os.execl(python, python, *sys.argv)

    create_dynamic_button(
        button_frame,
        "Refresh",
        refresh_program
    )

    # "Save All Graphs" 버튼 추가
    def save_all_graphs_button_action():
        output_folder = get_output_folder()  # Output folder 결정
        save_all_graphs(id_to_filename_map_1, id_to_filename_map_2, output_folder)
        messagebox.showinfo("Save Complete", f"All graphs have been saved to {output_folder}.")

    create_dynamic_button(
        button_frame,
        "Save All Graphs",
        save_all_graphs_button_action
    )

    def on_closing():
        root.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
