# examples/08_subplots_example.py

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

# --- Thêm thư mục src vào Python Path ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(project_root, 'src'))

# Import các hàm cần thiết
from publication_style import set_publication_style, CONTEXT_COLORS
from plot_templates import plot_line_comparison # Chỉ cần import hàm này

# --- Bước 1: Thiết lập Style chung ---
set_publication_style(font_family='sans-serif')

# --- Bước 2: Chuẩn bị dữ liệu ---
df_train = pd.read_csv(os.path.join(project_root, 'data', 'sample_training_curves.csv'))

# --- Bước 3: Tạo Figure và Grid các Subplots ---
# Tạo một figure chứa 1 hàng, 2 cột các subplots.
# `sharey=False` vì Accuracy và Loss có thang đo khác nhau.
# `figsize` giờ là cho toàn bộ figure.
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), sharey=False, layout='constrained')

# --- Bước 4: Vẽ lên từng Subplot bằng cách truyền `ax` vào template ---

# Vẽ biểu đồ Accuracy lên subplot đầu tiên (ax1)
plot_line_comparison(
    ax=ax1, # <--- Truyền vào subplot axis
    data=df_train,
    x_col='epoch',
    y_cols=['train_acc_mean', 'val_acc_mean'],
    y_labels=['Training', 'Validation'],
    x_label='Epoch',
    y_label='Accuracy',
    title='(a) Model Accuracy', # Thêm label (a), (b) vào title
    output_path='', # Không cần output_path vì chúng ta sẽ tự lưu
    y_error_cols={'train_acc_mean': 'train_acc_std', 'val_acc_mean': 'val_acc_std'},
    ylim=(0.5, 1.01),
    colors=[CONTEXT_COLORS['blue'], CONTEXT_COLORS['green']],
    linestyles=['-', '--']
)

# Vẽ biểu đồ Loss lên subplot thứ hai (ax2)
plot_line_comparison(
    ax=ax2, # <--- Truyền vào subplot axis
    data=df_train,
    x_col='epoch',
    y_cols=['train_loss_mean', 'val_loss_mean'],
    y_labels=['Training', 'Validation'],
    x_label='Epoch',
    y_label='Loss',
    title='(b) Model Loss',
    output_path='', # Không cần
    y_error_cols={'train_loss_mean': 'train_loss_std', 'val_loss_mean': 'val_loss_std'},
    colors=[CONTEXT_COLORS['blue'], CONTEXT_COLORS['green']],
    linestyles=['-', '--']
)

# --- Bước 5: Tinh chỉnh và Lưu toàn bộ Figure ---
# Thêm một tiêu đề chung cho cả figure (tùy chọn)
# fig.suptitle('Model Training Performance', fontsize=14)

# Lưu figure
final_output_path = os.path.join(project_root, 'figures', '14_combined_training_curves.pdf')
plt.savefig(final_output_path)
print(f"\nSubplots figure saved to: {final_output_path}")
plt.close(fig)
