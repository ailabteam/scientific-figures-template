# src/publication_style.py

import matplotlib.pyplot as plt

# ==============================================================================
# Bảng màu tùy chỉnh (Custom Color Palette)
# Đây là nơi chúng ta định nghĩa "ngôn ngữ màu sắc" cho paper của mình.
# Sử dụng bảng màu "Tableau 10" - một lựa chọn rất tốt, rõ ràng và đẹp.
# Ref: https://help.tableau.com/current/pro/desktop/en-us/viewparts_color_palette.htm
# Chúng ta sẽ đặt tên gợi nhớ cho từng màu.
# ==============================================================================
COLOR_PALETTE = {
    'blue':   '#1f77b4',  # Màu xanh dương chính
    'orange': '#ff7f0e',  # Màu cam nhấn mạnh
    'green':  '#2ca02c',  # Màu xanh lá
    'red':    '#d62728',  # Màu đỏ cảnh báo hoặc nhấn mạnh kết quả của bạn
    'purple': '#9467bd',
    'brown':  '#8c564b',
    'pink':   '#e377c2',
    'gray':   '#7f7f7f',  # Màu xám cho baseline hoặc các yếu tố phụ
    'olive':  '#bcbd22',
    'cyan':   '#17becf'
}


# ==============================================================================
# Bảng màu theo ngữ cảnh (Contextual Color Palette)
# Kế thừa tất cả màu từ COLOR_PALETTE và thêm các alias (tên thay thế)
# cho các trường hợp sử dụng phổ biến trong paper.
# ==============================================================================
CONTEXT_COLORS = COLOR_PALETTE.copy() # Bắt đầu bằng cách sao chép tất cả các màu cơ bản
CONTEXT_COLORS.update({
    # --- Aliases for common academic contexts ---
    'proposed':   CONTEXT_COLORS['red'],     # Phương pháp đề xuất
    'our_method': CONTEXT_COLORS['red'],
    
    'sota':       CONTEXT_COLORS['blue'],    # State-of-the-art
    'competitor': CONTEXT_COLORS['blue'],

    'baseline':   CONTEXT_COLORS['gray'],    # Phương pháp nền
    'benchmark':  CONTEXT_COLORS['gray'],
    
    # --- Aliases for generic methods ---
    'method_A':   CONTEXT_COLORS['green'],
    'method_B':   CONTEXT_COLORS['orange'],
    'method_C':   CONTEXT_COLORS['purple'],
})


# ==============================================================================
# Hàm thiết lập style chính
# ==============================================================================
def set_publication_style(font_family='sans-serif'):
    """
    Thiết lập các thông số rcParams của Matplotlib để tạo ra các figure
    có chất lượng cao, sẵn sàng cho việc công bố khoa học.

    Args:
        font_family (str): 'serif' (vd: Times New Roman) hoặc 
                           'sans-serif' (vd: Arial).
    """
    
    # Sử dụng một style cơ bản của Seaborn làm nền tảng
    # 'seaborn-v0_8-paper' là một lựa chọn tốt, 'seaborn-v0_8-ticks' cũng là một lựa chọn tốt
    plt.style.use('seaborn-v0_8-ticks')
    
    # --- 1. Font Settings ---
    if font_family == 'serif':
        plt.rcParams['font.family'] = 'serif'
        plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
        plt.rcParams['mathtext.fontset'] = 'dejavuserif' # Font cho công thức toán
    elif font_family == 'sans-serif':
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
        plt.rcParams['mathtext.fontset'] = 'dejavusans' # Font cho công thức toán
    
    # --- 2. Font Size Hierarchy ---
    # Dựa trên phân tích, chúng ta sẽ đặt các kích thước này
    # để đảm bảo dễ đọc sau khi chèn vào paper (thường font paper là 10pt).
    plt.rcParams['font.size'] = 10           # Kích thước font cơ bản
    plt.rcParams['axes.labelsize'] = 10      # Tên trục x, y
    plt.rcParams['axes.titlesize'] = 11      # Tiêu đề của một subplot
    plt.rcParams['xtick.labelsize'] = 9      # Số trên trục x
    plt.rcParams['ytick.labelsize'] = 9      # Số trên trục y
    plt.rcParams['legend.fontsize'] = 9      # Chú thích
    plt.rcParams['figure.titlesize'] = 12    # Tiêu đề lớn của cả figure
    
    # --- 3. Line and Marker Settings ---
    plt.rcParams['lines.linewidth'] = 1.5    # Độ dày đường mặc định
    plt.rcParams['lines.markersize'] = 5     # Kích thước marker mặc định
    plt.rcParams['lines.markeredgewidth'] = 1.0 # Độ dày viền marker
    
    # --- 4. Axes and Ticks Settings ---
    plt.rcParams['axes.edgecolor'] = 'black' # Màu của các trục
    plt.rcParams['axes.linewidth'] = 1.0     # Độ dày của các trục
    
    # Bật các "ticks" (vạch nhỏ) vào trong để trông gọn gàng hơn
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams['xtick.major.size'] = 5     # Độ dài vạch chính
    plt.rcParams['ytick.major.size'] = 5
    plt.rcParams['xtick.minor.size'] = 3     # Độ dài vạch phụ
    plt.rcParams['ytick.minor.size'] = 3
    
    # Bật hiển thị ticks trên cả 4 cạnh để dễ dàng gióng hàng hơn
    plt.rcParams['xtick.top'] = True
    plt.rcParams['ytick.right'] = True
    
    # --- 5. Legend Settings ---
    plt.rcParams['legend.frameon'] = False   # Tắt khung viền của legend, trông hiện đại hơn
    plt.rcParams['legend.loc'] = 'best'
    
    # --- 6. Grid Settings ---
    plt.rcParams['axes.grid'] = True         # Bật lưới theo mặc định
    plt.rcParams['grid.color'] = 'lightgray' # Màu lưới rất nhạt
    plt.rcParams['grid.linestyle'] = ':'     # Kiểu lưới: chấm chấm
    plt.rcParams['grid.linewidth'] = 0.6
    
    # --- 7. Figure Saving Settings ---
    plt.rcParams['savefig.dpi'] = 600
    plt.rcParams['savefig.format'] = 'pdf'
    plt.rcParams['savefig.bbox'] = 'tight'   # Tự động cắt khoảng trắng thừa khi lưu
    
    print("Publication style set successfully.")
