# examples/12_stacked_bar_example.py

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

# --- Thêm thư mục src vào Python Path ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(project_root, 'src'))

# Import các hàm cần thiết
from publication_style import set_publication_style, COLOR_PALETTE
from plot_templates import plot_stacked_bar_chart

# --- Bước 1: Thiết lập Style chung ---
set_publication_style(font_family='sans-serif')

# --- Bước 2: Chuẩn bị dữ liệu ---
df = pd.read_csv(os.path.join(project_root, 'data', 'sample_latency_breakdown.csv'))

# Danh sách các cột thành phần
component_cols = ['Propagation Time (ms)', 'Queuing Time (ms)', 'Processing Time (ms)']

# Tạo bảng màu tùy chỉnh để đảm bảo sự nhất quán
custom_palette = {
    'Propagation Time (ms)': COLOR_PALETTE['gray'],
    'Queuing Time (ms)': COLOR_PALETTE['orange'],
    'Processing Time (ms)': COLOR_PALETTE['blue']
}

# --- Bước 3: Vẽ Stacked Bar Chart (Giá trị tuyệt đối) ---
print("--- Generating Absolute Stacked Bar Chart ---")
output_path_abs = os.path.join(project_root, 'figures', '18_latency_breakdown_absolute.pdf')
plot_stacked_bar_chart(
    data=df,
    category_col='Algorithm',
    component_cols=component_cols,
    y_label='Total Latency (ms)',
    title='Breakdown of End-to-End Latency by Algorithm',
    output_path=output_path_abs,
    palette=custom_palette
)

# --- Bước 4: Vẽ 100% Stacked Bar Chart (Tỷ lệ) ---
print("\n--- Generating 100% Stacked Bar Chart ---")
output_path_perc = os.path.join(project_root, 'figures', '19_latency_breakdown_percentage.pdf')
plot_stacked_bar_chart(
    data=df,
    category_col='Algorithm',
    component_cols=component_cols,
    y_label='Latency Components', # Nhãn sẽ được tự động thêm "(%)"
    title='Proportional Breakdown of Latency Components',
    output_path=output_path_perc,
    is_100_percent=True, # <--- Bật chế độ 100%
    palette=custom_palette
)
