from main import *
class ButtonEffects:
    def __init__(self, button, normal_icon, hover_icon, size , pressed_icon=None):
        self.button = button
        self.normal_icon = QIcon(normal_icon)
        self.hover_icon = QIcon(hover_icon)
        self.pressed_icon = QIcon(pressed_icon) if pressed_icon else self.hover_icon

        # Đặt icon mặc định ban đầu
        self.button.setIcon(self.normal_icon)
        self.button.setIconSize(size)
        # Gán sự kiện hover và click
        self.button.enterEvent = self.on_enter
        self.button.leaveEvent = self.on_leave
        self.button.mousePressEvent = self.on_click
        self.button.mouseReleaseEvent = self.on_release

    def on_enter(self, event):
        # Đổi sang icon hover khi di chuột vào
        self.button.setIcon(self.hover_icon)

    def on_leave(self, event):
        # Trở về icon ban đầu khi rời chuột
        self.button.setIcon(self.normal_icon)

    def on_click(self, event):
        # Khi nhấn nút, đổi sang icon nhấn
        self.button.setIcon(self.pressed_icon)
        # Gọi hàm gốc để giữ lại các hiệu ứng mặc định
        super(type(self.button), self.button).mousePressEvent(event)

    def on_release(self, event):
        # Khi nhả nút, đổi lại icon hover hoặc normal
        if self.button.underMouse():
            self.button.setIcon(self.hover_icon)
        else:
            self.button.setIcon(self.normal_icon)
        # Gọi hàm gốc để giữ lại các hiệu ứng mặc định
        super(type(self.button), self.button).mouseReleaseEvent(event)
