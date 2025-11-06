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

# src/plot_templates.py
# (thêm vào cuối file)
import seaborn as sns

# ... (các hàm khác đã có ở trên) ...

def plot_heatmap(
    matrix_data,
    x_tick_labels,
    y_tick_labels,
    y_label: str,
    x_label: str,
    title: str,
    output_path: str,
    figsize: tuple = (6, 5),
    cmap: str = 'Blues',
    show_values: bool = True,
    value_format: str = 'd',
    cbar_label: str = 'Count'
):
    """
    Tạo và lưu một biểu đồ heatmap, tối ưu cho confusion matrix hoặc correlation matrix.

    Args:
        matrix_data (array-like): Dữ liệu ma trận 2D (vd: numpy array, DataFrame).
        x_tick_labels (list): Nhãn cho các cột (trục X).
        y_tick_labels (list): Nhãn cho các hàng (trục Y).
        y_label (str): Nhãn cho trục Y.
        x_label (str): Nhãn cho trục X.
        title (str): Tiêu đề biểu đồ.
        output_path (str): Đường dẫn lưu file PDF.
        figsize (tuple, optional): Kích thước figure. Mặc định là (6, 5).
        cmap (str, optional): Tên colormap. 'Blues' tốt cho confusion matrix,
                              'viridis' hoặc 'coolwarm' tốt cho correlation.
                              Mặc định là 'Blues'.
        show_values (bool, optional): Hiển thị giá trị số trong ô. Mặc định là True.
        value_format (str, optional): Định dạng cho giá trị số. 'd' cho integer,
                                      '.2f' cho float. Mặc định là 'd'.
        cbar_label (str, optional): Nhãn cho thanh màu (colorbar). Mặc định là 'Count'.
    """
    fig, ax = plt.subplots(figsize=figsize, layout='constrained')

    # Sử dụng seaborn để vẽ heatmap
    sns.heatmap(
        matrix_data,
        annot=show_values,      # Hiển thị số trong ô
        fmt=value_format,       # Định dạng của số
        cmap=cmap,              # Bảng màu
        linewidths=.5,          # Vẽ đường kẻ mảnh giữa các ô
        ax=ax,
        xticklabels=x_tick_labels,
        yticklabels=y_tick_labels,
        annot_kws={"size": 9},  # Tùy chỉnh kích thước font của số
        cbar_kws={'label': cbar_label} # Thêm nhãn cho color bar
    )

    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title(title)

    # Tối ưu hóa hiển thị của các tick labels
    # Xoay nhãn trục X một góc vừa phải để tránh chồng chéo nếu chúng dài
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right", rotation_mode="anchor")
    # Đảm bảo nhãn trục Y luôn nằm ngang
    plt.setp(ax.get_yticklabels(), rotation=0)

    # Tắt các vạch ticks nhỏ không cần thiết cho heatmap
    ax.tick_params(left=False, bottom=False)

    plt.savefig(output_path)
    print(f"Heatmap saved to: {output_path}")
    plt.close(fig)

# src/plot_templates.py
# ... (các hàm khác đã có ở trên) ...


# src/plot_templates.py
# (thay thế hàm plot_distribution cũ)

def plot_distribution(
    data: pd.Series,
    x_label: str,
    title: str,
    output_path: str,
    figsize: tuple = (6, 4),
    bins: int = 30,
    show_kde: bool = True,
    show_hist: bool = True,
    color: str = None
):
    """
    Tạo và lưu biểu đồ phân bố (histogram và/hoặc density plot - KDE).
    Lý tưởng để xem xét sự phân bố của một biến số liên tục.

    Args:
        data (pd.Series): Một chuỗi dữ liệu (một cột của DataFrame).
        x_label (str): Nhãn cho trục X.
        title (str): Tiêu đề biểu đồ.
        output_path (str): Đường dẫn lưu file PDF.
        figsize (tuple, optional): Kích thước figure. Mặc định là (6, 4).
        bins (int, optional): Số lượng "thùng" cho histogram. Mặc định là 30.
        show_kde (bool, optional): Có vẽ đường mật độ (KDE) hay không. Mặc định là True.
        show_hist (bool, optional): Có vẽ histogram hay không. Mặc định là True.
        color (str, optional): Màu sắc cho biểu đồ. Nếu None, sẽ dùng màu mặc định.
    """
    if not show_hist and not show_kde:
        print("Warning: Both show_hist and show_kde are False. No plot will be generated.")
        return

    fig, ax = plt.subplots(figsize=figsize, layout='constrained')
    
    plot_color = color if color else CONTEXT_COLORS['blue']
    
    # Logic vẽ đã được sửa lại cho chính xác
    if show_hist:
        # hist=True là mặc định, kde được điều khiển bởi tham số kde
        sns.histplot(
            data,
            bins=bins,
            kde=show_kde,
            color=plot_color,
            ax=ax
        )
    elif show_kde: # Chỉ show_kde=True, show_hist=False
        sns.kdeplot(
            data,
            color=plot_color,
            fill=True,
            alpha=0.5,
            ax=ax
        )
    
    # Đặt nhãn trục y dựa trên những gì được vẽ
    if show_hist:
        ax.set_ylabel('Frequency')
    else: # Chỉ có KDE
        ax.set_ylabel('Density')
        
    ax.set_xlabel(x_label)
    ax.set_title(title)
    
    ax.grid(axis='x', which='both', visible=False)
    ax.grid(axis='y', which='major', linestyle=':', linewidth=0.7)

    plt.savefig(output_path)
    print(f"Distribution plot saved to: {output_path}")
    plt.close(fig)
