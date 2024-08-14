import sys

# Import các thành phần cần thiết từ thư viện qtpy
from qtpy.QtCore import (
    Qt, QSize, QPoint, QPointF, QRectF,
    QEasingCurve, QPropertyAnimation, QSequentialAnimationGroup,
    Slot, Property)

from qtpy.QtWidgets import QCheckBox
from qtpy.QtGui import QColor, QBrush, QPaintEvent, QPen, QPainter


class Toggle(QCheckBox):  # Tạo lớp Toggle kế thừa từ QCheckBox

    _transparent_pen = QPen(Qt.transparent)  # Tạo bút vẽ không màu (trong suốt)
    _light_grey_pen = QPen(Qt.lightGray)  # Tạo bút vẽ màu xám nhạt

    def __init__(self,
        parent=None,
        bar_color=Qt.gray,  # Màu của thanh (mặc định là màu xám)
        checked_color=(0, 179, 179),  # Màu khi được chọn (mặc định là màu xanh ngọc)
        handle_color=Qt.white,  # Màu của tay cầm (mặc định là màu trắng)
        ):
        super().__init__(parent)

        # Lưu các thuộc tính màu sắc vào đối tượng để sử dụng trong sự kiện paintEvent
        self._bar_brush = QBrush(bar_color)
        self._bar_checked_brush = QBrush(QColor(checked_color))

        self._handle_brush = QBrush(handle_color)
        self._handle_checked_brush = QBrush(QColor(checked_color).lighter())

        # Cài đặt phần còn lại của widget

        self.setContentsMargins(8, 0, 8, 0)  # Cài đặt lề
        self._handle_position = 0  # Vị trí ban đầu của tay cầm (handle)

        self.stateChanged.connect(self.handle_state_change)  # Kết nối sự kiện thay đổi trạng thái

    def sizeHint(self):
        return QSize(58, 45)  # Kích thước đề xuất của widget

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)  # Kiểm tra xem vị trí có nằm trong vùng nhấn của widget không

    def paintEvent(self, e: QPaintEvent):
        # Hàm xử lý sự kiện vẽ widget

        contRect = self.contentsRect()  # Lấy vùng chứa widget
        handleRadius = round(0.24 * contRect.height())  # Bán kính của tay cầm

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)  # Kích hoạt khử răng cưa

        p.setPen(self._transparent_pen)  # Sử dụng bút vẽ trong suốt
        barRect = QRectF(
            0, 0,
            contRect.width() - handleRadius, 0.40 * contRect.height()  # Kích thước thanh
        )
        barRect.moveCenter(contRect.center())  # Đặt thanh vào giữa vùng chứa
        rounding = barRect.height() / 2  # Bo góc của thanh

        # Đường di chuyển của tay cầm
        trailLength = contRect.width() - 2 * handleRadius
        xPos = contRect.x() + handleRadius + trailLength * self._handle_position  # Tính toán vị trí tay cầm

        if self.isChecked():  # Kiểm tra nếu đang được chọn
            p.setBrush(self._bar_checked_brush)  # Đặt màu thanh khi được chọn
            p.drawRoundedRect(barRect, rounding, rounding)  # Vẽ thanh
            p.setBrush(self._handle_checked_brush)  # Đặt màu tay cầm khi được chọn

        else:
            p.setBrush(self._bar_brush)  # Đặt màu thanh khi không được chọn
            p.drawRoundedRect(barRect, rounding, rounding)  # Vẽ thanh
            p.setPen(self._light_grey_pen)  # Sử dụng bút vẽ màu xám nhạt
            p.setBrush(self._handle_brush)  # Đặt màu tay cầm khi không được chọn

        p.drawEllipse(
            QPointF(xPos, barRect.center().y()),  # Vẽ hình elip cho tay cầm
            handleRadius, handleRadius)

        p.end()  # Kết thúc vẽ

    @Slot(int)
    def handle_state_change(self, value):
        # Xử lý sự thay đổi trạng thái
        self._handle_position = 1 if value else 0  # Đặt vị trí tay cầm

    @Property(float)
    def handle_position(self):
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos):
        """Thay đổi thuộc tính
        Cần gọi phương thức QWidget.update() để cập nhật widget.
        """
        self._handle_position = pos
        self.update()  # Cập nhật widget

    @Property(float)
    def pulse_radius(self):
        return self._pulse_radius

    @pulse_radius.setter
    def pulse_radius(self, pos):
        self._pulse_radius = pos
        self.update()  # Cập nhật widget



class AnimatedToggle(Toggle):  # Tạo lớp AnimatedToggle kế thừa từ Toggle

    _transparent_pen = QPen(Qt.transparent)  # Tạo bút vẽ không màu (trong suốt)
    _light_grey_pen = QPen(Qt.lightGray)  # Tạo bút vẽ màu xám nhạt

    def __init__(self, *args, pulse_unchecked_color="#44999999",
        pulse_checked_color="#4400B0EE", **kwargs):

        self._pulse_radius = 0  # Bán kính xung ban đầu

        super().__init__(*args, **kwargs)

        # Tạo hoạt ảnh cho vị trí tay cầm
        self.animation = QPropertyAnimation(self, b"handle_position", self)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)  # Đường cong easing cho hoạt ảnh
        self.animation.setDuration(200)  # Thời gian hoạt ảnh (200ms)

        # Tạo hoạt ảnh cho hiệu ứng xung
        self.pulse_anim = QPropertyAnimation(self, b"pulse_radius", self)
        self.pulse_anim.setDuration(350)  # Thời gian hoạt ảnh (350ms)
        self.pulse_anim.setStartValue(10)
        self.pulse_anim.setEndValue(20)

        # Nhóm các hoạt ảnh lại để chạy tuần tự
        self.animations_group = QSequentialAnimationGroup()
        self.animations_group.addAnimation(self.animation)
        self.animations_group.addAnimation(self.pulse_anim)

        self._pulse_unchecked_animation = QBrush(QColor(pulse_unchecked_color))  # Màu xung khi không chọn
        self._pulse_checked_animation = QBrush(QColor(pulse_checked_color))  # Màu xung khi chọn



    @Slot(int)
    def handle_state_change(self, value):
        # Dừng hoạt ảnh hiện tại và bắt đầu hoạt ảnh mới
        self.animations_group.stop()
        if value:
            self.animation.setEndValue(1)  # Đặt giá trị cuối cùng khi chọn
        else:
            self.animation.setEndValue(0)  # Đặt giá trị cuối cùng khi không chọn
        self.animations_group.start()  # Bắt đầu nhóm hoạt ảnh

    def paintEvent(self, e: QPaintEvent):

        contRect = self.contentsRect()  # Lấy vùng chứa widget
        handleRadius = round(0.24 * contRect.height())  # Bán kính của tay cầm

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)  # Kích hoạt khử răng cưa

        p.setPen(self._transparent_pen)  # Sử dụng bút vẽ trong suốt
        barRect = QRectF(
            0, 0,
            contRect.width() - handleRadius, 0.40 * contRect.height()  # Kích thước thanh
        )
        barRect.moveCenter(contRect.center())  # Đặt thanh vào giữa vùng chứa
        rounding = barRect.height() / 2  # Bo góc của thanh

        # Đường di chuyển của tay cầm
        trailLength = contRect.width() - 2 * handleRadius

        xPos = contRect.x() + handleRadius + trailLength * self._handle_position  # Tính toán vị trí tay cầm

        if self.pulse_anim.state() == QPropertyAnimation.Running:  # Kiểm tra trạng thái của hoạt ảnh xung
            p.setBrush(
                self._pulse_checked_animation if
                self.isChecked() else self._pulse_unchecked_animation)  # Đặt màu xung
            p.drawEllipse(QPointF(xPos, barRect.center().y()),
                          self._pulse_radius, self._pulse_radius)  # Vẽ xung

        if self.isChecked():  # Kiểm tra nếu đang được chọn
            p.setBrush(self._bar_checked_brush)  # Đặt màu thanh khi được chọn
            p.drawRoundedRect(barRect, rounding, rounding)  # Vẽ thanh
            p.setBrush(self._handle_checked_brush)  # Đặt màu tay cầm khi được chọn

        else:
            p.setBrush(self._bar_brush)  # Đặt màu thanh khi không được chọn
            p.drawRoundedRect(barRect, rounding, rounding)  # Vẽ thanh
            p.setPen(self._light_grey_pen)  # Sử dụng bút vẽ màu xám nhạt
            p.setBrush(self._handle_brush)  # Đặt màu tay cầm khi không được chọn

        p.drawEllipse(
            QPointF(xPos, barRect.center().y()),  # Vẽ hình elip cho tay cầm
            handleRadius, handleRadius)

        p.end()  # Kết thúc vẽ
