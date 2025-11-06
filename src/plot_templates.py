# src/plot_templates.py

import matplotlib.pyplot as plt
import pandas as pd
from publication_style import CONTEXT_COLORS # Import bảng màu đã định nghĩa

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

    Args:
        data (pd.DataFrame): DataFrame chứa dữ liệu.
        x_col (str): Tên cột cho trục X.
        y_cols (list): Danh sách tên các cột cho trục Y.
        y_labels (list): Danh sách các nhãn (labels) tương ứng cho mỗi đường.
        x_label (str): Nhãn cho trục X.
        y_label (str): Nhãn cho trục Y.
        title (str): Tiêu đề của biểu đồ.
        output_path (str): Đường dẫn để lưu file PDF.
        figsize (tuple, optional): Kích thước của figure. Mặc định là (6, 4).
        **kwargs: Các tham số tùy chọn khác cho plt.plot (vd: linestyles, markers).
    """
    if len(y_cols) != len(y_labels):
        raise ValueError("Số lượng cột Y và nhãn Y phải bằng nhau.")

    fig, ax = plt.subplots(figsize=figsize)

    # --- Lấy các style từ kwargs hoặc đặt mặc định ---
    # Điều này giúp hàm trở nên linh hoạt hơn
    linestyles = kwargs.get('linestyles', ['-', '--', ':', '-.'])
    markers = kwargs.get('markers', ['o', 's', '^', 'D'])
    colors = kwargs.get('colors', [
        CONTEXT_COLORS.get('proposed'),
        CONTEXT_COLORS.get('sota'),
        CONTEXT_COLORS.get('baseline'),
        CONTEXT_COLORS.get('method_A'),
        CONTEXT_COLORS.get('method_B')
    ])
    
    # --- Vẽ từng đường ---
    for i, y_col in enumerate(y_cols):
        # Đảm bảo các style lặp lại nếu có nhiều đường hơn style đã định nghĩa
        style_idx = i % len(linestyles)
        marker_idx = i % len(markers)
        color_idx = i % len(colors)
        
        # Nhấn mạnh đường đầu tiên (coi như là 'proposed method')
        linewidth = 2.0 if i == 0 else 1.5
        
        ax.plot(
            data[x_col],
            data[y_col],
            label=y_labels[i],
            color=colors[color_idx],
            linestyle=linestyles[style_idx],
            marker=markers[marker_idx],
            markevery=10, # Chỉ hiển thị marker mỗi 10 điểm để tránh rối
            linewidth=linewidth
        )

    # --- Tinh chỉnh plot ---
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()
    
    # Đặt giới hạn trục nếu được cung cấp
    if 'xlim' in kwargs:
        ax.set_xlim(kwargs['xlim'])
    if 'ylim' in kwargs:
        ax.set_ylim(kwargs['ylim'])
    if 'yscale' in kwargs:
        ax.set_yscale(kwargs['yscale'])

    # --- Lưu figure ---
    plt.savefig(output_path)
    print(f"Line plot saved to: {output_path}")
    plt.close(fig) # Đóng figure để giải phóng bộ nhớ, quan trọng khi tạo nhiều hình
