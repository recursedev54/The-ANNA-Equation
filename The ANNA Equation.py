import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QColor, QPainter, QPen, QImage, QPixmap
from PyQt5.QtCore import Qt, QPoint

class AnnaEquationVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Anna Equation Visualizer')
        self.setGeometry(100, 100, 800, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        input_layout = QHBoxLayout()
        self.color_input = QLineEdit()
        self.color_input.setPlaceholderText('Enter color (e.g., 471975)')
        input_layout.addWidget(self.color_input)

        visualize_button = QPushButton('Visualize')
        visualize_button.clicked.connect(self.visualize)
        input_layout.addWidget(visualize_button)

        layout.addLayout(input_layout)

        self.color_label = QLabel()
        layout.addWidget(self.color_label)

        self.gradient_label = QLabel()
        layout.addWidget(self.gradient_label)

        self.canvas = AnnaEquationCanvas()
        layout.addWidget(self.canvas)

    def visualize(self):
        color = self.color_input.text()
        if len(color) == 6 and all(c in '0123456789ABCDEFabcdef' for c in color):
            start_color = np.array([int(color[i:i+2], 16) for i in (0, 2, 4)])
            end_color = self.anna_transform(start_color)
            self.color_label.setText(f'Start: #{color.upper()}, End: #{self.rgb_to_hex(end_color)}')
            self.canvas.plot_colors(start_color, end_color)
            self.update_gradient(start_color, end_color)
        else:
            self.color_label.setText('Invalid color format. Please use 6 hexadecimal digits.')

    def anna_transform(self, color):
        r, g, b = color
        if r != g and g != b and r != b:
            if r < b:
                while r > 0 and b < 255:
                    r -= 1
                    b += 1
            elif r > b:
                while r < 255 and b > 0:
                    r += 1
                    b -= 1
        return np.array([r, g, b])

    def rgb_to_hex(self, rgb):
        return '{:02X}{:02X}{:02X}'.format(*rgb)

    def update_gradient(self, start_color, end_color):
        gradient = self.create_gradient(start_color, end_color)
        qimage = QImage(gradient.tobytes(), gradient.shape[1], gradient.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.gradient_label.setPixmap(pixmap)

    def create_gradient(self, start_color, end_color, width=300, height=50):
        gradient = np.zeros((height, width, 3), dtype=np.uint8)
        for x in range(width):
            r = int(start_color[0] + (end_color[0] - start_color[0]) * x / width)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * x / width)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * x / width)
            gradient[:, x] = [r, g, b]
        return gradient

class AnnaEquationCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.start_color = None
        self.end_color = None

    def plot_colors(self, start_color, end_color):
        self.start_color = start_color
        self.end_color = end_color
        self.update()

    def paintEvent(self, event):
        if self.start_color is None or self.end_color is None:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        margin = 50

        # Draw color space
        self.draw_color_space(painter, width, height, margin)

        # Draw coordinate system
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(margin, height - margin, width - margin, height - margin)  # x-axis (R)
        painter.drawLine(margin, height - margin, margin, margin)  # y-axis (G)

        # Label axes
        painter.drawText(width - margin + 5, height - margin + 15, 'R')
        painter.drawText(margin - 15, margin - 5, 'G')

        # Add number labels
        for i in range(0, 256, 64):
            x = margin + (width - 2 * margin) * i / 255
            y = height - margin - (height - 2 * margin) * i / 255
            painter.drawText(int(x), height - margin + 15, str(i))
            painter.drawText(margin - 30, int(y), str(i))

        # Label corners and centers
        self.label_color_space(painter, width, height, margin)

        # Draw color points and connecting line
        self.draw_color_points_and_line(painter, width, height, margin)

    def draw_color_space(self, painter, width, height, margin):
        for x in range(margin, width - margin):
            for y in range(margin, height - margin):
                normalized_x = (x - margin) / (width - 2 * margin)
                normalized_y = (height - y - margin) / (height - 2 * margin)
                
                r = int(255 * normalized_x)
                g = int(255 * normalized_y)
                b = int(255 * (1 - max(normalized_x, normalized_y)))
                
                painter.setPen(QColor(r, g, b))
                painter.drawPoint(x, y)

    def label_color_space(self, painter, width, height, margin):
        painter.setPen(Qt.black)
        painter.drawText(margin, height - margin + 28, "Blue (0, 0, 255)")
        painter.drawText(margin, margin - 18, "Green (0, 255, 0)")
        painter.drawText(width - margin - 48, height - margin + 28, "Red (255, 0, 0)")
        painter.drawText(width - margin - 48, margin - 18, "Yellow (255, 255, 0)")
        painter.drawText(margin + 8, height // 2, "Cyan (0, 255, 255)")
        painter.drawText(width - margin - 54, height // 2, "Orange (255, 128, 0)")
        painter.drawText(width // 2 - 38, height - margin + 28, "Magenta (255, 0, 255)")
        painter.drawText(width // 2 - 38, margin - 18, "Chartreuse (128, 255, 0)")

    def draw_color_points_and_line(self, painter, width, height, margin):
        start_point = self.color_to_point(self.start_color, width, height, margin)
        end_point = self.color_to_point(self.end_color, width, height, margin)

        # Draw connecting line
        painter.setPen(QPen(Qt.white, 2, Qt.DashLine))
        painter.drawLine(start_point, end_point)

        # Draw points
        for point, color, label in [(start_point, self.start_color, 'Start'), (end_point, self.end_color, 'End')]:
            painter.setPen(QPen(Qt.white, 2))
            painter.setBrush(QColor(*color))
            painter.drawEllipse(point, 5, 5)
            
            painter.setPen(Qt.black)
            painter.drawText(point + QPoint(10, 10), f'{label}: ({color[0]}, {color[1]}, {color[2]})')

    def color_to_point(self, color, width, height, margin):
        x = margin + (width - 2 * margin) * color[0] / 255
        y = height - margin - (height - 2 * margin) * color[1] / 255
        return QPoint(int(x), int(y))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AnnaEquationVisualizer()
    ex.show()
    sys.exit(app.exec_())
