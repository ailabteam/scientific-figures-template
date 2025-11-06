# examples/02_line_plot_example.py
import sys
import os
import pandas as pd

# Thêm thư mục src vào Python Path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(project_root, 'src'))

# Import các hàm cần thiết
from publication_style import set_publication_style
from plot_templates import plot_line_comparison

# --- Bước 1: Thiết lập Style ---
set_publication_style(font_family='sans-serif')

# --- Bước 2: Chuẩn bị dữ liệu ---
# Load dữ liệu từ file CSV
data_path = os.path.join(project_root, 'data', 'sample_qber_data.csv')
df = pd.read_csv(data_path)

# --- Bước 3: Gọi hàm vẽ từ template ---
output_path = os.path.join(project_root, 'figures', '02_qber_comparison.pdf')

plot_line_comparison(
    data=df,
    x_col='distance',
    y_cols=['our_method', 'protocol_B', 'protocol_A'], # Thứ tự quan trọng, 'our' lên đầu
    y_labels=['Our Proposed Method', 'Protocol B (SOTA)', 'Protocol A (Baseline)'],
    x_label='Distance (km)',
    y_label='Quantum Bit Error Rate (QBER)',
    title='Performance of QKD Protocols over Distance',
    output_path=output_path,
    # Thêm các tùy chỉnh khác nếu muốn
    ylim=(0, 0.06),
    yscale='linear' # hoặc 'log'
)

# --- Ví dụ 2: Vẽ trên thang log ---
output_path_log = os.path.join(project_root, 'figures', '03_qber_comparison_log.pdf')

plot_line_comparison(
    data=df,
    x_col='distance',
    y_cols=['our_method', 'protocol_B', 'protocol_A'],
    y_labels=['Our Proposed Method', 'Protocol B (SOTA)', 'Protocol A (Baseline)'],
    x_label='Distance (km)',
    y_label='Quantum Bit Error Rate (QBER)',
    title='Performance of QKD Protocols (Log Scale)',
    output_path=output_path_log,
    yscale='log' # Thay đổi ở đây
)
