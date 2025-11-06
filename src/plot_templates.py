# src/plot_templates.py (VERSION 2 - SUBPLOT ENABLED)

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from publication_style import CONTEXT_COLORS, COLOR_PALETTE

# src/plot_templates.py
# (thêm vào cuối file)

def plot_stacked_bar_chart(
    data: pd.DataFrame,
    category_col: str,
    component_cols: list,
    y_label: str,
    title: str,

    output_path: str,
    is_100_percent: bool = False,
    figsize: tuple = (8, 6),
    palette: dict = None,
    ax=None
):
    """
    Tạo và lưu biểu đồ cột xếp chồng (stacked bar chart).

    Args:
        data (pd.DataFrame): DataFrame chứa dữ liệu.
        category_col (str): Tên cột chứa các hạng mục chính trên trục X.
        component_cols (list): Danh sách tên các cột chứa giá trị của các thành phần.
        y_label (str): Nhãn cho trục Y.
        title (str): Tiêu đề biểu đồ.
        output_path (str): Đường dẫn lưu file.
        is_100_percent (bool, optional): Nếu True, vẽ biểu đồ 100% stacked. 
                                         Mặc định là False.
        figsize (tuple, optional): Kích thước figure.
        palette (dict, optional): Dictionary map tên thành phần với màu sắc.
        ax (matplotlib.axes.Axes, optional): Subplot axis để vẽ lên.
    """
    fig, ax, save_and_close = _setup_ax_and_save(ax, figsize, output_path)

    # Chuẩn bị dữ liệu
    df_plot = data.set_index(category_col)[component_cols]

    if is_100_percent:
        # Chuẩn hóa mỗi hàng để có tổng là 100
        df_plot = df_plot.div(df_plot.sum(axis=1), axis=0) * 100
        y_label = f"{y_label} (%)" # Tự động cập nhật nhãn Y

    # Lấy bảng màu
    if palette is None:
        colors = [COLOR_PALETTE[c] for c in ['blue', 'green', 'orange', 'red', 'purple']]
        palette = {col: colors[i % len(colors)] for i, col in enumerate(component_cols)}
    
    # Vẽ biểu đồ bằng pandas' plotting, nó xử lý việc xếp chồng rất tốt
    df_plot.plot(
        kind='bar',
        stacked=True,
        color=[palette.get(col) for col in component_cols],
        ax=ax,
        width=0.8 # Làm cho các cột rộng hơn một chút
    )
    
    # --- Tinh chỉnh ---
    ax.set_ylabel(y_label)
    ax.set_xlabel(category_col) # Tự động lấy tên cột làm nhãn X
    ax.set_title(title)
    
    # Xoay nhãn trục X để dễ đọc
    plt.setp(ax.get_xticklabels(), rotation=0, ha="center")
    
    # Di chuyển legend ra ngoài biểu đồ để không che mất dữ liệu
    ax.legend(title='Components', bbox_to_anchor=(1.02, 1), loc='upper left')

    ax.grid(axis='x', which='both', visible=False)
    ax.grid(axis='y', which='major', linestyle=':', linewidth=0.7)

    if save_and_close:
        plt.savefig(output_path)
        print(f"Stacked bar chart saved to: {output_path}")
        plt.close(fig)

    return ax

# src/plot_templates.py
# (thêm vào cuối file)

def plot_dual_axis(
    # Dữ liệu cho trục Y1 (trái)
    x_data,
    y1_data,
    y1_label: str,
    y1_color: str,
    # Dữ liệu cho trục Y2 (phải)
    y2_data,
    y2_label: str,
    y2_color: str,
    # Các thông tin chung
    x_label: str,
    title: str,
    output_path: str,
    figsize: tuple = (7, 5),
    y1_style: dict = None,
    y2_style: dict = None,
    ax=None
):
    """
    Tạo và lưu biểu đồ với hai trục Y.
    Lý tưởng để so sánh hai biến có thang đo khác nhau trên cùng một trục X.

    Args:
        x_data (array-like): Dữ liệu cho trục X.
        y1_data (array-like): Dữ liệu cho trục Y bên trái.
        y1_label (str): Nhãn cho trục Y bên trái.
        y1_color (str): Màu cho trục và đường dữ liệu Y1.
        y2_data (array-like): Dữ liệu cho trục Y bên phải.
        y2_label (str): Nhãn cho trục Y bên phải.
        y2_color (str): Màu cho trục và đường dữ liệu Y2.
        x_label (str): Nhãn cho trục X.
        title (str): Tiêu đề biểu đồ.
        output_path (str): Đường dẫn lưu file.
        figsize (tuple, optional): Kích thước figure.
        y1_style (dict, optional): Dict chứa các kwargs cho plot Y1 (vd: linestyle, marker).
        y2_style (dict, optional): Dict chứa các kwargs cho plot Y2.
        ax (matplotlib.axes.Axes, optional): Subplot axis để vẽ lên.
    """
    fig, ax1, save_and_close = _setup_ax_and_save(ax, figsize, output_path)

    # Đảm bảo các dict style tồn tại
    if y1_style is None: y1_style = {}
    if y2_style is None: y2_style = {}

    # --- Vẽ trục Y1 (bên trái) ---
    # Đặt các style mặc định nếu không được cung cấp
    y1_style.setdefault('linestyle', '-')
    y1_style.setdefault('marker', 'o')
    
    line1, = ax1.plot(x_data, y1_data, color=y1_color, label=y1_label, **y1_style)
    
    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y1_label, color=y1_color)
    ax1.tick_params(axis='y', labelcolor=y1_color)
    
    # --- Tạo và vẽ trục Y2 (bên phải) ---
    ax2 = ax1.twinx()  # Tạo một trục Y mới chia sẻ cùng trục X
    
    # Đặt các style mặc định
    y2_style.setdefault('linestyle', '--')
    y2_style.setdefault('marker', 's')
    
    line2, = ax2.plot(x_data, y2_data, color=y2_color, label=y2_label, **y2_style)

    ax2.set_ylabel(y2_label, color=y2_color)
    ax2.tick_params(axis='y', labelcolor=y2_color)

    # --- Tinh chỉnh chung ---
    ax1.set_title(title)
    
    # Gộp legend từ cả hai trục vào một chỗ
    lines = [line1, line2]
    ax1.legend(lines, [l.get_label() for l in lines], loc='upper left')

    # Bật lưới cho trục chính (Y1)
    ax1.grid(axis='y', which='major', linestyle=':', linewidth=0.7)
    # Tắt lưới của trục phụ để tránh rối
    ax2.grid(False)

    if save_and_close:
        plt.savefig(output_path)
        print(f"Dual-axis plot saved to: {output_path}")
        plt.close(fig)

    return ax1, ax2

# src/plot_templates.py
# (thêm vào cuối file)
from sklearn.manifold import TSNE

def plot_tsne(
    features,
    labels,
    title: str,
    output_path: str,
    palette: dict = None,
    figsize: tuple = (6, 6),
    perplexity: float = 30.0,
    ax=None,
    **kwargs
):
    """
    Thực hiện t-SNE và vẽ kết quả lên một scatter plot.

    Args:
        features (np.array): Mảng 2D chứa các vector đặc trưng (n_samples, n_features).
        labels (array-like): Nhãn (ground truth) của mỗi mẫu.
        title (str): Tiêu đề cho subplot.
        output_path (str): Đường dẫn lưu file (chỉ dùng khi ax=None).
        palette (dict, optional): Dictionary map nhãn với màu sắc.
        figsize (tuple, optional): Kích thước figure. Mặc định là (6, 6) (hình vuông).
        perplexity (float, optional): Tham số perplexity cho t-SNE. Mặc định là 30.0.
        ax (matplotlib.axes.Axes, optional): Subplot axis để vẽ lên.
        **kwargs: Các tham số khác cho plt.scatter (vd: s - kích thước điểm).
    """
    fig, ax, save_and_close = _setup_ax_and_save(ax, figsize, output_path)

    # --- Bước 1: Chạy thuật toán t-SNE ---
    print(f"Running t-SNE for '{title}' with perplexity={perplexity}...")
    tsne = TSNE(n_components=2, perplexity=perplexity, random_state=42, init='pca', learning_rate='auto')
    features_2d = tsne.fit_transform(features)
    
    # Tạo DataFrame để dễ dàng vẽ với Seaborn
    df_tsne = pd.DataFrame({
        't-SNE-1': features_2d[:, 0],
        't-SNE-2': features_2d[:, 1],
        'label': labels
    })

    # --- Bước 2: Vẽ Scatter Plot ---
    # Lấy danh sách các lớp duy nhất để đảm bảo thứ tự nhất quán
    unique_labels = sorted(df_tsne['label'].unique())
    
    # Lấy bảng màu
    if palette is None:
        colors = [COLOR_PALETTE[c] for c in ['blue', 'green', 'orange', 'purple', 'red', 'olive']]
        palette = {label: colors[i % len(colors)] for i, label in enumerate(unique_labels)}

    sns.scatterplot(
        data=df_tsne,
        x='t-SNE-1',
        y='t-SNE-2',
        hue='label',
        hue_order=unique_labels, # Đảm bảo thứ tự legend
        palette=palette,
        ax=ax,
        s=kwargs.get('s', 20),      # Kích thước điểm
        alpha=kwargs.get('alpha', 0.8) # Độ trong suốt
    )
    
    # --- Tinh chỉnh cho đẹp ---
    ax.set_title(title)
    ax.set_xlabel('t-SNE Dimension 1')
    ax.set_ylabel('t-SNE Dimension 2')
    
    # Tắt các số trên trục vì chúng không có ý nghĩa vật lý
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Tắt lưới
    ax.grid(False)
    
    # Tối ưu hóa legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, title='Classes', loc='best')

    if save_and_close:
        plt.savefig(output_path)
        print(f"t-SNE plot saved to: {output_path}")
        plt.close(fig)

    return ax

# ==============================================================================
# Helper function to handle figure/axis creation and saving
# This avoids code repetition in every plotting function.
# ==============================================================================
def _setup_ax_and_save(ax, figsize, output_path):
    """A helper to manage axis creation and figure saving."""
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, layout='constrained')
        save_and_close = True
    else:
        fig = ax.get_figure()
        save_and_close = False
    return fig, ax, save_and_close

# ==============================================================================
# Refactored Plotting Functions
# ==============================================================================

def plot_line_comparison(data: pd.DataFrame, x_col: str, y_cols: list, y_labels: list,
                         x_label: str, y_label: str, title: str, output_path: str,
                         y_error_cols: dict = None, figsize: tuple = (6, 4), ax=None, **kwargs):
    fig, ax, save_and_close = _setup_ax_and_save(ax, figsize, output_path)

    # ... (toàn bộ code vẽ bên trong hàm giữ nguyên, chỉ dùng `ax` đã được setup)
    linestyles = kwargs.get('linestyles', ['-', '--', ':', '-.'])
    markers = kwargs.get('markers', ['o', 's', '^', 'D'])
    colors = kwargs.get('colors', [CONTEXT_COLORS.get(c) for c in ['proposed', 'sota', 'baseline', 'method_A']])

    for i, y_col in enumerate(y_cols):
        style_idx = i % len(linestyles)
        marker_idx = i % len(markers)
        color = colors[i % len(colors)]
        linewidth = 2.0 if i == 0 else 1.5
        x_data, y_data = data[x_col], data[y_col]
        
        ax.plot(x_data, y_data, label=y_labels[i], color=color, linestyle=linestyles[style_idx],
                marker=markers[marker_idx], markevery=10, linewidth=linewidth, zorder=i + 2)
        
        if y_error_cols and y_col in y_error_cols:
            error_col = y_error_cols[y_col]
            y_error = data[error_col]
            ax.fill_between(x_data, y_data - y_error, y_data + y_error, color=color, alpha=0.2, zorder=i + 1)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()
    if 'xlim' in kwargs: ax.set_xlim(kwargs['xlim'])
    if 'ylim' in kwargs: ax.set_ylim(kwargs['ylim'])
    if 'yscale' in kwargs: ax.set_yscale(kwargs['yscale'])

    if save_and_close:
        plt.savefig(output_path)
        print(f"Line plot saved to: {output_path}")
        plt.close(fig)
    return ax


def plot_grouped_bar_chart(data: pd.DataFrame, category_col: str, value_cols: list, value_labels: list,
                           y_label: str, title: str, output_path: str, error_cols: list = None,
                           figsize: tuple = (7, 5), ylim: tuple = None, ax=None, **kwargs):
    fig, ax, save_and_close = _setup_ax_and_save(ax, figsize, output_path)

    # ... (toàn bộ code vẽ bên trong hàm giữ nguyên)
    if error_cols and len(value_cols) != len(error_cols):
        raise ValueError("Số lượng cột giá trị và cột lỗi phải bằng nhau.")
    categories, n_categories, n_values = data[category_col], len(data[category_col]), len(value_cols)
    x = np.arange(n_categories)
    total_width, width = 0.8, 0.8 / n_values
    colors = kwargs.get('colors', [COLOR_PALETTE.get(c) for c in ['blue', 'green', 'orange']])

    for i, value_col in enumerate(value_cols):
        offset = width * (i - (n_values - 1) / 2)
        measurements = data[value_col]
        y_error = data[error_cols[i]] if error_cols else None
        rects = ax.bar(x + offset, measurements, width, label=value_labels[i],
                       color=colors[i % len(colors)], yerr=y_error, capsize=3)
        ax.bar_label(rects, padding=3, fmt='%.2f', fontsize=8)

    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.set_xticks(x, categories)
    ax.legend(title='Metrics')

    if ylim:
        ax.set_ylim(ylim)
    else:
        y_max_val = data[value_cols].max().max()
        y_max = y_max_val
        if error_cols:
            y_max_err = (data[value_cols] + data[error_cols]).max().max()
            y_max = max(y_max_val, y_max_err)
        ax.set_ylim(0, y_max * 1.15)
        
    ax.grid(axis='x', which='both', visible=False)
    ax.grid(axis='y', which='major', linestyle=':', linewidth=0.7)
    
    if save_and_close:
        plt.savefig(output_path)
        print(f"Grouped bar chart saved to: {output_path}")
        plt.close(fig)
    return ax


def plot_heatmap(matrix_data, x_tick_labels, y_tick_labels, y_label: str, x_label: str, title: str,
                 output_path: str, figsize: tuple = (6, 5), cmap: str = 'Blues', show_values: bool = True,
                 value_format: str = 'd', cbar_label: str = 'Count', ax=None):
    fig, ax, save_and_close = _setup_ax_and_save(ax, figsize, output_path)
    
    # ... (toàn bộ code vẽ bên trong hàm giữ nguyên)
    sns.heatmap(matrix_data, annot=show_values, fmt=value_format, cmap=cmap, linewidths=.5, ax=ax,
                xticklabels=x_tick_labels, yticklabels=y_tick_labels, annot_kws={"size": 9},
                cbar_kws={'label': cbar_label})
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title(title)
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right", rotation_mode="anchor")
    plt.setp(ax.get_yticklabels(), rotation=0)
    ax.tick_params(left=False, bottom=False)

    if save_and_close:
        plt.savefig(output_path)
        print(f"Heatmap saved to: {output_path}")
        plt.close(fig)
    return ax


def plot_distribution(data: pd.Series, x_label: str, title: str, output_path: str,
                      figsize: tuple = (6, 4), bins: int = 30, show_kde: bool = True,
                      show_hist: bool = True, color: str = None, ax=None):
    fig, ax, save_and_close = _setup_ax_and_save(ax, figsize, output_path)

    # ... (toàn bộ code vẽ bên trong hàm giữ nguyên)
    if not show_hist and not show_kde: return
    plot_color = color if color else CONTEXT_COLORS['blue']
    if show_hist:
        sns.histplot(data, bins=bins, kde=show_kde, color=plot_color, ax=ax)
    elif show_kde:
        sns.kdeplot(data, color=plot_color, fill=True, alpha=0.5, ax=ax)
    ax.set_ylabel('Frequency' if show_hist else 'Density')
    ax.set_xlabel(x_label)
    ax.set_title(title)
    ax.grid(axis='x', which='both', visible=False)
    ax.grid(axis='y', which='major', linestyle=':', linewidth=0.7)

    if save_and_close:
        plt.savefig(output_path)
        print(f"Distribution plot saved to: {output_path}")
        plt.close(fig)
    return ax


def plot_distribution_comparison(data: pd.DataFrame, x_col: str, y_col: str, y_label: str, x_label: str,
                                 title: str, output_path: str, plot_type: str = 'violin',
                                 figsize: tuple = (8, 5), palette: dict = None, ax=None):
    fig, ax, save_and_close = _setup_ax_and_save(ax, figsize, output_path)

    # ... (toàn bộ code vẽ bên trong hàm giữ nguyên)
    plot_func = sns.violinplot if plot_type == 'violin' else sns.boxplot
    plot_func(x=x_col, y=y_col, data=data, palette=palette, ax=ax)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title(title)
    if len(data[x_col].unique()) > 4:
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    ax.grid(axis='x', which='both', visible=False)
    ax.grid(axis='y', which='major', linestyle=':', linewidth=0.7)

    if save_and_close:
        plt.savefig(output_path)
        print(f"{plot_type.capitalize()} plot saved to: {output_path}")
        plt.close(fig)
    return ax

# src/plot_templates.py
# (thêm vào cuối file)
from scipy.interpolate import griddata

def plot_contour(
    x_data,
    y_data,
    z_data,
    x_label: str,
    y_label: str,
    title: str,
    output_path: str,
    cbar_label: str,
    figsize: tuple = (7, 5),
    cmap: str = 'viridis',
    is_gridded: bool = False,
    grid_resolution: int = 100,
    levels: int = 10,
    show_points: bool = True
):
    """
    Tạo và lưu biểu đồ đường viền (contour plot), có thể nội suy từ dữ liệu rời rạc.

    Args:
        x_data (array-like): Dữ liệu tọa độ X.
        y_data (array-like): Dữ liệu tọa độ Y.
        z_data (array-like): Dữ liệu giá trị Z.
        x_label (str): Nhãn trục X.
        y_label (str): Nhãn trục Y.
        title (str): Tiêu đề biểu đồ.
        output_path (str): Đường dẫn lưu file PDF.
        cbar_label (str): Nhãn cho thanh màu.
        figsize (tuple, optional): Kích thước figure. Mặc định là (7, 5).
        cmap (str, optional): Tên colormap. Mặc định là 'viridis'.
        is_gridded (bool, optional): True nếu dữ liệu đã ở dạng lưới. 
                                     Nếu False, hàm sẽ thực hiện nội suy. Mặc định là False.
        grid_resolution (int, optional): Độ phân giải của lưới nội suy. Mặc định là 100.
        levels (int, optional): Số lượng đường viền. Mặc định là 10.
        show_points (bool, optional): Có hiển thị các điểm dữ liệu gốc hay không. 
                                      Hữu ích khi is_gridded=False. Mặc định là True.
    """
    fig, ax = plt.subplots(figsize=figsize, layout='constrained')
    
    xi, yi, zi = None, None, None
    
    if is_gridded:
        # Dữ liệu đã là lưới, X và Y là vector, Z là ma trận
        xi, yi = x_data, y_data
        zi = z_data
    else:
        # Dữ liệu là các điểm rời rạc, cần nội suy
        # Tạo một lưới đều
        xi = np.linspace(min(x_data), max(x_data), grid_resolution)
        yi = np.linspace(min(y_data), max(y_data), grid_resolution)
        grid_x, grid_y = np.meshgrid(xi, yi)
        
        # Nội suy dữ liệu Z lên lưới
        zi = griddata((x_data, y_data), z_data, (grid_x, grid_y), method='cubic')

    # Vẽ contour plot dạng tô màu (filled)
    contourf = ax.contourf(xi, yi, zi, levels=levels, cmap=cmap, alpha=0.9)
    
    # Vẽ các đường viền
    contour_lines = ax.contour(xi, yi, zi, levels=levels, colors='white', linewidths=0.5)
    
    # Thêm nhãn số lên các đường viền
    ax.clabel(contour_lines, inline=True, fontsize=8, fmt='%.1f')
    
    # Hiển thị các điểm dữ liệu gốc (nếu có)
    if not is_gridded and show_points:
        ax.scatter(x_data, y_data, c='red', s=10, edgecolor='black', linewidth=0.5,
                   label='Data Points', zorder=10)
        ax.legend(loc='upper right')

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    
    # Thêm thanh màu (colorbar)
    cbar = fig.colorbar(contourf, ax=ax)
    cbar.set_label(cbar_label)
    
    plt.savefig(output_path)
    print(f"Contour plot saved to: {output_path}")
    plt.close(fig)
