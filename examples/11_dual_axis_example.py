# examples/11_dual_axis_example.py

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
from plot_templates import plot_dual_axis

# --- Bước 1: Thiết lập Style chung ---
set_publication_style(font_family='sans-serif')

# --- Bước 2: Tạo dữ liệu giả ---
print("--- Generating sample network performance data ---")

# Trục X: Tải trọng mạng từ 10% đến 100%
network_load = np.linspace(10, 100, 20)

# Trục Y1: Thông lượng (Mbps) - tăng theo tải trọng nhưng sau đó bão hòa
throughput = -0.05 * (network_load - 80)**2 + 100
throughput[throughput < 10] = 10 + np.random.uniform(-2, 2, len(throughput[throughput < 10]))
throughput[throughput > 98] = 98 + np.random.uniform(-2, 2, len(throughput[throughput > 98]))

# Trục Y2: Độ trễ (ms) - tăng rất nhanh khi mạng gần bão hòa
latency = 20 * np.exp(0.05 * network_load)

df = pd.DataFrame({
    'load': network_load,
    'throughput': throughput,
    'latency': latency
})

# --- Bước 3: Gọi template để vẽ ---
output_path = os.path.join(project_root, 'figures', '17_throughput_vs_latency.pdf')

plot_dual_axis(
    # Dữ liệu
    x_data=df['load'],
    y1_data=df['throughput'],
    y2_data=df['latency'],
    
    # Nhãn và màu cho trục Y1 (trái)
    y1_label='Throughput (Mbps)',
    y1_color=CONTEXT_COLORS['blue'],

    # Nhãn và màu cho trục Y2 (phải)
    y2_label='Latency (ms)',
    y2_color=CONTEXT_COLORS['red'],

    # Thông tin chung
    x_label='Network Load (%)',
    title='Network Throughput vs. Latency Trade-off',
    output_path=output_path,

    # Tùy chỉnh thêm style cho từng đường
    y1_style={'marker': 'o', 'markersize': 5},
    y2_style={'marker': 's', 'markersize': 5, 'linestyle': '--'}
)
