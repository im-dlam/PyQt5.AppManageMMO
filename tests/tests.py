item_width = 360
item_spacing = 10
items_per_row = 1367 / (item_width + item_spacing)  # Tính toán số lượng item trên mỗi dòng

print(int(items_per_row) + 0.5)