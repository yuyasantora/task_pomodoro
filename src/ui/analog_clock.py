from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont
import math


class AnalogClockWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(300, 300)
        self.remaining_seconds = 0
        self.total_seconds = 1500
        self.current_phase = "work"
        self.phase_colors = {
            "work": QColor("#FF6B6B"),
            "short_break": QColor("#4ECDC4"),
            "long_break": QColor("#45B7D1")
        }

    def set_time(self, seconds: int):
        self.remaining_seconds = seconds
        self.update()

    def set_total_duration(self, seconds: int):
        self.total_seconds = seconds

    def set_phase(self, phase: str):
        self.current_phase = phase
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        size = min(width, height)
        center_x = width / 2
        center_y = height / 2
        radius = size / 2 - 20

        painter.translate(center_x, center_y)

        self._draw_background(painter, radius)
        self._draw_progress_arc(painter, radius)
        self._draw_clock_face(painter, radius)
        self._draw_center_time(painter)

    def _draw_background(self, painter, radius):
        painter.setPen(QPen(QColor("#E0E0E0"), 2))
        painter.setBrush(QBrush(QColor("#FFFFFF")))
        painter.drawEllipse(QPointF(0, 0), radius, radius)

    def _draw_progress_arc(self, painter, radius):
        if self.total_seconds == 0:
            return

        elapsed = self.total_seconds - self.remaining_seconds
        progress = elapsed / self.total_seconds
        angle = int(progress * 360 * 16)

        color = self.phase_colors.get(self.current_phase, QColor("#FF6B6B"))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(color))

        start_angle = 90 * 16
        painter.drawPie(
            int(-radius), int(-radius),
            int(radius * 2), int(radius * 2),
            start_angle, -angle
        )

        painter.setPen(QPen(QColor("#FFFFFF"), 8))
        painter.setBrush(QBrush(QColor("#FFFFFF")))
        inner_radius = radius * 0.7
        painter.drawEllipse(QPointF(0, 0), inner_radius, inner_radius)

    def _draw_clock_face(self, painter, radius):
        painter.setPen(QPen(QColor("#333333"), 2))

        for hour in range(12):
            angle = math.radians(hour * 30 - 90)
            outer_radius = radius * 0.65
            inner_radius = radius * 0.6

            x1 = math.cos(angle) * inner_radius
            y1 = math.sin(angle) * inner_radius
            x2 = math.cos(angle) * outer_radius
            y2 = math.sin(angle) * outer_radius

            painter.drawLine(int(x1), int(y1), int(x2), int(y2))

    def _draw_center_time(self, painter):
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        time_text = f"{minutes:02d}:{seconds:02d}"

        font = QFont("Arial", 36, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QPen(QColor("#333333")))

        metrics = painter.fontMetrics()
        text_width = metrics.horizontalAdvance(time_text)
        text_height = metrics.height()

        painter.drawText(
            int(-text_width / 2),
            int(text_height / 3),
            time_text
        )
