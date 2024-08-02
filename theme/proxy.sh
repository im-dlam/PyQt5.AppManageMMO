#!/bin/bash
# Đường dẫn tới các thư mục
THEME_DIR="$(pwd)"
APP_DIR="../models/app"
UI_FILE="${THEME_DIR}/proxyitem.ui"
PY_FILE="${THEME_DIR}/proxyitem.py"

echo "Kiểm tra thư mục theme..."
if [ ! -d "$THEME_DIR" ]; then
  echo "Lỗi: Thư mục $THEME_DIR không tồn tại."
  exit 1
fi

echo "Kiểm tra file proxyitem.ui..."
if [ ! -f "$UI_FILE" ]; then
  echo "Lỗi: File $UI_FILE không tồn tại."
  exit 1
fi

echo "Chạy lệnh pyuic5..."
pyuic5 -x "$UI_FILE" -o "$PY_FILE"

echo "Kiểm tra kết quả pyuic5..."
if [ $? -eq 0 ]; then
  echo "Kiểm tra thư mục app..."
  if [ ! -d "$APP_DIR" ]; then
    echo "Lỗi: Thư mục $APP_DIR không tồn tại."
    exit 1
  fi

  echo "Di chuyển file proxyitem.py từ theme sang app..."
  mv "$PY_FILE" "$APP_DIR/proxyitem.py"
  echo "File proxyitem.py đã được chuyển đến thư mục $APP_DIR."
else
  echo "Lỗi: Không thể tạo file proxyitem.py từ proxyitem.ui."
fi
