# examples/05_distribution_plot_example.py

import sys
import os
import numpy as np
import pandas as pd
import seaborn as sns # <<<<<<< THÊM DÒNG NÀY

# Thêm thư mục src vào Python Path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(project_root, 'src'))

# Import các hàm cần thiết
from publication_style import set_publication_style, CONTEXT_COLORS
from plot_templates import plot_distribution
import matplotlib.pyplot as plt # Import thêm plt để vẽ so sánh

# --- Bước 1: Thiết lập Style chung ---
set_publication_style(font_family='sans-serif')

# --- Bước 2: Tạo dữ liệu giả ---
# Dữ liệu mô phỏng độ trễ (ms) cho hai thuật toán
np.random.seed(42)
# Thuật toán baseline: độ trễ trung bình cao hơn và có phương sai lớn hơn
latency_baseline = np.random.normal(loc=120, scale=30, size=1000)
# Thêm một vài giá trị ngoại lệ (đuôi dài)
latency_baseline = np.append(latency_baseline, np.random.uniform(200, 400, 20))

# Thuật toán của chúng ta: độ trễ trung bình thấp hơn và ổn định hơn
latency_proposed = np.random.normal(loc=80, scale=15, size=1000)

# --- Bước 3: Vẽ phân bố cho từng thuật toán riêng lẻ ---
print("--- Generating individual distribution plots ---")

# Vẽ cho baseline
output_path_base = os.path.join(project_root, 'figures', '07_latency_dist_baseline.pdf')
plot_distribution(
    data=pd.Series(latency_baseline),
    x_label='End-to-end Latency (ms)',
    title='Latency Distribution (Baseline Algorithm)',
    output_path=output_path_base,
    color=CONTEXT_COLORS['gray']
)

# Vẽ cho phương pháp đề xuất
output_path_prop = os.path.join(project_root, 'figures', '08_latency_dist_proposed.pdf')
plot_distribution(
    data=pd.Series(latency_proposed),
    x_label='End-to-end Latency (ms)',
    title='Latency Distribution (Our Proposed Algorithm)',
    output_path=output_path_prop,
    color=CONTEXT_COLORS['red']
)

# --- Bước 4: So sánh hai phân bố trên cùng một biểu đồ (CÁCH LÀM TỐT NHẤT) ---
print("\n--- Generating comparative distribution plot ---")
fig, ax = plt.subplots(figsize=(7, 5), layout='constrained')

# Chỉ vẽ đường KDE để so sánh hình dạng phân bố một cách rõ ràng
sns.kdeplot(latency_baseline, fill=True, alpha=0.5, label='Baseline Algorithm', color=CONTEXT_COLORS['gray'], ax=ax)
sns.kdeplot(latency_proposed, fill=True, alpha=0.7, label='Our Proposed Algorithm', color=CONTEXT_COLORS['red'], ax=ax)

ax.set_xlabel('End-to-end Latency (ms)')
ax.set_ylabel('Density')
ax.set_title('Comparison of Latency Distributions')
ax.legend()
ax.grid(axis='x', which='both', visible=False)
ax.grid(axis='y', which='major', linestyle=':', linewidth=0.7)

output_path_comp = os.path.join(project_root, 'figures', '09_latency_dist_comparison.pdf')
plt.savefig(output_path_comp)
print(f"Comparative distribution plot saved to: {output_path_comp}")
plt.close(fig)
