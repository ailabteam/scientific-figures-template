# src/plot_templates.py (VERSION 2 - SUBPLOT ENABLED)

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from publication_style import CONTEXT_COLORS, COLOR_PALETTE

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
