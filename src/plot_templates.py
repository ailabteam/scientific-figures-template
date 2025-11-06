# src/plot_templates.py

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from publication_style import CONTEXT_COLORS, COLOR_PALETTE

def plot_line_comparison(
    data: pd.DataFrame,
    x_col: str,
    y_cols: list,
    y_labels: list,
    x_label: str,
    y_label: str,
    title: str,
    output_path: str,
    figsize: tuple = (6, 4),
    **kwargs
):
    """
    Tạo và lưu một biểu đồ đường (line plot) để so sánh hiệu năng.
    ... (docstring) ...
    """
    if len(y_cols) != len(y_labels):
        raise ValueError("Số lượng cột Y và nhãn Y phải bằng nhau.")

    fig, ax = plt.subplots(figsize=figsize)

    linestyles = kwargs.get('linestyles', ['-', '--', ':', '-.'])
    markers = kwargs.get('markers', ['o', 's', '^', 'D'])
    colors = kwargs.get('colors', [
        CONTEXT_COLORS.get('proposed'),
        CONTEXT_COLORS.get('sota'),
        CONTEXT_COLORS.get('baseline'),
        CONTEXT_COLORS.get('method_A'),
        CONTEXT_COLORS.get('method_B')
    ])

    for i, y_col in enumerate(y_cols):
        style_idx = i % len(linestyles)
        marker_idx = i % len(markers)
        color_idx = i % len(colors)

        linewidth = 2.0 if i == 0 else 1.5

        ax.plot(
            data[x_col],
            data[y_col],
            label=y_labels[i],
            color=colors[color_idx],
            linestyle=linestyles[style_idx],
            marker=markers[marker_idx],
            markevery=10,
            linewidth=linewidth
        )

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()

    if 'xlim' in kwargs:
        ax.set_xlim(kwargs['xlim'])
    if 'ylim' in kwargs:
        ax.set_ylim(kwargs['ylim'])
    if 'yscale' in kwargs:
        ax.set_yscale(kwargs['yscale'])

    plt.savefig(output_path)
    print(f"Line plot saved to: {output_path}")
    plt.close(fig)


# src/plot_templates.py
# ... (các import và hàm plot_line_comparison) ...

def plot_grouped_bar_chart(
    data: pd.DataFrame,
    category_col: str,
    value_cols: list,
    value_labels: list,
    y_label: str,
    title: str,
    output_path: str,
    figsize: tuple = (7, 5),
    # <<<<<<< THÊM THAM SỐ MỚI
    ylim: tuple = None, 
    **kwargs
):
    """
    Tạo và lưu một biểu đồ cột nhóm (grouped bar chart).
    ... (docstring cập nhật) ...
    Args:
        ...
        ylim (tuple, optional): Giới hạn cho trục Y, ví dụ (0, 100). 
                                Nếu là None, sẽ tự động tính toán. Mặc định là None.
        ...
    """
    # ... (code kiểm tra len và lấy categories vẫn như cũ) ...
    if len(value_cols) != len(value_labels):
        raise ValueError("Số lượng cột giá trị và nhãn giá trị phải bằng nhau.")

    categories = data[category_col]
    n_categories = len(categories)
    n_values = len(value_cols)

    x = np.arange(n_categories)
    
    total_width = 0.8
    width = total_width / n_values
    
    fig, ax = plt.subplots(figsize=figsize, layout='constrained')

    colors = kwargs.get('colors', [COLOR_PALETTE[c] for c in ['blue', 'green', 'orange', 'purple']])

    for i, value_col in enumerate(value_cols):
        offset = width * (i - (n_values - 1) / 2)
        measurements = data[value_col]
        
        rects = ax.bar(x + offset, measurements, width, 
                       label=value_labels[i], color=colors[i % len(colors)])
        
        ax.bar_label(rects, padding=3, fmt='%.2f', fontsize=8)

    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.set_xticks(x, categories)
    ax.legend(title='Metrics')

    # <<<<<<< THAY ĐỔI LOGIC XỬ LÝ YLIM
    if ylim:
        ax.set_ylim(ylim)
    else:
        # Logic tự động: bắt đầu từ 0 và thêm 15% không gian ở trên
        y_max = data[value_cols].max().max()
        ax.set_ylim(0, y_max * 1.15)
    # <<<<<<< KẾT THÚC THAY ĐỔI
    
    ax.grid(axis='x', which='both', visible=False)
    ax.grid(axis='y', which='major', linestyle=':', linewidth=0.7)

    plt.savefig(output_path)
    print(f"Grouped bar chart saved to: {output_path}")
    plt.close(fig)
