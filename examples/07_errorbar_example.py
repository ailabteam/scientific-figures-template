# examples/07_errorbar_example.py

import sys
import os
import pandas as pd

# Thêm thư mục src vào Python Path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(project_root, 'src'))

# Import các hàm cần thiết
from publication_style import set_publication_style
from plot_templates import plot_line_comparison, plot_grouped_bar_chart

# --- Bước 1: Thiết lập Style chung ---
set_publication_style(font_family='sans-serif')

# --- Ví dụ 1: Line Plot với dải lỗi (Training Curve) ---
print("--- Generating Line Plot with Error Bands ---")
df_train = pd.read_csv(os.path.join(project_root, 'data', 'sample_training_curves.csv'))

output_path_line = os.path.join(project_root, 'figures', '12_training_accuracy_with_error.pdf')
plot_line_comparison(
    data=df_train,
    x_col='epoch',
    y_cols=['accuracy_mean'],
    y_labels=['Model Accuracy'],
    x_label='Epoch',
    y_label='Accuracy',
    title='Model Training Accuracy (Mean ± SD over 5 runs)',
    output_path=output_path_line,
    y_error_cols={'accuracy_mean': 'accuracy_std'}, # Map cột mean với cột std
    ylim=(0.5, 1.0)
)

# --- Ví dụ 2: Bar Chart với thanh lỗi (Final Performance) ---
print("\n--- Generating Bar Chart with Error Bars ---")
# Sử dụng lại dữ liệu từ ví dụ 03, thêm cột lỗi
df_perf = pd.read_csv(os.path.join(project_root, 'data', 'sample_model_performance.csv'))
# Thêm dữ liệu lỗi giả (SEM)
df_perf['accuracy_sem'] = [1.2, 0.9, 0.5]
df_perf['f1_score_sem'] = [1.1, 1.0, 0.6]

output_path_bar = os.path.join(project_root, 'figures', '13_model_perf_with_error.pdf')
plot_grouped_bar_chart(
    data=df_perf,
    category_col='model_name',
    value_cols=['accuracy', 'f1_score'],
    value_labels=['Accuracy (%)', 'F1-Score (%)'],
    error_cols=['accuracy_sem', 'f1_score_sem'], # Truyền vào cột lỗi
    y_label='Performance Score (%)',
    title='Final Model Performance (Mean ± SEM)',
    output_path=output_path_bar,
    ylim=(80, 100)
)
