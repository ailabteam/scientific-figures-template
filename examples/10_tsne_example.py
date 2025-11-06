# examples/10_tsne_example.py

import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification # Dùng để tạo dữ liệu giả

# --- Thêm thư mục src vào Python Path ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(project_root, 'src'))

# Import các hàm cần thiết
from publication_style import set_publication_style, COLOR_PALETTE
from plot_templates import plot_tsne

# --- Bước 1: Thiết lập Style chung ---
set_publication_style(font_family='sans-serif')

# --- Bước 2: Tạo dữ liệu giả và các bộ đặc trưng "giả" ---
print("--- Generating sample features from different methods ---")

# Tạo một bộ dữ liệu gốc có 4 lớp, 64 chiều, 500 mẫu
# `class_sep` càng cao, các lớp càng dễ tách biệt
features_raw, labels_raw = make_classification(
    n_samples=500,
    n_features=64,
    n_informative=10,
    n_redundant=10,
    n_classes=4,
    n_clusters_per_class=1,
    class_sep=1.5,
    random_state=42
)

class_names = {0: 'Normal', 1: 'Congestion', 2: 'Handover', 3: 'Attack'}
labels = pd.Series(labels_raw).map(class_names)

# Phương pháp 1: Baseline (đặc trưng bị nhiễu, khó tách)
noise = np.random.normal(0, 2.0, features_raw.shape)
features_baseline = features_raw + noise

# Phương pháp 2: SOTA (đặc trưng tốt hơn)
# Giả lập bằng cách tăng khoảng cách giữa các lớp
features_sota = features_raw * 1.5

# Phương pháp 3: Our Method (đặc trưng rất tốt, tách biệt rõ ràng)
features_ours = features_raw * 2.5

# --- Bước 3: Chuẩn bị để vẽ subplot ---
fig, axes = plt.subplots(1, 3, figsize=(15, 5), layout='constrained')

# Tạo bảng màu chung cho cả 3 subplot
custom_palette = {
    'Normal': COLOR_PALETTE['blue'],
    'Congestion': COLOR_PALETTE['green'],
    'Handover': COLOR_PALETTE['orange'],
    'Attack': COLOR_PALETTE['red']
}

# --- Bước 4: Vẽ t-SNE cho từng phương pháp lên từng subplot ---

# Subplot (a): Baseline
plot_tsne(
    features=features_baseline,
    labels=labels,
    title='(a) Baseline Method (PCA)',
    output_path='', # Không cần
    palette=custom_palette,
    ax=axes[0]
)

# Subplot (b): SOTA
plot_tsne(
    features=features_sota,
    labels=labels,
    title='(b) SOTA Method (GNN)',
    output_path='',
    palette=custom_palette,
    ax=axes[1]
)

# Subplot (c): Our Method
plot_tsne(
    features=features_ours,
    labels=labels,
    title='(c) Our Proposed Method',
    output_path='',
    palette=custom_palette,
    ax=axes[2]
)

# --- Bước 5: Tinh chỉnh và Lưu toàn bộ Figure ---
handles, labels = axes[0].get_legend_handles_labels()
# Tắt legend của từng subplot
for ax in axes:
    ax.get_legend().remove()
# Thêm một legend chung cho cả figure
fig.legend(handles, labels, title='Traffic Classes', loc='center right', bbox_to_anchor=(1.08, 0.5))

final_output_path = os.path.join(project_root, 'figures', '16_tsne_feature_comparison.pdf')
plt.savefig(final_output_path)
print(f"\nComparative t-SNE plot saved to: {final_output_path}")
plt.close(fig)
