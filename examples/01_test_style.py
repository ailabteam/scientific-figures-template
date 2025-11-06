# examples/01_test_style.py

import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# --- Thêm thư mục src vào Python Path ---
# Điều này cho phép chúng ta import các module từ thư mục src
# một cách dễ dàng.
# Lấy đường dẫn của thư mục cha của thư mục hiện tại (project root)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(project_root, 'src'))
# --- Kết thúc phần thêm path ---

# Import hàm và các biến màu từ module của chúng ta
from publication_style import set_publication_style, CONTEXT_COLORS

# Áp dụng style!
set_publication_style(font_family='sans-serif') # Bạn có thể đổi thành 'serif' để thử

# --- Tạo dữ liệu giả để vẽ ---
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = -0.5 * np.cos(x) + 0.2 * np.sin(x)

# --- Bắt đầu vẽ ---
# Tạo một figure và một subplot
fig, ax = plt.subplots(figsize=(6, 4)) # Kích thước phổ biến cho 1 cột

# Vẽ các đường, sử dụng màu sắc đã định nghĩa trong CONTEXT_COLORS
ax.plot(x, y1, label='Our Proposed Method', color=CONTEXT_COLORS['proposed'], linewidth=2.0)
ax.plot(x, y2, label='State-of-the-Art (SOTA)', color=CONTEXT_COLORS['sota'], linestyle='--')
ax.plot(x, y3, label='Baseline', color=CONTEXT_COLORS['baseline'], linestyle=':')

# --- Tinh chỉnh ---
ax.set_xlabel('Time (s)')
ax.set_ylabel('Amplitude')
ax.set_title('Example Plot to Test Style')

# Hiển thị legend
ax.legend()

# Lưu figure vào thư mục 'figures'
output_path = os.path.join(project_root, 'figures', '01_style_test.pdf')
plt.savefig(output_path)
print(f"Figure saved to: {output_path}")

# Hiển thị plot trên màn hình
plt.show()
