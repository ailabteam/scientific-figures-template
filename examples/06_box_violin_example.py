# examples/06_box_violin_example.py

import sys
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Thêm thư mục src vào Python Path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(project_root, 'src'))

# Import các hàm cần thiết
from publication_style import set_publication_style, CONTEXT_COLORS
from plot_templates import plot_distribution_comparison

# --- Bước 1: Thiết lập Style chung ---
set_publication_style(font_family='sans-serif')

# --- Bước 2: Tạo dữ liệu giả ở dạng "long-form" ---
print("--- Preparing comparative performance data ---")
np.random.seed(42)
scenarios = ['Low Congestion', 'Medium Congestion', 'High Congestion']
algorithms = ['Baseline', 'Our Method']
data_list = []

for scenario in scenarios:
    for algorithm in algorithms:
        # Giả lập hiệu năng
        if algorithm == 'Baseline':
            if scenario == 'Low Congestion':
                mean_throughput = 100
                std_dev = 10
            elif scenario == 'Medium Congestion':
                mean_throughput = 70
                std_dev = 15
            else: # High Congestion
                mean_throughput = 40
                std_dev = 20
        else: # Our Method
            if scenario == 'Low Congestion':
                mean_throughput = 105
                std_dev = 8
            elif scenario == 'Medium Congestion':
                mean_throughput = 90
                std_dev = 10
            else: # High Congestion
                mean_throughput = 80
                std_dev = 12
        
        # Tạo 100 mẫu dữ liệu cho mỗi cặp (scenario, algorithm)
        samples = np.random.normal(mean_throughput, std_dev, 100)
        for s in samples:
            data_list.append({'Scenario': scenario, 'Algorithm': algorithm, 'Throughput (Mbps)': s})

df = pd.DataFrame(data_list)

# --- Bước 3: Vẽ Violin Plot ---
print("--- Generating Violin Plot ---")
output_path_violin = os.path.join(project_root, 'figures', '10_throughput_violin_comparison.pdf')

# Tạo một palette màu tùy chỉnh
custom_palette = {"Baseline": CONTEXT_COLORS['gray'], "Our Method": CONTEXT_COLORS['red']}

# Đây là một cách vẽ nâng cao hơn, dùng hue để phân biệt thuật toán
fig, ax = plt.subplots(figsize=(8, 5), layout='constrained')
sns.violinplot(data=df, x='Scenario', y='Throughput (Mbps)', hue='Algorithm',
               split=True, inner="quart", palette=custom_palette, ax=ax)
ax.set_ylabel('Throughput (Mbps)')
ax.set_xlabel('Network Scenario')
ax.set_title('Throughput Performance Comparison Across Scenarios')
ax.grid(axis='x', which='both', visible=False)
ax.grid(axis='y', which='major', linestyle=':', linewidth=0.7)
plt.savefig(output_path_violin)
print(f"Violin plot saved to: {output_path_violin}")
plt.close(fig)

# --- Bước 4: Vẽ Box Plot (sử dụng template) ---
print("\n--- Generating Box Plot ---")
# Để dùng template, chúng ta cần một cột gộp cả scenario và algorithm
df['Experiment'] = df['Scenario'] + "\n" + df['Algorithm']

output_path_box = os.path.join(project_root, 'figures', '11_throughput_box_comparison.pdf')

plot_distribution_comparison(
    data=df.sort_values(by=['Scenario', 'Algorithm']), # Sắp xếp để các nhóm gần nhau
    x_col='Experiment',
    y_col='Throughput (Mbps)',
    y_label='Throughput (Mbps)',
    x_label='Experiment Condition',
    title='Throughput Performance Comparison Across Scenarios',
    output_path=output_path_box,
    plot_type='box'
)
