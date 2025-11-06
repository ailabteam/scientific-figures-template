# examples/03_bar_chart_example.py

import sys
import os
import pandas as pd

# Thêm thư mục src vào Python Path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(project_root, 'src'))

# Import các hàm cần thiết
from publication_style import set_publication_style, CONTEXT_COLORS
from plot_templates import plot_grouped_bar_chart

# --- Bước 1: Thiết lập Style ---
set_publication_style(font_family='sans-serif')

# --- Bước 2: Chuẩn bị dữ liệu ---
data_path = os.path.join(project_root, 'data', 'sample_model_performance.csv')
df = pd.read_csv(data_path)

# --- Bước 3: Gọi hàm vẽ từ template để so sánh các metric chính ---
output_path = os.path.join(project_root, 'figures', '04_model_comparison_metrics.pdf')

plot_grouped_bar_chart(
    data=df,
    category_col='model_name',
    value_cols=['accuracy', 'f1_score'],
    value_labels=['Accuracy (%)', 'F1-Score (%)'],
    y_label='Performance Score (%)',
    title='AI Model Performance for Satellite Link State Prediction',
    output_path=output_path,
    # <<<<<<< SỬ DỤNG THAM SỐ MỚI
    # Bắt đầu trục Y từ 85 để làm nổi bật sự khác biệt
    ylim=(85, 97)
)

