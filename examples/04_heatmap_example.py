# examples/04_heatmap_example.py

import sys
import os
import numpy as np
from sklearn.metrics import confusion_matrix
import pandas as pd # Dùng pandas để chuẩn bị dữ liệu cho ví dụ 2

# Thêm thư mục src vào Python Path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(project_root, 'src'))

# Import các hàm cần thiết
from publication_style import set_publication_style
from plot_templates import plot_heatmap

# --- Bước 1: Thiết lập Style chung ---
set_publication_style(font_family='sans-serif')

# --- Ví dụ 1: Ma trận nhầm lẫn (Confusion Matrix) ---
print("--- Generating Confusion Matrix ---")

# Dữ liệu giả: Phân loại 4 loại lưu lượng mạng trong SAGIN
class_names = ['Normal', 'Congestion', 'QKD Handover', 'Attack']

# Dữ liệu thực tế (ground truth) và dữ liệu dự đoán của mô hình
y_true = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3])
y_pred = np.array([0, 0, 1, 0, 1, 1, 1, 3, 1, 2, 2, 2, 3, 3, 1, 3, 3])

# Tạo confusion matrix bằng scikit-learn
cm = confusion_matrix(y_true, y_pred)

# Gọi template để vẽ
output_path_cm = os.path.join(project_root, 'figures', '05_confusion_matrix.pdf')
plot_heatmap(
    matrix_data=cm,
    x_tick_labels=class_names,
    y_tick_labels=class_names,
    y_label='True Traffic Type',
    x_label='Predicted Traffic Type',
    title='Confusion Matrix for SAGIN Traffic Classification',
    output_path=output_path_cm,
    cbar_label='Number of Samples'
)

# --- Ví dụ 2: Ma trận tương quan (Correlation Matrix) ---
print("\n--- Generating Correlation Matrix ---")

# Tạo dữ liệu giả với các đặc trưng có ý nghĩa
np.random.seed(42)
data = {
    'SNR (dB)': np.random.uniform(5, 20, 100),
    'QBER (%)': np.random.uniform(0.1, 5, 100),
    'Latency (ms)': np.random.uniform(50, 200, 100),
    'Altitude (km)': np.random.uniform(400, 800, 100)
}
df = pd.DataFrame(data)
# Tạo ra một vài mối tương quan nhân tạo để heatmap có ý nghĩa
df['Throughput (Mbps)'] = 2 * df['SNR (dB)'] - 0.5 * df['Latency (ms)'] + np.random.normal(0, 5, 100)
df['QBER (%)'] = 10 / df['SNR (dB)'] + np.random.normal(0, 0.2, 100)

# Tính toán ma trận tương quan
corr_matrix = df.corr()
feature_names = corr_matrix.columns

# Gọi template để vẽ
output_path_corr = os.path.join(project_root, 'figures', '06_correlation_matrix.pdf')
plot_heatmap(
    matrix_data=corr_matrix,
    x_tick_labels=feature_names,
    y_tick_labels=feature_names,
    y_label='Features',
    x_label='Features',
    title='Feature Correlation Matrix',
    output_path=output_path_corr,
    cmap='viridis',    # 'viridis' là một lựa chọn tốt cho dữ liệu liên tục
    value_format='.2f',  # Hiển thị 2 chữ số thập phân
    cbar_label='Pearson Correlation Coefficient'
)
