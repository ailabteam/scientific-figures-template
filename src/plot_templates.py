# src/plot_templates.py

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from publication_style import CONTEXT_COLORS, COLOR_PALETTE

# src/plot_templates.py
# (sửa lại hàm plot_line_comparison)

def plot_line_comparison(
    data: pd.DataFrame,
    x_col: str,
    y_cols: list,
    y_labels: list,
    x_label: str,
    y_label: str,
    title: str,
    output_path: str,
    # <<<<<<< THÊM THAM SỐ MỚI
    y_error_cols: dict = None,
    figsize: tuple = (6, 4),
    **kwargs
):
    """
    Tạo và lưu một biểu đồ đường để so sánh hiệu năng, có thể kèm dải lỗi.

    Args:
        ... (các tham số cũ) ...
        y_error_cols (dict, optional): Dict để map cột y với cột chứa giá trị lỗi.
                                       Giá trị lỗi này là bán kính của dải lỗi (vd: SD).
                                       Ví dụ: {'our_method': 'our_method_std'}.
                                       Mặc định là None.
        ...
    """
    if len(y_cols) != len(y_labels):
        raise ValueError("Số lượng cột Y và nhãn Y phải bằng nhau.")

    fig, ax = plt.subplots(figsize=figsize, layout='constrained')

    linestyles = kwargs.get('linestyles', ['-', '--', ':', '-.'])
    markers = kwargs.get('markers', ['o', 's', '^', 'D'])
    colors = kwargs.get('colors', [CONTEXT_COLORS.get(c) for c in ['proposed', 'sota', 'baseline', 'method_A']])

    for i, y_col in enumerate(y_cols):
        style_idx = i % len(linestyles)
        marker_idx = i % len(markers)
        color = colors[i % len(colors)]
        
        linewidth = 2.0 if i == 0 else 1.5
        
        # Lấy dữ liệu
        x_data = data[x_col]
        y_data = data[y_col]
        
        # Vẽ đường trung tâm
        ax.plot(
            x_data, y_data, label=y_labels[i], color=color,
            linestyle=linestyles[style_idx], marker=markers[marker_idx],
            markevery=10, linewidth=linewidth, zorder=i+2 # zorder để đường kẻ nổi lên trên dải màu
        )
        
        # <<<<<<< THÊM LOGIC VẼ DẢI LỖI
        if y_error_cols and y_col in y_error_cols:
            error_col = y_error_cols[y_col]
            y_error = data[error_col]
            ax.fill_between(
                x_data, y_data - y_error, y_data + y_error,
                color=color, alpha=0.2, zorder=i+1 # alpha để dải màu trong suốt
            )

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()
    
    if 'xlim' in kwargs: ax.set_xlim(kwargs['xlim'])
    if 'ylim' in kwargs: ax.set_ylim(kwargs['ylim'])
    if 'yscale' in kwargs: ax.set_yscale(kwargs['yscale'])

    plt.savefig(output_path)
    print(f"Line plot with error bands saved to: {output_path}")
    plt.close(fig)


# src/plot_templates.py
# ... (các import và hàm plot_line_comparison) ...

# src/plot_templates.py
# (sửa lại hàm plot_grouped_bar_chart)
def plot_grouped_bar_chart(
    data: pd.DataFrame,
    category_col: str,
    value_cols: list,
    value_labels: list,
    y_label: str,
    title: str,
    output_path: str,
    # <<<<<<< THÊM THAM SỐ MỚI
    error_cols: list = None,
    figsize: tuple = (7, 5),
    ylim: tuple = None, 
    **kwargs
):
    """
    ... (docstring) ...
    Args:
        ...
        error_cols (list, optional): Danh sách tên các cột chứa giá trị lỗi (vd: SD, SEM).
                                     Thứ tự phải tương ứng với value_cols.
                                     Nếu None, sẽ không vẽ thanh lỗi. Mặc định là None.
        ...
    """
    # ... (code kiểm tra và chuẩn bị) ...
    if len(value_cols) != len(value_labels):
        raise ValueError(...)
    if error_cols and len(value_cols) != len(error_cols):
        raise ValueError("Số lượng cột giá trị và cột lỗi phải bằng nhau.")

    # ... (code tính toán vị trí) ...
    categories = data[category_col]
    n_categories = len(categories)
    n_values = len(value_cols)
    x = np.arange(n_categories)
    total_width = 0.8
    width = total_width / n_values
    
    fig, ax = plt.subplots(figsize=figsize, layout='constrained')
    colors = kwargs.get('colors', [COLOR_PALETTE.get(c) for c in ['blue', 'green', 'orange']])

    for i, value_col in enumerate(value_cols):
        offset = width * (i - (n_values - 1) / 2)
        measurements = data[value_col]
        
        # <<<<<<< THÊM LOGIC LẤY DỮ LIỆU LỖI
        y_error = data[error_cols[i]] if error_cols else None
        
        rects = ax.bar(
            x + offset, measurements, width, 
            label=value_labels[i], color=colors[i % len(colors)],
            yerr=y_error, # Tham số để vẽ error bar
            capsize=3     # Thêm gạch ngang ở đầu/cuối error bar
        )
        
        ax.bar_label(rects, padding=3, fmt='%.2f', fontsize=8)

    # ... (code còn lại của hàm giữ nguyên) ...
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.set_xticks(x, categories)
    ax.legend(title='Metrics')

    if ylim:
        ax.set_ylim(ylim)
    else:
        # Cập nhật logic tự động để tính cả error bar
        y_max_val = data[value_cols].max().max()
        if error_cols:
            y_max_err = (data[value_cols] + data[error_cols]).max().max()
            y_max = max(y_max_val, y_max_err)
        else:
            y_max = y_max_val
        ax.set_ylim(0, y_max * 1.15)
        
    ax.grid(axis='x', which='both', visible=False)
    ax.grid(axis='y', which='major', linestyle=':', linewidth=0.7)

    plt.savefig(output_path)
    print(f"Grouped bar chart with error bars saved to: {output_path}")
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

# src/plot_templates.py
# (thêm vào cuối file)

def plot_distribution_comparison(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    y_label: str,
    x_label: str,
    title: str,
    output_path: str,
    plot_type: str = 'violin',
    figsize: tuple = (8, 5),
    palette: dict = None
):
    """
    Tạo và lưu biểu đồ so sánh phân bố (Violin hoặc Box Plot).
    Lý tưởng để so sánh phân bố của một biến số qua nhiều nhóm.

    Args:
        data (pd.DataFrame): DataFrame ở dạng "long-form" chứa dữ liệu.
        x_col (str): Tên cột chứa các nhóm/hạng mục.
        y_col (str): Tên cột chứa giá trị số liên tục.
        y_label (str): Nhãn cho trục Y.
        x_label (str): Nhãn cho trục X.
        title (str): Tiêu đề biểu đồ.
        output_path (str): Đường dẫn lưu file PDF.
        plot_type (str, optional): Loại biểu đồ, 'violin' hoặc 'box'.
                                   Mặc định là 'violin'.
        figsize (tuple, optional): Kích thước figure. Mặc định là (8, 5).
        palette (dict, optional): Dictionary map tên hạng mục với màu sắc.
                                  Ví dụ: {'Baseline': 'gray', 'Our Method': 'red'}.
                                  Mặc định là None.
    """
    fig, ax = plt.subplots(figsize=figsize, layout='constrained')

    plot_func = None
    if plot_type == 'violin':
        plot_func = sns.violinplot
    elif plot_type == 'box':
        plot_func = sns.boxplot
    else:
        raise ValueError(f"plot_type phải là 'violin' hoặc 'box', nhận được '{plot_type}'")

    # Vẽ biểu đồ chính
    plot_func(
        x=x_col,
        y=y_col,
        data=data,
        palette=palette,
        ax=ax
    )

    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title(title)

    # Tinh chỉnh cho đẹp hơn
    # Xoay nhãn trục X nếu có nhiều nhóm và tên dài
    if len(data[x_col].unique()) > 4:
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right", rotation_mode="anchor")

    ax.grid(axis='x', which='both', visible=False)
    ax.grid(axis='y', which='major', linestyle=':', linewidth=0.7)

    plt.savefig(output_path)
    print(f"{plot_type.capitalize()} plot saved to: {output_path}")
    plt.close(fig)

