# examples/09_contour_plot_example.py

import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Thêm thư mục src vào Python Path ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(project_root, 'src'))

# Import các hàm cần thiết
from publication_style import set_publication_style, CONTEXT_COLORS
from plot_templates import plot_contour

# --- Bước 1: Thiết lập Style chung ---
set_publication_style(font_family='sans-serif')

# --- Bước 2: Tạo dữ liệu giả (dạng điểm rời rạc) ---
# Đây là cách dữ liệu thường trông như thế nào trong thực tế
print("--- Generating sample QKD performance data ---")
np.random.seed(42)

# Các tham số đầu vào (X và Y)
# Tỷ lệ lỗi quang nội tại của hệ thống (%)
optical_error_rate = np.random.uniform(1.0, 5.0, 50) 
# Hiệu suất của bộ dò photon đơn (%)
detection_efficiency = np.random.uniform(50.0, 95.0, 50)

# Giá trị đầu ra (Z): Secret Key Rate (SKR) (kbps)
# Mô phỏng một hàm Z = f(X, Y) hợp lý: SKR giảm khi lỗi tăng, và tăng khi hiệu suất tăng
skr = (1000 * (detection_efficiency / 100)**2) / (optical_error_rate) \
      + np.random.normal(0, 10, 50)
# Đảm bảo không có giá trị âm
skr[skr < 0] = 0

# --- Bước 3: Gọi template để vẽ contour plot ---
output_path = os.path.join(project_root, 'figures', '15_qkd_skr_contour.pdf')

plot_contour(
    x_data=optical_error_rate,
    y_data=detection_efficiency,
    z_data=skr,
    x_label='Intrinsic Optical Error Rate (%)',
    y_label='Single-Photon Detector Efficiency (%)',
    title='Secret Key Rate (SKR) Landscape',
    output_path=output_path,
    cbar_label='Secret Key Rate (kbps)',
    cmap='magma', # 'magma' hoặc 'plasma' rất tốt cho dạng dữ liệu này
    show_points=True
)
