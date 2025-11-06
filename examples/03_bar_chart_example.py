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
    # Tùy chỉnh màu sắc để làm nổi bật phương pháp của chúng ta
    # (Giả sử thứ tự trong CSV là Baseline, SOTA, Our Method)
    colors=[CONTEXT_COLORS['gray'], CONTEXT_COLORS['blue'], CONTEXT_COLORS['red']]
)

# LƯU Ý: Nếu dữ liệu có thứ tự khác, bạn cần sắp xếp lại DataFrame
# hoặc điều chỉnh lại thứ tự màu cho phù hợp.
# Ví dụ: df = df.set_index('model_name').loc[['Baseline (SVM)', 'SOTA (GNN)', 'Our Method (Q-GNN)']].reset_index()
